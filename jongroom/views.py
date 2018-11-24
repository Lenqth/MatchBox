import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

CROSSORIGIN = False

class Config(View):
    def get(self, request, *args, **kwargs):
        from .installed_games import INSTALLED_GAMES
        import importlib
        game = kwargs["game_type"]
        if game in INSTALLED_GAMES:
            conf = importlib.import_module(
                (".games.%s.main" % game), package=__package__).config()
            res = HttpResponse(json.dumps(conf))
        else:
            res = HttpResponse("error")
        #res["Access-Control-Allow-Origin"] = "*" if CROSSORIGIN
        return res


class GetLoginStateAjax(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            res = {"username": request.user.username}
        else:
            res = {"username": None}
        resp = HttpResponse(json.dumps(res))
        #resp["Access-Control-Allow-Origin"] = "*" if CROSSORIGIN
        return resp


class LoginAjax(View):
    def post(self, request, *args, **kwargs):
        user = authenticate(request)
        if user is not None:
            login(request, user)
            res = HttpResponse(json.dumps(user))
        else:
            res = HttpResponse('login failed', status=401)
        #res["Access-Control-Allow-Origin"] = "*" if CROSSORIGIN
        return res


class LogoutAjax(View):
    def post(self, request, *args, **kwargs):
        logout(request)


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
        d = {"room_id": "nyan"}
        return render(request, 'jong.html', d)


class Quarto(View):
    def get(self, request, *args, **kwargs):
        d = {"room_id": "nyan"}
        return render(request, 'quarto/quarto.html', d)


class WebPackIndex(View):
    def get(self, request, *args, **kwargs):
        d = {"room_id": "nyan"}
        return render(request, 'index.html', d)
