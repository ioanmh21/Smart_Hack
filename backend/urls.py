from django.urls import path

from .views import (
    availability_view,
    book_slot_view,
    chat_sql_api,
    landing,
    login_view,
    logout_view,
    profile_view,
    cancel_booking_view,
)

app_name = "backend"


urlpatterns = [
    path("", landing, name="landing"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/cancel/", cancel_booking_view, name="cancel_reservation"),
    path("api/availability/<str:css_id>/", availability_view, name="availability"),
    path("api/book/", book_slot_view, name="book"),
    path("api/chat/sql/", chat_sql_api, name="chat_sql_api"),
]
