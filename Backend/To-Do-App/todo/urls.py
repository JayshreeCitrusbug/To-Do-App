from django.conf.urls import url
from .views import TodoView


urlpatterns = [
    url(r'^api/todo/', TodoView.as_view()),
]

app_name = "todo"