from django.contrib import admin

from .models import (
    DiscordGuild,
    DiscordLevel,
    DiscordSetting,
    DiscordUser,
)

class DiscordGuildAdmin(admin.ModelAdmin):
    model = DiscordGuild

class DiscordUserAdmin(admin.ModelAdmin):
    model = DiscordUser

class DiscordLevelsAdmin(admin.ModelAdmin):
    model = DiscordLevel

class DiscordSettingsAdmin(admin.ModelAdmin):
    model = DiscordSetting

admin.site.site_header = "Mamono Management"

admin.site.register(DiscordGuild, DiscordGuildAdmin)
admin.site.register(DiscordUser, DiscordUserAdmin)
admin.site.register(DiscordLevel, DiscordLevelsAdmin)
admin.site.register(DiscordSetting, DiscordSettingsAdmin)

