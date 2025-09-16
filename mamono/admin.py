from django.contrib import admin

from .models import (
    DiscordGuild,
    DiscordLevels,
    DiscordSettings,
    DiscordUser,
)

class DiscordGuildAdmin(admin.ModelAdmin):
    model = DiscordGuild

class DiscordUserAdmin(admin.ModelAdmin):
    model = DiscordUser

class DiscordLevelsAdmin(admin.ModelAdmin):
    model = DiscordLevels

class DiscordSettingsAdmin(admin.ModelAdmin):
    model = DiscordSettings

admin.site.register(DiscordGuild, DiscordGuildAdmin)
admin.site.register(DiscordUser, DiscordUserAdmin)
admin.site.register(DiscordLevels, DiscordLevelsAdmin)
admin.site.register(DiscordSettings, DiscordSettingsAdmin)

