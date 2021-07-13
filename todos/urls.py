
from django.urls import path , include
from . import views as v
urlpatterns = [
    path('',v.docs , name="docs"),
    #task
    path('todos/<str:username>/',v.todos , name="todos"),
    path('viewTask/<str:pk>/',v.viewTask ,  name="viewTask"),
    path('addTask/',v.addTask , name="addTask"),
    path('updateTask/<str:pk>/',v.updateTask , name="updateTask"),
    path('deleteTask/<str:pk>/',v.deleteTask , name="deleteTask"),
    path('isAdminUser/<str:username>/',v.isAdminUser , name="isUserName"),
    #user
    path('signup/',v.signup,name="signup"),
]

from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/',v.UserAPI().as_view(),name="user"),
]

#Teams Logic
urlpatterns +=[
    path("myTeams/<str:username>/",v.myTeams , name="myTeams"),
    path("workers/",v.workers,name="workers"),
    path("getUserIds/<str:username>/",v.getUserIds , name="getUserIds"),
    path('getTeamWorkers/<str:pk>/', v.getTeamWorkers , name="getTeamWorkers"),
    path('teams/',v.teams , name="teams"),
    path('addTeam/',v.addTeam , name="addTeam"),
    path('viewTeam/<str:pk>/',v.viewTeam ,name="viewTeam"),
    path('deleteTeam/<str:pk>/',v.deleteTeam , name="deleteTeam"),
    path('updateTeam/<str:pk>/',v.updateTeam , name="updateTeam"),
    #...
    path("ask/",v.askToBeAdmin , name="ask"),
    path("askList/" , v.askList , name="askList"),
    path("approveAsk/<str:pk>/" , v.approveAsk , name="approveAsk"),
    path("deleteAsk/<str:pk>/" , v.deleteAsk , name="deleteAsk"),
    path("myTeam/<str:username>/",v.userTeam , name="userTeam"),
]