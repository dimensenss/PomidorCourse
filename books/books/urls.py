from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, auth, UserBookRelationView

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('auth/', auth)
] + debug_toolbar_urls()

urlpatterns += router.urls
