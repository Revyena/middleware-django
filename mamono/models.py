import uuid

from django.db import models


# Abstract base model with fields that should be in all models
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DiscordGuild(BaseModel):
    guild = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

# Abstract model that adds guild scope
class GuildScopedModel(BaseModel):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE, related_name='guilds')

    class Meta:
        abstract = True

class DiscordUser(BaseModel):
    user = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

class DiscordLevel(GuildScopedModel):
    user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE, related_name='users')
    level = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)

    class Meta:
        unique_together = ('guild', 'user')

class DiscordSetting(BaseModel):
    SCOPES = [
        ('GUILD', 'Guild'),
        ('USER', 'User'),
        ('BOT', 'Bot'),
    ]

    scope_type = models.CharField(max_length=5, choices=SCOPES)
    scope_id = models.CharField(max_length=100, null=True, blank=True)
    setting_key = models.CharField(max_length=100)
    setting_value = models.TextField()