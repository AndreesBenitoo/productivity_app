from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from goals.views import AreaViewSet, GoalViewSet, ScheduleEntryViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'schedule', ScheduleEntryViewSet, basename='schedule')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
