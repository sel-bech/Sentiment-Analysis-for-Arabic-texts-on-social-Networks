from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.get_predict, name="bypost"),
    path('link', view=views.get_predict_link, name="bylink"),
    path('predict/<str:comment>', view=views.get_prediction),
    path('predictlink/<path:link_post>', view=views.get_prediction_link),
]