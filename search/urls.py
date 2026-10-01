from django.urls import path

from . import views


app_name = "search"


urlpatterns = [
    path(
        "",
        views.chat_page,
        name="chat",
    ),

    path(
        "new/",
        views.new_chat,
        name="new_chat",
    ),

    path(
        "message/",
        views.message,
        name="message",
    ),

    path(
        "clear-history/",
        views.clear_history,
        name="clear_history",
    ),

    # =============================================
    # NEW: Admin Global Search URL
    # =============================================
    path(
        "global-search/",
        views.admin_global_search,
        name="admin-global-search",
    ),

    # =============================================
    # NEW: Live Stats API URL
    # =============================================
    path(
        "live-stats/",
        views.live_stats_api,
        name="live-stats",
    ),
]