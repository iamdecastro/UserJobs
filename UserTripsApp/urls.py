from django.urls import path,include
from . import views


urlpatterns = [
    path("",views.index),
    path("register",views.register),
    path("login",views.login),
    path("log_out",views.log_out),
    path("dashboard",views.dashboard),
    path("Trips/New",views.new_trip),
    path("Trips/Edit/<int:Trip_ID>",views.edit_trip),
    path("Trips/Create",views.trip_create),
    path("Trips/View/<int:Trip_ID>",views.view_trip),
    path("Trips/Join/<int:Trip_ID>",views.join_trip),
    path("Trips/Cancel/<int:Trip_ID>",views.cancel_trip),
    path("Trips/Update/<int:Trip_ID>",views.trip_update),
    path("Trips/Remove/<int:Trip_ID>",views.remove_trip)

]


