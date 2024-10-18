"""
URL configuration for parish_inspection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inspections import views as inspection_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inspection_views.HomeView.as_view(), name='home'),
    path('register/', inspection_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='inspections/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inspections/logout.html'), name='logout'),
    path('parish/create/', inspection_views.ParishCreateView.as_view(), name='create_parish'),
    path('parish/<int:parish_id>/delete/', inspection_views.ParishDeleteView.as_view(), name='delete_parish'),
    path('parish/<int:parish_id>/', inspection_views.ParishDetailView.as_view(), name='parish_detail'),
    path('parish/<int:parish_id>/inspection/create/', inspection_views.InspectionCreateView.as_view(), name='create_inspection'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/', inspection_views.InspectionDetailView.as_view(), name='inspection_detail'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/edit/', inspection_views.InspectionEditView.as_view(), name='edit_inspection'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/delete/', inspection_views.InspectionDeleteView.as_view(), name='delete_inspection'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
