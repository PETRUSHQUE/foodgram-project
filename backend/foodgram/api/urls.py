from django.urls import include, path

urlpatterns = [
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include((
        'recipe_catalogue.urls', 'recipe_catalogue'), namespace='recipes')),
]
