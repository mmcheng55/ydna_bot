#  Copyright (c) 2020.

from discord.ext.commands import Cog
from discord.ext import commands
import functools
import discord
import sqlite3
import Embeds
import Objs


class City(Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect("secured/city.db")
        self.c = self.conn.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS user (user_id integer, level integer, exp integer)")
        self.c.execute("CREATE TABLE IF NOT EXISTS bank (balance integer, user_id integer, FOREIGN KEY(user_id) REFERENCES user(user_id))")

    def check_prefix(self, ctx):
        if ctx.prefix != "city!":
            raise commands.errors.CommandNotFound(f"Command Not Found.")

    async def check_level(self, ctx, q: list):
        q[2] += 1
        if Objs.level(q[1], q[2]):
            await ctx.send("Level up! You are now {}".format(q[1] + 1))
            q[2] = 0
            q[1] += 1
            return q

        return q

    @commands.command()
    # @check_prefix
    async def register(self, ctx):
        self.check_prefix(ctx)
        if self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchall():
            return await ctx.send("You already register to our database!\n"
                                  "Please check out this command `city!get_info`")

        self.c.execute(f"INSERT INTO user (user_id, level, exp) VALUES ({ctx.author.id}, 1, 0)")
        self.c.execute(f"INSERT INTO bank (balance, user_id) VALUES (0, {ctx.author.id})")
        self.conn.commit()
        await ctx.send("Registered to our database! Please type `city!get_info` to look for more!")

    @commands.command()
    async def get_info(self, ctx):
        self.check_prefix(ctx)

        q = self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchone() if self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchall() else None

        if q is None: return await ctx.send(f"User Not Found.")
        
        b = self.c.execute(f"SELECT * FROM bank WHERE user_id={q[0]}").fetchone()

        await ctx.send(embed=Embeds.Embeds.user_info(ctx.author, q[2], q[1], b[0]))
    
    @commands.command()
    async def how(self, ctx):
        self.check_prefix(ctx)

        await ctx.send(embed=Embeds.Embeds.how())

    @Cog.listener()
    async def on_message(self, message):
        q = list(self.c.execute(f"SELECT * FROM user WHERE user_id={message.author.id}").fetchone())

        q = await self.check_level(message.channel, q)

        print(q)

        self.c.execute(f"UPDATE user SET level={q[1]}, exp={q[2]} WHERE user_id={q[0]}")
        self.conn.commit()
