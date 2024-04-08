from django.urls import path
from .views import AuthorREST, BlogREST

urlpatterns = [
    path('author/', AuthorREST.as_view()),
    path('author/<int:id>/', AuthorREST.as_view()),
    path('blog/', BlogREST.as_view()),
    path('blog/<int:id>/', BlogREST.as_view())
]