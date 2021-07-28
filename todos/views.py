from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import *
from django.shortcuts import render , redirect 
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import *
from .api import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Create your views here.
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['id'] = user.id
            data['email'] = user.email
            data['username'] = user.username
            worker = Worker(user=user)
            worker.save()
        else:
            data = serializer.errors
            return Response(data)
        user = User.objects.get(username=data['username'])
        data["token"] = AuthToken.objects.create(user)[1]
        return Response(data)


@api_view(['GET'])
def getTeamWorkers(request, pk):
    team = Team.objects.get(pk=pk)
    workers = []
    for worker in team.workers.all():
        workers.append(worker.user.username)
    data = {
        "workers": workers,
    }
    return Response(data)


@api_view(['GET'])
def home(request):
    apiUrls = {
        "List": "/todos/<str:pk>/",  # pk is username for now
        "addteam": "/addTask/",
        "updateTask": "/updateTask/<str:pk>/",  # pk is task id
        "DeleteTask": "/deleteTask/<str:pk>/",  # pk is task id
        "ViewTask": "/viewTask/<str:pk>/",
    }
    return Response(apiUrls)


@api_view(['GET'])
def todos(request, username):
    try:
        username = username.lower()
        user = User.objects.get(username=username)
        worker = Worker.objects.get(user=user)
        tasks = Task.objects.all().filter(worker=worker)
        serializer = TaskSerializer(tasks, many=True)
    except:
        return  # Response({"message": "not a worker yet"})
    return Response(serializer.data)

@api_view(['POST'])
def addTask(request):
    data = request.data
    user = User.objects.get(username=data["worker"])
    worker = Worker.objects.get(user=user)
    data["worker"] = worker.id
    try:
        task = TaskSerializer(data=data)
        print(data)
        if task.is_valid():
            print("valid")
            task.save()
    except:
        print("Error")
    return Response(task.data)

@api_view(["GET"])
def viewTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task)
    data = serializer.data
    print("data : ", data)
    team = Team.objects.get(id=data["team"])
    worker = Worker.objects.get(id=data["worker"])
    data["team"] = team.name
    data["worker"] = worker.user.username
    print("data : ", data)
    return Response(data)


@api_view(['PUT'])
def updateTask(request, pk):
    data = request.data
    user = User.objects.get(username=data["worker"])
    worker = Worker.objects.get(user=user)
    team = Team.objects.get(name=data["team"])
    data["worker"] = worker.id
    data["team"] = team.id
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response({"message": f"Item with id : {pk} was deleted !"})

# teams
@api_view(['GET'])
def teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addTeam(request):
    if request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            team = serializer.save()
            data['response'] = 'successfully registered new Team and Chat room.'
            chatRoom = ChatRoom(team=team)
            chatRoom.save()
        else:
            data = serializer.errors
            return Response(data)
        return Response(data)

@api_view(['GET'])
def viewTeam(request, pk):
    team = Team.objects.get(id=pk)
    serializer = TeamSerializer(team)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTeam(request, pk):
    team = Team.objects.get(id=pk)
    team.delete()
    return Response({"message": f"Item with id : {pk} was deleted !"})

@api_view(['PUT'])
def updateTeam(request, pk):
    team = Team.objects.get(id=pk)
    serializer = TeamSerializer(instance=team, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
def userTeam(request , username):
    user = User.objects.get(username = username)
    admin = AdminUser.objects.get(user = user)
    try:
        team = Team.objects.get(leader = admin)
        serializers = TeamSerializer(team)
        data = serializers.data
        workers = []
        for w in data["workers"]:
            worker = Worker.objects.get(id = w)
            workers.append(worker.user.username)
        data["workers"] = workers
        return Response(data)
    except :
        return Response([])


@api_view(["GET"])
def workers(request):
    work = Worker.objects.all()
    serializer = WorkerSerializer(work, many=True)
    data = serializer.data
    for w in data:
        user = User.objects.get(id=w["user"])
        w["label"] = user.username
        w["value"] = w["id"]
        w.pop('id')
        w.pop("user")

    return Response(data)

@api_view(['POST'])
def askToBeAdmin(request):
    data = request.data
    user = User.objects.get(username = data["username"])
    worker = Worker.objects.get(user = user)
    data["worker"] = worker.id
    print(data)
    ask = AskToBeAdminSerializer(data=data)
    try:
        if ask.is_valid():
            print("valid")
            ask.save()
            return Response(ask.data)
    except:
        return Response({"message": "A leader must have only one Team"})
    return Response({"message": "A leader must have only one Team"})

#admin views
def askList(request):
    asks = AskToBeAdmin.objects.all
    context = {
        "asks" :asks,
    } 
    return render(request,"list.html" ,context)

def approveAsk(request , pk):
    ask = AskToBeAdmin.objects.get(id = pk)
    print(f"{ask.username}  : {ask.worker}")
    user = User.objects.get(username = ask.username)
    adminUser = AdminUser(user=user)
    adminUser.save()
    ask.delete()
    return redirect("askList")

def deleteAsk(request , pk):
    ask = AskToBeAdmin.objects.get(id = pk)
    ask.delete()
    return redirect("askList")

#docs views
def docs(request):
    return render(request , "docs/index.html")


@api_view(['GET'])
def getUserIds(request, username):
    try:
        user = User.objects.get(username=username)
        uid = user.id
    except:
        uid = 0
    try:
        worker = Worker.objects.get(user=user)
        wid = worker.id
    except:
        wid = 0
    try:
        leader = AdminUser.objects.get(user=user)
        lid = leader.id
    except:
        lid = 0
    data = {}
    data["worker"] = wid
    data["user"] = uid
    data["leader"] = lid
    print(data)
    return Response(data)

@api_view(['GET'])
def isAdminUser(request, username):
    valid = False
    try:
        user = User.objects.get(username=username)
        adminUser = AdminUser.objects.get(user=user)
        print("The User : ", user)
        valid = True
        return Response({"isAdmin": valid})
    except:
        return Response({"isAdmin": valid})

@api_view(['GET'])
def chatRoom(request , name):
    team = Team.objects.get(name = name)
    room = ChatRoom.objects.get(team = team)
    data = {
        "room" : room.id
    }
    return Response(data)


@api_view(['GET'])
def roomMessages(request , name):
    team = Team.objects.get(name = name)
    room = ChatRoom.objects.get(team = team)
    messages = Message.objects.all().filter(chatRoom = room)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def sendMessage(request):
    data = request.data
    team = Team.objects.get(name = data["room"])
    room = ChatRoom.objects.get(team = team)
    data["chatRoom"] = room.id
    serializer = MessageSerializer(data=data)
    print(data)
    if serializer.is_valid():
        print("valid !")
        serializer.save()
    return Response(serializer.data)

@api_view(["GET"])
def getUserRooms (request , username):
    print("1")
    user = User.objects.get(username = username)
    print("2")
    leader = AdminUser.objects.get(user = user)
    print("3")
    worker = Worker.objects.get(user = user)
    print("4")
    rooms = []
    print("6")
    teams = Team.objects.all()
    for team in teams :
        workers = team.workers.all()
        for worker in workers:
            if username == worker.user.username:
                rooms.append(team.name)

    try :
        team = Team.objects.get(leader = leader)
        rooms.append(team.name)
    except :
        pass
    rooms = set(rooms)
    return Response(rooms)