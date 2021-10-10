from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.humanize.templatetags.humanize import naturaltime

from .forms import RegistrationForm, AudioForm

from .models import User, Message, Theme, Room, Clip, BinaryRoom

from .AssemblyAI import assembly_ai as assembly_ai

# Create your views here.
def index(request):
    return render(request, "application/index.html")

class Register(View):
    template = 'application/register.html'
    success_url = 'application:index'

    def get(self, request):
        ctx = {
            'form': RegistrationForm(),
        }
        return render(request, self.template, ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            login(request, instance)
            return redirect(self.success_url)
        ctx = {
           'form': form,
        }
        return render(request, self.template, ctx)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("application:index"))

class Login(View):
    template = 'application/login.html'
    success_url = 'application:index'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return render(request, self.template, {
                "error": "Invalid username and/or password."
            })

def about(request):
    return render(request, "application/about.html")

class Connect(LoginRequiredMixin, View):
    template = "application/connect.html"

    def get(self, request):
        try:
            rooms = Room.objects.filter(full=False)
        except Room.DoesNotExist:
            return render(request, self.template, {
                'message': "No active chat rooms for now",
            })
        return render(request, self.template, {
            'rooms': rooms,
        })

class ChatRoom(LoginRequiredMixin, View):
    template = "application/room.html"
    success_url = 'application:room'

    def get(self, request, name):
        theme = Theme.objects.get(name=name)
        room = Room.objects.get(theme=theme)
        return render(request, self.template, {
            'room': room,
        })

    def post(self, request, name):
        theme = Theme.objects.get(name=name)
        room = Room.objects.get(theme=theme)
        message = Message(text=request.POST['message'], owner=request.user, room=room)
        message.save()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'name':name, }))

class Messages(LoginRequiredMixin, View):
    def get(self, request, pk):
        room = BinaryRoom.objects.get(id=pk)
        messages = Message.objects.filter(room=room).order_by('-created_at')[:10]
        results = []

        for m in messages:
            result = [m.text, m.owner.username, naturaltime(m.created_at)]
            results.append(result)

        return JsonResponse(results, safe=False)

class RoomMessages(LoginRequiredMixin, View):
    def get(self, request, name):
        theme = Theme.objects.get(name=name)
        room = Room.objects.get(theme=theme)
        messages = Message.objects.filter(room=room).order_by('-created_at')[:10]
        results = []

        for m in messages:
            result = [m.text, m.owner.username, naturaltime(m.created_at)]
            results.append(result)

        return JsonResponse(results, safe=False)

class People(LoginRequiredMixin, View):
    template = "application/people.html"

    def get(self, request, topic):
        theme = Theme.objects.get(name=topic)
        room = Room.objects.get(theme=theme)

        people = room.people.all()

        return render(request, self.template, {
            "people": people,
        })

class BinaryChat(LoginRequiredMixin, View):
    template = "application/room.html"
    success_url = 'application:binary_chat'

    def get(self, request, pk):
        u1 = User.objects.get(id=pk)
        flag = False
        try:
            room = BinaryRoom.objects.get(person1=u1, person2=request.user)
        except BinaryRoom.DoesNotExist:
            flag = True

        if flag:
            try:
                room = BinaryRoom.objects.get(person1=request.user, person2=u1)
            except:
                room = BinaryRoom.objects.create(person1=u1, person2=request.user)
                room.save()
        return render(request, self.template, {
            'binary_room': room,
            'name': u1.username,
        })

    def post(self, request, pk):
        u1 = User.objects.get(id=pk)
        try:
            room = BinaryRoom.objects.get(person1=u1, person2=request.user)
        except BinaryRoom.DoesNotExist:
            room = BinaryRoom.objects.get(person1=request.user, person2=u1)

        message = Message(text=request.POST['message'], owner=request.user, binary_room=room)
        message.save()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'pk':pk, }))

class LikeMinded(LoginRequiredMixin, View):
    template = "application/connect.html"

    def get(self, request):
        try:
            rooms = Room.objects.filter(full=False)
        except Room.DoesNotExist:
            return render(request, self.template, {
                'message': "No active chat rooms for now",
            })
        return render(request, self.template, {
            'themes': rooms,
        })

class Audio(LoginRequiredMixin, View):
    template = "application/upload.html"
    success_url = 'application:get_heard'

    def get(self, request):
        return render(request, self.template, {
            'form': AudioForm(),
        })

    def post(self, request):
        form = AudioForm(request.POST, request.FILES or None)
        instance = 0
        if form.is_valid():
            instance = form.save()
        else:
            return render(request, self.template, {
                'form': AudioForm(),
            })
        topic = assembly_ai("""destination of the audio file in media directory""")
        themes = Theme.objects.all().name
        if not topic in themes:
            t = Theme.objects.create(name=topic)
            t.save()
            room = Room.objects.create(theme=t)
            room.people.add(request.user)
            room.save()
        else:
            theme = Theme.objects.get(name=topic)
            room = Room.objects.get(theme=theme)
            room.people.add(request.user)
            room.save()
        return HttpResponseRedirect(reverse(self.success_url, kwargs={'topic':topic, }))
