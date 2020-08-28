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

    @staticmethod
    def user_info(user, exp, lvl, balance):
        embed = discord.Embed(title="User Info 使用者資訊", color=discord.Color.blue())
        embed.add_field(name="Level 等級", value=f"Lv. {lvl} (Experience: {exp})")
        embed.add_field(name="Balance ", value=f"${balance}")
        embed.set_author(name=f"User 用戶 {user.nick if user.nick is not None else user.nick}", icon_url=user.avatar_url)

        return embed

    @staticmethod
    def how():
        embed = discord.Embed(title="How this system works? 這套系統如何運作?", color=discord.Color.blurple())

        embed.add_field(name="Level System", value="Ranking System:\n"
                                                   "It will add experience when you type a message\n"
                                                   "1-10 New Comer 新人\n"
                                                   "11-20 Starter 初始者\n"
                                                   "21-45 Advanced 進階\n"
                                                   "46-100 Professional 專業\n"
                                                   "101 - * Expert 老手", inline=False)

        embed.add_field(name="Job System", value="Job System:\n"
                                                 "You can consider it as a booster.\n"
                                                 "You can earn money by a job\n"
                                                 "And also, you can boost up experience.\n", inline=False)

        embed.add_field(name="Bank System", value="Bank System:\n"
                                                  "You can use money to buy item for customizing your profile.\n"
                                                  "Earn by job and rewards.", inline=False)

        return embed