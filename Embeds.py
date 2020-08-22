#  Copyright (c) 2020.
import discord


class Embeds:
    def __init__(self): pass

    @staticmethod
    def web_role(reason: str, member: discord.Member, role: discord.Role):
        embed = discord.Embed(title="申請身分組", description=f"Reason 原因: {reason}")
        embed.add_field(name="身分組 Roles", value=role.mention)
        embed.add_field(name="身分狀態 Status", value="批核中 Pending :grey_question:")
        embed.set_author(name="由身份組 {a} 申請 | Requested By {a}".format(a=member.nick if member.nick is not None else member.name))
        embed.set_footer(text="在網站上申請 Requested on Website: http://ydna.themichael-cheng.com/panel/roles")
        return embed

    @staticmethod
    def embed(role: discord.Role, ctx: discord.ext.commands.Context, reason):
        embed = discord.Embed(title="申請身分組", description=f"Reason 原因: {reason}")
        embed.add_field(name="身分組　Roles", value=role.mention)
        embed.add_field(name="申請狀態　Status", value="批核中 Pending :grey_question:")
        embed.set_author(name="由使用者 {a} 申請 | Requested By {a}".format(
            a=ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name))

        embed.set_footer(text="在Discord上申請 Requested on Discord")

        return embed