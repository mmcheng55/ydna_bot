#  Copyright (c) 2020.

from discord.ext.commands import Cog
from discord.ext import commands
import requests
import sqlite3
import discord


def osu_prefix():
    async def decorator(ctx):
        return ctx.prefix == "osu!"

    return commands.check(decorator)


class Osu(Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect("secured/osu.db")
        self.c = self.conn.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS player (user_id INTEGER, username TEXT)")

    @commands.command()
    @osu_prefix()
    async def register_osu(self, ctx, *, username):
        self.c.execute(f"DELETE FROM player WHERE user_id={ctx.message.author.id}")
        self.c.execute(f"INSERT INTO player (user_id, username) VALUES (?,?)", (ctx.message.author.id, username,))
        await ctx.send(f"Registered to our database (`{username}`)")

    @commands.command(alalies=[])
    @osu_prefix()
    async def rs(self): pass