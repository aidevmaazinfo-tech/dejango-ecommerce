from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path(
        "recommended-list/",
        views.recommendation_section_view,
        name="recommended_list",
    ),
    path(
        "api/v1/recommendations/",
        views.recommendation_api_view,
        name="recommendations_api",
    ),
]