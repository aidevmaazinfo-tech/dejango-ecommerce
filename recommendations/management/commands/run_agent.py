import time
import logging
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

from django.core.management.base import BaseCommand
from recommendations.models import UserInteraction, UserPreferenceProfile, CachedRecommendation
from products.models import Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs the Autonomous ML Recommendation Agent in a continuous background loop using SVD Matrix Factorization."

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=10,
            help="Loop delay in seconds (default: 10s)",
        )

    def handle(self, *args, **options):
        interval = options["interval"]
        self.stdout.write(
            self.style.SUCCESS(f"🤖 ML Autonomous Agent started (Loop Interval: {interval}s)...")
        )

        while True:
            try:
                self.process_agent_cycle()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error in Agent loop cycle: {e}"))

            time.sleep(interval)

    def process_agent_cycle(self):
        """
        Autonomous Loop Cycle:
        1. Trains a TruncatedSVD Collaborative Filtering model on all UserInteraction logs.
        2. Predicts user-specific item affinity based on learned hidden latent patterns.
        3. Evaluates fallback rules for guest sessions with sparse interactions.
        4. Writes top recommended product mappings to CachedRecommendation.
        """
        # Active product pool base queryset
        products_qs = Product.objects.all()
        if hasattr(Product, "is_active"):
            products_qs = products_qs.filter(is_active=True)

        active_products = list(products_qs.values_list("id", flat=True))
        if not active_products:
            return

        # Fetch distinct authenticated users with recorded actions
        user_ids = list(
            UserInteraction.objects.filter(user__isnull=False)
            .values_list("user_id", flat=True)
            .distinct()
        )

        processed_count = 0

        # =========================================================
        # 1. MACHINE LEARNING ENGINE: COLLABORATIVE FILTERING
        # =========================================================
        if user_ids and len(active_products) > 1:
            processed_count += self.train_and_cache_ml_models(user_ids, active_products)

        # =========================================================
        # 2. GUEST SESSION PROCESSING (INTERACTION FALLBACK)
        # =========================================================
        session_keys = list(
            UserInteraction.objects.filter(user__isnull=True)
            .values_list("session_key", flat=True)
            .distinct()
        )

        for skey in session_keys:
            if not skey:
                continue
            interactions = UserInteraction.objects.filter(user__isnull=True, session_key=skey)
            if interactions.exists():
                self.evaluate_guest_fallback(skey, interactions, active_products)
                processed_count += 1

        if processed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[Agent Cycle] Updated ML recommendations for {processed_count} profiles."
                )
            )

    def train_and_cache_ml_models(self, user_ids, active_product_ids):
        """
        Builds a sparse User-Item Matrix from interaction weights,
        fits TruncatedSVD to discover latent preference features,
        and saves predicted product rankings to CachedRecommendation.
        """
        user_to_idx = {u_id: i for i, u_id in enumerate(user_ids)}
        prod_to_idx = {p_id: i for i, p_id in enumerate(active_product_ids)}
        idx_to_prod = {i: p_id for p_id, i in prod_to_idx.items()}

        interactions = UserInteraction.objects.filter(
            user_id__in=user_ids, product_id__in=active_product_ids
        )

        if not interactions.exists():
            return 0

        rows, cols, data = [], [], []
        for interaction in interactions:
            if interaction.user_id in user_to_idx and interaction.product_id in prod_to_idx:
                rows.append(user_to_idx[interaction.user_id])
                cols.append(prod_to_idx[interaction.product_id])
                data.append(float(interaction.weight))

        if not data:
            return 0

        # Construct Sparse Interaction Matrix
        interaction_matrix = csr_matrix(
            (data, (rows, cols)), shape=(len(user_ids), len(active_product_ids))
        )

        # Determine latent component count dynamically based on matrix dimensions
        n_components = max(1, min(10, len(active_product_ids) - 1, len(user_ids) - 1))
        
        # Train SVD Model to decompose Matrix into User/Item latent features
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        user_factors = svd.fit_transform(interaction_matrix)
        item_factors = svd.components_

        # Reconstruct matrix to predict interaction affinity scores across all items
        reconstructed_matrix = np.dot(user_factors, item_factors)

        processed = 0
        for user_id, u_idx in user_to_idx.items():
            predicted_scores = reconstructed_matrix[u_idx]

            # Downweight items the user has already interacted with to promote novelty
            user_interacted_prod_ids = set(
                interactions.filter(user_id=user_id).values_list("product_id", flat=True)
            )
            for p_id in user_interacted_prod_ids:
                if p_id in prod_to_idx:
                    predicted_scores[prod_to_idx[p_id]] -= 2.0

            # Rank items by highest ML predicted score
            top_prod_indices = np.argsort(predicted_scores)[::-1][:8]
            recommended_product_ids = [idx_to_prod[i] for i in top_prod_indices]

            # Cache ML recommendations
            cache_obj, _ = CachedRecommendation.objects.get_or_create(user_id=user_id)
            cache_obj.recommended_products.set(
                Product.objects.filter(id__in=recommended_product_ids)
            )
            cache_obj.save()
            processed += 1

        return processed

    def evaluate_guest_fallback(self, session_key, interactions, active_product_ids):
        """
        Fallback heuristic engine for guest sessions that haven't registered
        an authenticated user identity in the ML interaction matrix.
        """
        interacted_product_ids = list(interactions.values_list("product_id", flat=True).distinct())

        category_scores = {}
        for interaction in interactions.select_related("product"):
            if interaction.product and interaction.product.category_id:
                cat_id = interaction.product.category_id
                category_scores[cat_id] = category_scores.get(cat_id, 0.0) + float(interaction.weight)

        top_cat_id = max(category_scores, key=category_scores.get) if category_scores else None

        if top_cat_id:
            UserPreferenceProfile.objects.update_or_create(
                session_key=session_key,
                defaults={"favorite_category_id": top_cat_id}
            )

        products = Product.objects.filter(id__in=active_product_ids)
        if top_cat_id:
            products = products.filter(category_id=top_cat_id).exclude(id__in=interacted_product_ids)

        top_products = list(products[:8])
        if len(top_products) < 8:
            fillers = Product.objects.filter(id__in=active_product_ids).exclude(
                id__in=[p.id for p in top_products]
            )[: 8 - len(top_products)]
            top_products.extend(list(fillers))

        cache_obj, _ = CachedRecommendation.objects.get_or_create(session_key=session_key)
        cache_obj.recommended_products.set(top_products)
        cache_obj.save()