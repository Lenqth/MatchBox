# -*- coding : utf8 -*-

import numpy as np
from matplotlib import pyplot as plt
from .judge.util import *
from .judge.shanten import shanten

from .structs import *

import asyncio
import promise
from promise import Promise
import time

import traceback
import threading


class AITsumogiri:
    def __init__(self):
        pass

    def select_discard(self, pl, game):
        return len(pl.hand)-1

    def get_name(self):
        return "ツモ切りAIちゃん"

    async def turn_command_async(self, pl, game, commands):
        return TurnCommand(TurnCommand.DISCARD, -1)

    async def command_async(self, pl, game, commands):
        return Claim(0)

    async def confirm(self, message):
        pass

    async def message(self, message):
        pass

    async def send(self, obj):
        pass


class AIShanten:
    def __init__(self):
        pass

    def get_name(self):
        return "よわいAIちゃん"

    def select_discard(self, pl, game):
        from numpy import random
        h = list(pl.hand)
        if pl.drew is not None:
            h.append(pl.drew)
        ary = list_to_array(h)
        e = np.eye(64, dtype=np.int32)
        q = np.tile(ary, (len(h), 1)) - e[h]
        p = np.apply_along_axis(shanten, 1, q) + random.rand(len(q)) / 2.0
        r = np.argmin(p)
        if pl.drew is not None and (r+1) == len(h):
            return -1
        return r

    async def turn_command_async(self, pl, game, commands):
        if len([1 for x in commands if x.type == TurnCommand.TSUMO]) > 0:
            return TurnCommand(TurnCommand.TSUMO)
        ps = self.select_discard(pl, game)
        cmd = TurnCommand(TurnCommand.DISCARD, pos=ps)
        print(cmd)
        return cmd

    async def command_async(self, pl, game, commands):
        if len([1 for x in commands if x.type == Claim.RON]) > 0:
            return Claim(Claim.RON)
        return Claim(0)

    async def confirm(self, message):
        pass

    async def message(self, message):
        pass

    async def send(self, obj):
        pass


class RemotePlayer:

    def __init__(self, connection):
        self.conn = connection

    def get_name(self):

        return str(self.conn.get_user())

    def send(self, obj):
        if not hasattr(self, "conn"):
            raise Exception("No connection")

    @staticmethod
    def validate_turn_command(command, hand_range, li):
        if command.type == TurnCommand.DISCARD:
            return command.pos in hand_range
        return command in li

    @staticmethod
    def validate_command(command, li):
        return command in li

    async def turn_command_async(self, pl, game, commands):
        obj = {"type": "your_turn", "hand_tiles": pl.hand,
               "draw": pl.drew, "turn_commands_available": commands}
        if pl.agari_infos is not None:
            obj["agari_info"] = pl.agari_infos

        try:
            res = await self.conn.send_and_receive_reply(obj, timeout=game.timeout)
            res = TurnCommand.fromDict(res)
            if not RemotePlayer.validate_turn_command(res, range(0 if pl.drew is None else -1, len(pl.hand)), obj["turn_commands_available"]):
                raise Exception("validation error : %s" % res)
            return res
        except Exception as e:
            traceback.print_exc()
            if pl.drew is not None:
                return TurnCommand(TurnCommand.DISCARD, -1)
            else:
                return TurnCommand(TurnCommand.DISCARD, len(pl.hand)-1)

    async def command_async(self, pl, game, commands):
        obj = {"type": "claim_command", "hand_tiles": pl.hand,
               "target": {"player": game.turn,
                          "apkong": game.apkong,
                          "tile": game.target_tile},
               "commands_available": commands}
        if pl.agari_infos is not None:
            obj["agari_info"] = pl.agari_infos
        try:
            res = await self.conn.send_and_receive_reply(obj, timeout=game.timeout)
            res = Claim.fromDict(res)
            if not RemotePlayer.validate_command(res,  obj["commands_available"]):
                raise Exception("validation error : %s" % res)
            return res
        except Exception as e:
            traceback.format_exc()
            return Claim(0)

    async def confirm(self, message):
        obj = {"type": "confirm", "message": message}
        try:
            await self.conn.send_and_receive_reply(obj, timeout=3000)
        except Exception as e:
            traceback.format_exc()
            return

    async def message(self, message):
        obj = {"type": "message", "message": message}
        await self.conn.send(obj)

    async def send(self, obj):
        await self.conn.send(obj)
