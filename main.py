#  Copyright (c) 2020.
import quart.flask_patch

from quart import Quart, abort, render_template, request, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization
from socket import gethostbyname, gethostname
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import flask_discord
import asyncio
import sqlite3
import discord
import Embeds
import random
import json
import Roles
import City
import Osu
import os

loop = asyncio.get_event_loop()
client = Bot(command_prefix=commands.when_mentioned_or("ydna!", "city!", "osu!"), loop=loop)
render = render_template
# c = sqlite3.connect()

with open(r"secured/info.json", encoding="utf8") as data:
    data = json.load(data)


with sqlite3.connect("secured/main.db") as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, admin BOOLEAN)")


def ydna_prefix():
    async def decorator(ctx):
        return ctx.prefix == "ydna!"

    return commands.check(decorator)


# Quart Settings
app = Quart(__name__)
app.secret_key = data["SECRET_KEY"].encode("unicode-escape")
app.config["DISCORD_CLIENT_ID"] = data["DISCORD_CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = data["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = f"http://{gethostbyname(gethostname())}/discord/callback" if gethostbyname(gethostname()) != "192.168.128.136" else "http://ydna.themichael-cheng.com/discord/callback"
app.config["DISCORD_BOT_TOKEN"] = data["DISCORD_BOT_TOKEN"]
dc = DiscordOAuth2Session(app)


@client.event
async def on_ready():
    print(f"Online as user {client.user}")


@client.command()
@ydna_prefix()
async def wash_call(ctx):
    voice_client = ctx.guild.voice_client
    channel = voice_client.channel
    while True:
        await voice_client.main_ws.voice_state(ctx.guild.id, channel.id, self_mute=False)
        await voice_client.main_ws.voice_state(ctx.guild.id, channel.id, self_mute=True)


@client.command()
@ydna_prefix()
async def join(ctx):
    await ctx.author.voice.channel.connect()


@client.command()
@ydna_prefix()
async def split(ctx, item: int):
    users = (await client.fetch_channel(739791934180294696)).members
    random.shuffle(users)

    for i in range(item):
        pass


# Quart
@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/login")
async def account():
    if check_user():
        return redirect(url_for("panel"))
    return await render_template("accounts/login.html")


@app.route("/discord/login")
async def login():
    return dc.create_session()


@app.route("/discord/callback")
async def callback():

    await dc.callback_quart()
    if 678630845178839051 not in [g.id for g in dc.fetch_guilds()]:
        dc.revoke()
        return redirect(url_for("errors", e="not_in_our_guild"))

    g = await client.fetch_guild(678630845178839051)

    with sqlite3.connect("secured/main.db") as conn:
        c = conn.cursor()
        if not c.execute(f"SELECT * FROM users WHERE user_id={dc.fetch_user().id}").fetchall():
            c.execute(f"INSERT INTO users (user_id, admin) VALUES (?,?)", (dc.fetch_user().id, 0,))

    return redirect(url_for("panel"))


@app.route("/panel", methods=["GET", "POST"])
@requires_authorization
async def panel():
    return await render("accounts/panel/index.html")


@app.route("/panel/<item>", methods=["GET", "POST"])
@requires_authorization
async def panels(item):
    if item not in ["roles", "admin_reg"]:
        abort(404)
    i = {}
    if item == "roles":
        with sqlite3.connect("secured/main.db") as conn:
            c = conn.cursor()
            i = {"roles": c.execute("SELECT * FROM roles_adding").fetchall()}

    return await render(f"accounts/panel/{item}.html", **i)


@app.route("/admins/<item>")
@requires_authorization
async def admins(item):
    with sqlite3.connect("secured/main.db") as conn:
        c = conn.cursor()
        r = c.execute(f"SELECT * FROM users WHERE user_id={dc.fetch_user().id}").fetchone()

    i = {}

    if r[1] == 0: abort(401)

    if not item in ["roles"]: abort(404)

    if item == "roles":
        with sqlite3.connect("secured/main.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users")

    return await render_template(f"admin/{item}.html", **i)


@app.errorhandler(flask_discord.Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("account", item="login"))


@app.route("/commands")
async def commands():
    return await render("commands.html")


@app.route("/suggestions", methods=["GET", "POST"])
@requires_authorization
async def suggestions():
    if request.method == "POST":
        with sqlite3.connect("secured/main.db") as db:
            suggestion = request.form.get("suggestions")

    return await render("suggestion/suggestions.html")


@app.route("/submissions?<item>", methods=["POST"])
async def submissions(item):
    if list(request.args)[0] == "admin_reg":
        print("entered {}".format(item))
        if (await request.form).get("key") == data["ADMIN_KEY"]:
            with sqlite3.connect("secured/main.db") as conn:
                c = conn.cursor()
                c.execute(f"UPDATE users SET admin = 1 WHERE user_id={dc.fetch_user().id}")
                conn.commit()

            channel = await client.fetch_channel(744894935517495358)
            await channel.send(f"User {dc.fetch_user().name} Registered as an admin!")

            return redirect(url_for("panels", item="admin"))

    elif list(request.args)[0] == "get_role":
        g = await client.fetch_guild(678630845178839051)
        r = g.get_role(int((await request.form).get("role")))
        channel = await client.fetch_channel(736469089614168074)
        u = dc.fetch_user()

        if r.id in [roles.id for roles in (await g.fetch_member(u.id)).roles]: return redirect(url_for('errors', e="already_own_role"))

        with sqlite3.connect("secured/main.db") as conn:
            c = conn.cursor()

            msg = await channel.send(embed=Embeds.Embeds.web_role(reason=(await request.form).get("reason"), member=await g.fetch_member(u.id), role=r))
            c.execute(f"INSERT INTO roles (role_id, msg_id, user_id) VALUES (?,?,?)", (r.id, msg.id, u.id,))
            conn.commit()

        return redirect(url_for("success", item="get_role"))

    abort(404)


@app.route("/success/<item>")
async def success(item):
    if item == "get_role": return await render_template("accounts/success/get_role.html")

    abort(404)


@app.route("/errors/<e>")
async def errors(e):
    if e == "not_in_our_guild":
        return await render("accounts/errors/not_in_guild.html")
    elif e == "already_own_role":
        return await render("accounts/errors/already_own_role.html")

    abort(404)


@app.errorhandler(404)
async def not_found(e):
    return await render("not_found.html")


def check_user():
    try:
        dc.fetch_user()
    except:
        return False
    else:
        return True


app.jinja_env.globals.update(check_user=check_user)
client.add_cog(Roles.Role(client))
client.add_cog(City.City(client))
client.add_cog(Osu.Osu(client))
print("http://ydna.themichael-cheng.com")

# Asyncio Running.
app.run(host=gethostbyname(gethostname()), port=80, use_reloader=False, debug=True, loop=loop, start_now=False)
client.run(data["DISCORD_BOT_TOKEN"])
