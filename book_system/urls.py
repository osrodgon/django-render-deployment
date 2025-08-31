from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include([
            path('books/', include('books.urls')),
            path('categories/', include('categories.urls')),
    ])),
]
