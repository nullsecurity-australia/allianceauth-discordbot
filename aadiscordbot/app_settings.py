from django.conf import settings
import re


def get_site_url():  # regex sso url
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0]  # first match

    return url


def aastatistics_active():
    return 'aastatistics' in settings.INSTALLED_APPS


def timezones_active():
    return 'timezones' in settings.INSTALLED_APPS


def timerboard_active():
    return 'allianceauth.timerboard' in settings.INSTALLED_APPS


def get_admins():
    from .models import AuthBotConfiguration
    return list(AuthBotConfiguration.objects.get(pk=1).admin_users.all().values_list('uid', flat=True))

def get_low_adm():
    adm = getattr(settings, 'DISCORD_BOT_LOW_ADM', 2.5)
    if isinstance(adm, (float, int)):
        if adm < 0 or adm > 6:
            return 4.5
        else:
            return adm

DISCORD_BOT_COGS = getattr(settings, 'DISCORD_BOT_COGS',[ "aadiscordbot.cogs.about",
                                                          "aadiscordbot.cogs.admin",
                                                          "aadiscordbot.cogs.members",
                                                          "aadiscordbot.cogs.timers",
                                                          "aadiscordbot.cogs.auth",
                                                          "aadiscordbot.cogs.sov",
                                                          "aadiscordbot.cogs.time",
                                                          "aadiscordbot.cogs.eastereggs",
                                                          "aadiscordbot.cogs.remind",
                                                          "aadiscordbot.cogs.reaction_roles"])
