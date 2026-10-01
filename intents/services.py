import logging
import re

from .models import Intent


logger = logging.getLogger(__name__)


class IntentService:
    """
    Detects user intent using deterministic rules.
    """

    def detect(
        self,
        message: str
    ) -> Intent | None:

        normalized = self.normalize(
            message
        )

        intents = Intent.objects.filter(
            is_active=True
        )

        for intent in intents:

            triggers = [
                item.strip().lower()
                for item in intent.trigger_phrase.split(",")
                if item.strip()
            ]

            for trigger in triggers:

                if self.matches(
                    normalized,
                    trigger
                ):

                    logger.info(
                        "Intent matched: %s",
                        intent.intent_name
                    )

                    return intent

        logger.info(
            "No intent matched for query: %s",
            message
        )

        return None

    def normalize(
        self,
        text: str
    ) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            "",
            text
        )

        return text.strip()

    def matches(
        self,
        message: str,
        trigger: str
    ) -> bool:

        trigger = trigger.lower().strip()

        return trigger in message