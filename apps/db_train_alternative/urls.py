from django.urls import path
<<<<<<< HEAD
from .views import AuthorREST, BlogREST
=======
from .views import AuthorREST

>>>>>>> origin/main

urlpatterns = [
    path('author/', AuthorREST.as_view()),
    path('author/<int:id>/', AuthorREST.as_view()),
<<<<<<< HEAD
    path('blog/', BlogREST.as_view()),
    path('blog/<int:id>/', BlogREST.as_view())
=======
>>>>>>> origin/main
]