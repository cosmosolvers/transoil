from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from gaz.views import SignInViewSet, SignOutViewSet, SignUpViewSet




router = DefaultRouter()


# authentication views
router.register('signin', SignInViewSet, basename='signin')
router.register('signout', SignOutViewSet, basename='signout')
router.register('signup', SignUpViewSet, basename='signup')


urlpatterns = router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
