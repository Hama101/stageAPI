from django.db import models

from django.contrib.auth.models import User


class AdminUser(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} + {self.id}"


class Worker(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} + {self.id}"


class Team(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True ,unique=True)
    leader = models.OneToOneField(
        AdminUser, blank=True, null=True, on_delete=models.CASCADE)
    workers = models.ManyToManyField(Worker)

    def __str__(self):
        return f"{self.name} <----> : {self.leader}"

    def getLeader(self):
        return self.leader


class Task(models.Model):
    listOfStatus = [
        ("To Do", "To Do"),
        ("Doing", "Doing"),
        ("Done", "Done")
    ]
    worker = models.ForeignKey(
        Worker, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    delay = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=15, blank=True, null=True, choices=listOfStatus, default="To Do")
    checked = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.worker.user.username} ---> {self.title}"

    def getStatus(self):
        return f"{self.status}"

class AskToBeAdmin(models.Model):
    username = models.CharField(max_length=200 ,blank=True , null=True)
    worker = models.OneToOneField(Worker , blank=True , null=True , on_delete=models.CASCADE)
    discreption = models.CharField(max_length=2000 ,  blank=True , null=True )

    def __str__(self):
        return f"{self.username} is asking to be admin : {self.worker}"

