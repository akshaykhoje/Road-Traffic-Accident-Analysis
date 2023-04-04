from django.urls import path

from .views import HomePageView, AboutPageView, FormPageView, CityPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("form/", FormPageView.as_view(), name="form"),
    path("form/result", CityPageView.as_view(), name="CityPageView"),
]
