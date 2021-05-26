# Cog Stuff
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color
from discord.utils import get
# AA Contexts
from django.conf import settings
from aadiscordbot import app_settings, __version__, __branch__

import pendulum
import re

import hashlib
import logging
import traceback
logger = logging.getLogger(__name__)


class About(commands.Cog):
    """
    All about me!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def about(self, ctx):
        """
        All about the bot
        """
        await ctx.trigger_typing()

        embed = Embed(title="AuthBot: The Authening")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/516758158748811264/ae3991584b0f800b181c936cfc707880.webp?size=128"
        )
        embed.colour = Color.blue()

        embed.description = "This is a multi-de-functional discord bot tailored specifically for Alliance Auth Shenanigans."
        regex = r"^(.+)\/d.+"

        matches = re.finditer(regex, settings.DISCORD_CALLBACK_URL, re.MULTILINE)

        for m in matches:
            url = m.groups()
        embed.set_footer(text="Lovingly developed for Init.™ by AaronKable")

        embed.add_field(
            name="Number of Servers:", value=len(self.bot.guilds), inline=True
        )
        embed.add_field(name="Unwilling Monitorees:", value=len(self.bot.users), inline=True)
        embed.add_field(
            name="Auth Link", value="[{}]({})".format(url[0], url[0]), inline=False
        )
        embed.add_field(
            name="Version", value="{}@{}".format(__version__, __branch__), inline=False
        )

        # embed.add_field(
        #     name="Creator", value="<@318309023478972417>", inline=False
        # )

        return await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def uptime(self, ctx):
        """
        Returns the uptime
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.send(
            pendulum.now(tz="UTC").diff_for_humans(
                self.bot.currentuptime, absolute=True
            )
        )

    @commands.command(hidden=True)
    async def get_webhooks(self, ctx):
        """
        Returns the webhooks for the channel
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        hooks = await ctx.message.channel.webhooks()
        if len(hooks) == 0:
            name = "{}_webhook".format(ctx.message.channel.name.replace(" ", "_"))
            hook = await ctx.message.channel.create_webhook(
                        name=name
                    )
            await ctx.message.author.send("{} - {}".format(
                hook.name,
                hook.url
            ))

        else:
            for hook in hooks:
                await ctx.message.author.send("{} - {}".format(
                    hook.name,
                    hook.url
                ))

        return await ctx.message.delete()

    @commands.command(hidden=True)
    async def new_channel(self, ctx):
        """
        create a new channel in a category.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        input_string = ctx.message.content[13:].split(' ')
        if len(input_string) != 2:
            return await ctx.message.add_reaction(chr(0x274C))

        everyone_role = ctx.guild.default_role
        channel_name = input_string[1]
        target_cat = get(ctx.guild.channels, id=int(input_string[0]))

        found_channel = False

        for channel in ctx.guild.channels:   # TODO replace with channel lookup not loop
            if channel.name.lower() == channel_name.lower():
                found_channel = True

        if not found_channel:
            channel = await ctx.guild.create_text_channel(channel_name.lower(),
                                                          category=target_cat)  # make channel

            await channel.set_permissions(everyone_role, read_messages=False,
                                          send_messages=False)

        return await ctx.message.add_reaction(chr(0x1F44D))

    @commands.command(hidden=True)
    async def add_role(self, ctx):
        """
        add a role with read and send to a channel.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        input_string = ctx.message.content[10:].split(' ')
        if len(input_string) != 2:
            return await ctx.message.add_reaction(chr(0x274C))

        target_role = get(ctx.guild.roles, name=input_string[1])
        channel_name = get(ctx.guild.channels, name=input_string[0])
        
        if channel_name:
            await channel_name.set_permissions(target_role, read_messages=True,
                                               send_messages=True)

        return await ctx.message.add_reaction(chr(0x1F44D))

    @commands.command(hidden=True)
    async def add_role_read(self, ctx):
        """
        add a role with read only perms to a channel.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        input_string = ctx.message.content[10:].split(' ')
        if len(input_string) != 2:
            return await ctx.message.add_reaction(chr(0x274C))

        target_role = get(ctx.guild.roles, name=input_string[1])
        channel_name = get(ctx.guild.channels, name=input_string[0])
        
        if channel_name:
            await channel_name.set_permissions(target_role, read_messages=True,
                                               send_messages=False)

        return await ctx.message.add_reaction(chr(0x1F44D))

    @commands.command(hidden=True)
    async def rem_role(self, ctx):
        """
        remove a role from a channel.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        input_string = ctx.message.content[10:].split(' ')
        if len(input_string) != 2:
            return await ctx.message.add_reaction(chr(0x274C))

        target_role = get(ctx.guild.roles, name=input_string[1])
        channel_name = get(ctx.guild.channels, name=input_string[0])

        if channel_name:
            await channel_name.set_permissions(target_role, read_messages=False,
                                               send_messages=False)

        return await ctx.message.add_reaction(chr(0x1F44D))


    @commands.command(hidden=True)
    async def list_role(self, ctx):
        """
        list roles from a channel.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        input_string = ctx.message.content[11:]

        channel_name = get(ctx.guild.channels, name=input_string)
        roles = {}

        if channel_name:
            for role in channel_name.overwrites:
                roles[role.name] = {}
                overides = channel_name.overwrites_for(role)
                for _name, _value in overides:
                    if _value is not None:
                        roles[role.name][_name] = _value
                pass
        embed = Embed(title=f"'{channel_name.name}' Channel Roles")
        embed.colour = Color.blue()
        message = ""
        for key, role in roles.items():
            _msg = f"\n`{key}` Role:\n"
            for r, v in role.items():
                _msg += f"{r}: {v}\n"
            message += _msg
        embed.description = message
        
        return await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def dump_channels(self, ctx):
        """
        dump all channels and roles.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()
        
        await ctx.send(F"Discord may get cranky, this may take some time.\n\nChannels: {len(ctx.guild.channels)}\n\nRoles:{len(ctx.guild.roles)}")
        for channel_name in ctx.guild.channels:
            roles = {}
            for role in channel_name.overwrites:
                roles[role.name] = {}
                overides = channel_name.overwrites_for(role)
                for _name, _value in overides:
                    if _value is not None:
                        roles[role.name][_name] = _value
                pass
            embed = Embed(title=f"'{channel_name.name}' Channel Roles")
            embed.colour = Color.blue()
            message = ""
            for key, role in roles.items():
                _msg = f"\n`{key}` Role:\n"
                for r, v in role.items():
                    _msg += f"{r}: {v}\n"
                message += _msg
            embed.description = message
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def empty_roles(self, ctx):
        """
        dump all roles with no members.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()
        
        await ctx.send(F"Discord may get cranky, this may take some time.\nRole count:{len(ctx.guild.roles)}")
        empties = []
        for role_model in ctx.guild.roles:
            if len(role_model.members) == 0:
                empties.append(role_model.name)

        await ctx.send("\n".join(empties))

    @commands.command(hidden=True)
    async def clear_empty_roles(self, ctx):
        """
        dump all roles with no members.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()
        
        await ctx.send(F"Discord may get cranky, this may take some time.\nRole count:{len(ctx.guild.roles)}")
        empties = 0
        fails = [] 
        for role_model in ctx.guild.roles:
            if len(role_model.members) == 0:
                try:
                    await role_model.delete()
                    empties += 1
                except Exception as e: 
                    fails.append(role_model.name)
                    logger.error(e)

        await ctx.send(f"Deleted {empties} Roles.")
        chunks = [fails[x:x+50] for x in range(0, len(fails), 50)]
        for c in chunks:
            await ctx.send("\n".join(c))

    @commands.command(hidden=True)
    async def list_roles(self, ctx):
        """
        dump all roles with no members.
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()
        
        await ctx.send(F"Discord may get cranky, this may take some time.\nRole count:{len(ctx.guild.roles)}")
        roles = []
        for role_model in ctx.guild.roles:
            roles.append(f"`{role_model.name}`")
        roles.sort()
        chunks = [roles[x:x+50] for x in range(0, len(roles), 50)]
        for c in chunks:
            await ctx.send("\n".join(c))

    @commands.command(hidden=True)
    async def rem_channel(self, ctx):
        """
        deletes a channel... User beware....
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()
        
        input_string = ctx.message.content[13:]

        parts = input_string.split("|")
        channel_name = get(ctx.guild.channels, name=parts[0])

        if channel_name:
            hash = hashlib.sha1(channel_name.name.encode("UTF-8")).hexdigest()[:10]
            if len(parts) == 1:
                await ctx.send(f"This will delete the channel {channel_name.name}\nto confirm reply\n")
                return await ctx.send(f"`!rem_channel {channel_name.name}|{hash}`")
            if len(parts) == 2:
                name = channel_name.name
                await channel_name.delete()
                return await ctx.send(f"Deleted `{name}`")

    @commands.command(hidden=True)
    async def list_cats(self, ctx):
        """
        Lists all Cats....
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        for category in ctx.message.guild.categories:
            await ctx.send(f"{category.name}")
            await ctx.send(f"`{category.id}`")


    @commands.command(hidden=True)
    async def help_admin(self, ctx):
        """
        Hidden help...
        """
        if ctx.message.author.id not in app_settings.get_admins():  # https://media1.tenor.com/images/1796f0fa0b4b07e51687fad26a2ce735/tenor.gif
            return await ctx.message.add_reaction(chr(0x1F44E))

        await ctx.message.channel.trigger_typing()

        command_list = [
            "`get_webhooks` gets a webhook for the current channel and sneds via DM",
            "`add_channel` `cat_id channel_name` Creates a channel",
            "`rem_channel` `channel_name` removes a channel",
            "`add_role` `channel_name role_name` adds a read and send role to channel",
            "`add_role_read` `channel_name role_name` adds a read role to channel",
            "`rem_role` `channel_name role_name` removes a role from a channel",
            "`list_cats` lists all cats",
            "`list_role` `channel_name` Lists roles attached to a channel",
            "`list_roles` lists all roles",
            "`dump_channels` dumps all channels and roles ( will be rate limited )",
            "`empty_roles` lists all roles with no members",
            "`clear_empty_roles` clears all empty roles from the server",
            "`uptime` how ong have we been live"
        ]
        return await ctx.send("\n".join(command_list))

def setup(bot):
    bot.add_cog(About(bot))
