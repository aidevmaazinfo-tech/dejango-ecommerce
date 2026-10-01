from django.urls import path

from .views import command_api


app_name = "assistant"


urlpatterns = [
    path(
        "command/",
        command_api,
        name="command",
    ),
]