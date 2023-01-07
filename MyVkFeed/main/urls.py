from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", MainPage.as_view(), name="home"),
    path("post/<int:pk>/", PostView.as_view(), name="post"),
    path("subs/", SubsView.as_view(), name="subs"),
    path("post_search/", PostSearchView.as_view(), name="post_search"),
    path("about/", about, name="about"),
    path("settings/", settings, name="settings"),
    path("filters/", FiltersView.as_view(), name="filters"),
    path("group/<int:pk>/", GroupView.as_view(), name="group"),
    path("about/history/", project_history, name="history"),
    path("start", start_page, name="start"),
]

urlpatterns += i18n_patterns(
    path("accounts/", include("allauth.urls")),
)
