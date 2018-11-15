from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class Room(View):
    def get(self, request, *args, **kwargs):
        d = {}
        return render(request, 'chatindex.html', d)

class RoomSelect(View):
    def get(self, request, *args, **kwargs):
        d = {}
        return render(request, 'roomselect.html', d)

class Jong(View):
    def get(self, request, *args, **kwargs):
        d = {"room_id" : "nyan"}
        return render(request, 'jong.html', d)

class Quarto(View):
    def get(self, request, *args, **kwargs):
        d = {"room_id" : "nyan"}
        return render(request, 'quarto/quarto.html', d)

class TestIndex(View):
    def get(self, request, *args, **kwargs):
        d = {"room_id" : "nyan"}
        return render(request, 'index.html', d)
