"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authentication.views import UserViewset
from support.views import (ProjectViewset,
                           ContributorViewset,
                           IssueViewset,
                           CommentViewset,
                           home)

# router creation
router = routers.SimpleRouter()
# routeur configuration
router.register('user', UserViewset, basename='user')
router.register('project', ProjectViewset, basename='project')

urlpatterns = [
    path('', home, name='home'),
    path('api/', home, name='homeapi'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/contributor/<int:project_pk>/',
         ContributorViewset.as_view(
             {'get': 'list',
              'post': 'create'}
         ),
         name='contributor_list'),
    path('api/contributor/<int:project_pk>/<int:pk>/',
         ContributorViewset.as_view(
             {'get': 'retrieve',
              'delete': 'destroy'}
         ),
         name='contributor_detail'),
    path('api/issue/<int:project_pk>/',
         IssueViewset.as_view(
             {'get': 'list',
              'post': 'create'}
         ),
         name='issue_list'),
    path('api/issue/<int:project_pk>/<int:pk>/',
         IssueViewset.as_view(
             {'get': 'retrieve',
              'put': 'update',
              'patch': 'partial_update',
              'delete': 'destroy'}
         ),
         name='issue_detail'),
    path('api/comment/<int:issue_pk>/',
         CommentViewset.as_view(
             {'get': 'list',
              'post': 'create'}
         ),
         name='comment_list'),
    path('api/comment/<int:issue_pk>/<uuid:pk>/',
         CommentViewset.as_view(
             {'get': 'retrieve',
              'put': 'update',
              'patch': 'partial_update',
              'delete': 'destroy'}
         ),
         name='comment_detail')
]
