#  Copyright (c) 2020.

from discord.ext.commands import Cog
from discord.ext import commands
import functools
import discord
import sqlite3
import Embeds
import Objs


# TODO: Job System
# TODO: Admin Award System

def city_prefix():
    async def decorator(ctx):
        return ctx.prefix == "city!"

    return commands.check(decorator)


class City(Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect("secured/city.db")
        self.c = self.conn.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS user (user_id integer, level integer, exp integer)")
        self.c.execute("CREATE TABLE IF NOT EXISTS bank (balance integer, user_id integer, FOREIGN KEY(user_id) REFERENCES user(user_id))")
        self.c.execute("CREATE TABLE IF NOT EXISTS job (user_id integer, job text, multiplier integer, FOREIGN KEY(user_id) REFERENCES user(user_id))")

    async def check_level(self, ctx, q: list, m: list):
        q[2] += m[2]
        if Objs.level(q[1], q[2]):
            await ctx.channel.send(f"Level up! {ctx.author.mention} is now {q[1] + 1}")
            q[2] = 0
            q[1] += 1
            return q

        return q

    @commands.command()
    @city_prefix()
    async def register(self, ctx):
        if self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchall():
            return await ctx.send("You already register to our database!\n"
                                  "Please check out this command `city!get_info`")

        self.c.execute(f"INSERT INTO user (user_id, level, exp) VALUES ({ctx.author.id}, 1, 0)")
        self.c.execute(f"INSERT INTO bank (balance, user_id) VALUES (0, {ctx.author.id})")
        self.c.execute(f"INSERT INTO job (user_id, job, multiplier) VALUES (?,?,?)", (ctx.author.id, "None", 1))
        self.conn.commit()
        await ctx.send("Registered to our database! Please type `city!get_info` to look for more!")

    @commands.command()
    @city_prefix()
    async def get_info(self, ctx):
        q = self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchone() if self.c.execute(f"SELECT * FROM user WHERE user_id={ctx.author.id}").fetchall() else None

        if q is None: return await ctx.send(f"User Not Found.")
        
        b = self.c.execute(f"SELECT * FROM bank WHERE user_id={q[0]}").fetchone()

        await ctx.send(embed=Embeds.Embeds.user_info(ctx.author, q[2], q[1], b[0]))
    
    @commands.command()
    @city_prefix()
    async def how(self, ctx):

        await ctx.send(embed=Embeds.Embeds.how())

    @commands.command()
    @city_prefix()
    async def get_job(self, ctx):
        pass

    @Cog.listener("on_message")
    async def on_message(self, message):
        print(message.author.id)

        q = list(self.c.execute(f"SELECT * FROM user WHERE user_id={message.author.id}").fetchone())
        m = list(self.c.execute(f"SELECT * FROM job WHERE user_id={message.author.id}").fetchone())
        b = list(self.c.execute(f"SELECT * FROM bank WHERE user_id={message.author.id}").fetchone())

        q = await self.check_level(message, q, m)

        self.c.execute(f"UPDATE user SET level={q[1]}, exp={q[2]} WHERE user_id={q[0]}")
        self.c.execute(f"UPDATE bank SET balance={b[0] + 0.1 } WHERE user_id={b[1]}")
        self.conn.commit()
