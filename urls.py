from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginTokenView, ProfileListView, ProfileDetailView, PostViewSet, OpportunityViewSet, ReportCreateView, AppealCreateView

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("opportunities", OpportunityViewSet, basename="opportunity")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", LoginTokenView.as_view(), name="token"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("reports/", ReportCreateView.as_view(), name="report"),
    path("appeals/", AppealCreateView.as_view(), name="appeal"),
    path("", include(router.urls)),
]
