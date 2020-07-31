from discord.ext import commands
from discord.ext.commands import Bot
from models import *
from quart import Quart, render_template
import asyncio
import datetime
import discord
import threading


client = Bot(command_prefix=commands.when_mentioned_or("ydna!"))
app = Quart(__name__)


def bot()
    client.run('NzM2OTA5MTQyMDM1Mzk4Njk5.Xx1qHg.ZPo70qNxcYD3n0667UEvY1G__qk')


def website():
    app.run()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")


@client.command()
async def c_role(ctx, role: discord.Role):
    # await ctx.send(find_query(RolesCanBeAdded, RolesCanBeAdded.id == int(role)))
    if find_query(RolesCanBeAdded, RolesCanBeAdded.id_ == role.id) is None and 736463134474109002 in [y.id for y in ctx.message.author.roles]:
        RolesCanBeAdded(name=role.name, id_=role.id).save()
        await ctx.send("Role Registered (ID: %d | Name: %s) at database" % (role.id, role.name))
    else:
        await ctx.send("Register Procedure Failed.")


@client.command()
async def delete_role(ctx, role: discord.Role):
    if find_query(RolesCanBeAdded, RolesCanBeAdded.id_ == role.id) and 736463134474109002 in [y.id for y in ctx.message.author.roles]:
        RolesCanBeAdded.delete().where(RolesCanBeAdded.id_ == role.id).execute()
        await ctx.send("Role Successfully deleted. ( Role ID: %d | Role Name: %s )" % (role.id, role.name))
    else:
        await ctx.send("Delete Procedure Failed.")

@client.command()
async def get_role(ctx, role: discord.Role, *, reason=""):
    if find_query(RolesCanBeAdded, RolesCanBeAdded.id_ == int(role.id)) and role.id not in [y.id for y in ctx.message.author.roles] and ctx.channel.id == 736469089614168074:
        embed = discord.Embed(title="申請身分組", description="Reason 原因: {}".format(reason), color=discord.Colour.light_grey())

        embed.set_author(name="由使用者 {d} 申請 Requested by {d}".format(d=ctx.message.author.name if ctx.message.author.nick is None else ctx.message.author.nick), icon_url=ctx.message.author.avatar_url)

        embed.add_field(name="身分組 Role", value="%s" % role.mention)
        embed.add_field(name="申請狀態 Status", value="申請中 Pending")
        await ctx.message.delete()
        msg = await ctx.send(embed=embed)

        VotingForRoles(user_id=ctx.message.author.id, role_id=role.id, msg_id=msg.id).save()
        CommandRecords(user_id=ctx.message.author.id, command=ctx.message, command_type="Role/Commands", action="Get Role (PENDING)", time=datetime.datetime.now()).save()

    elif role.id in [y.id for y in ctx.message.author.roles]:
        await ctx.message.delete()
        embed = discord.Embed(title="ERROR 錯誤", description="You already have the role. 你已經有該身份組", color=discord.Colour.red())
        embed.set_author(name="由使用者 {d} 申請 Requested by {d}".format(d=ctx.message.author.name if ctx.message.author.nick is None else ctx.message.author.nick),
                         icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    elif find_query(RolesCanBeAdded, RolesCanBeAdded.id_ == int(role.id)) is None:
        await ctx.message.delete()
        embed = discord.Embed(title="Error 錯誤", description="This Role Is Not Available. 這個身分組未能申請")
        embed.set_author(name="由使用者 {d} 申請 Requested by {d}".format(d=ctx.message.author.name if ctx.message.author.nick is None else ctx.message.author.nick),
                         icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.event
async def on_reaction_add(reaction, user):
    if find_query(VotingForRoles, VotingForRoles.msg_id == int(reaction.message.id)):
        q = find_query(VotingForRoles, VotingForRoles.msg_id == int(reaction.message.id))

        if str(reaction) == "⭕":
            print("Application Approved")
            await reaction.message.guild.get_member(q.user_id).add_roles(reaction.message.guild.get_role(q.role_id))

            embed = await reaction.message.channel.fetch_message(q.msg_id)
            embed = embed.embeds[0].copy()

            embed.remove_field(1)
            embed.color = discord.Colour.green()
            embed.add_field(name="申請狀態 Status", value="批核 Approved :white_check_mark:")
            embed.add_field(name="經手人 Moderator", value=user.mention)

            c = await reaction.message.channel.fetch_message(q.msg_id)
            await c.edit(embed=embed)

            VotingForRoles.delete().where(VotingForRoles.msg_id == q.msg_id)
            CommandRecords(user_id=user, command=f"Approving {q.user_id}'s role (Role ID: %s | Role Name: %s)" % (q.role_id, await reaction.message.guild.get_role(q.role_id)), command_type="Roles/Reaction",
                           action="Get Role (Approved)", time=datetime.datetime.now()).save()

        elif str(reaction) == "❌":
            print("Application Rejected")
            await reaction.message.guild.get_member(q.user_id).add_roles(reaction.message.guild.get_role(q.role_id))

            embed = await reaction.message.channel.fetch_message(q.msg_id)
            embed = embed.embeds[0].copy()

            embed.remove_field(1)
            embed.color = discord.Colour.red()
            embed.add_field(name="申請狀態 Status", value="拒絕 Declined :x:")
            embed.add_field(name="經手人 Moderator", value=user.mention)

            c = await reaction.message.channel.fetch_message(q.msg_id)
            await c.edit(embed=embed)

            VotingForRoles.delete().where(VotingForRoles.msg_id == q.msg_id).execute()


# Flask Section
@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/check-records")
async def check_records():
    print(find_query(CommandRecords, CommandRecords.id > -1))
    return await render_template("check_records.html", cmds=find_query(CommandRecords, CommandRecords.id > -1))


if __name__ == "__main__":
    b = threading.Thread(target=bot)
    # w = threading.Thread(target=website)
    b.start()
    # w.start()
