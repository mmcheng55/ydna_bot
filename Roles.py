#  Copyright (c) 2020.
from discord.ext.commands import Cog
from discord.ext import commands
import discord
import sqlite3


def ydna_prefix():
    async def decorator(ctx):
        return ctx.prefix == "ydna!"

    return commands.check(decorator)


class Role(Cog):
    __doc__ = ["client", "conn", "c"]

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect("secured/main.db", check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS roles (role_id INTEGER, msg_id INTEGER, user_id INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS roles_adding (role_id INTEGER, role_name STRING)")

    def check_admin(self, user: discord.Member):
        if 736463134474109002 in [u.id for u in user.roles]:
            return True
        return False

    @commands.command()
    @ydna_prefix()
    async def create_role(self, ctx, role: discord.Role):
        if self.check_admin(ctx.author) and not self.c.execute(
                f"SELECT * FROM roles_adding WHERE role_id={role.id}").fetchall():
            self.c.execute(f"INSERT INTO roles_adding (role_id, role_name) VALUES (?,?)", (role.id, role.name,))
            self.conn.commit()
            await ctx.send("Role Added Successfully!")
            return

        await ctx.send("Role Was Not Added Successfully.")

    @commands.command()
    @ydna_prefix()
    async def delete_role(self, ctx, role: discord.Role):
        if self.check_admin(ctx.author):
            self.c.execute(f"DELETE FROM roles_adding WHERE role_id={role.id}")
            print("Deleted role.")

    @commands.command()
    @ydna_prefix()
    async def get_role(self, ctx, role: discord.Role, *, reason=None):
        errors = []
        if not ctx.message.channel.id == 736469089614168074:
            errors.append("Wrong channel to send!")

        if role.id in [r.id for r in ctx.message.author.roles]:
            errors.append("You already own this role!")

        if not self.c.execute(f"SELECT * FROM roles_adding WHERE role_id={role.id}").fetchall():
            errors.append("You cant get this role!")

        if errors:
            return await ctx.send(
                embed=discord.Embed(title="ERROR", description="\n".join(errors), color=discord.Color.red()))

        msg = await ctx.send(embed=Embeds.Embeds.embed(role, ctx, reason))
        self.c.execute(f"INSERT INTO roles (role_id, msg_id, user_id) VALUES (?,?,?)",
                       (role.id, msg.id, ctx.message.author.id))
        self.conn.commit()

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        if self.c.execute(f"SELECT * FROM roles WHERE msg_id={reaction.message.id}").fetchall():
            q = self.c.execute(f"SELECT * FROM roles WHERE msg_id={reaction.message.id}").fetchall()
            if reaction.emoji == "\u2B55":  # ⭕
                embed = reaction.message.embeds[0].copy()

                embed.remove_field(1)
                embed.color = discord.Color.green()
                embed.add_field(name="申請狀態 Status", value="批核成功 Approved :white_check_mark:")
                embed.add_field(name="經手人 Moderator", value=user.mention)

                await reaction.message.edit(embed=embed)

                self.c.execute(f"DELETE FROM roles WHERE msg_id={reaction.message.id}")
                self.conn.commit()

                await reaction.message.guild.get_member(int(q[0][2])).add_roles(
                    reaction.message.guild.get_role(q[0][0]))

            elif reaction.emoji == "\u274C":  # ❌
                embed = reaction.message.embeds[0].copy()

                embed.remove_field(1)
                embed.color = discord.Color.red()
                embed.add_field(name="申請狀態 Status", value="批核成功 Declined :x:")
                embed.add_field(name="經手人 Moderator", value=user.mention)

                await reaction.message.edit(embed=embed)

                self.c.execute(f"DELETE FROM roles WHERE msg_id={reaction.message.id}")
                self.conn.commit()

