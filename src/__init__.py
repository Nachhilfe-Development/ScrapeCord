from abc import ABC, abstractmethod
import discord


class Exportable(ABC):
    @abstractmethod
    async def export(self) -> dict:
        ...


class Embed(Exportable):
    def __init__(self, embed: discord.Embed):
        self.embed = embed

    async def export(self) -> dict:
        ...


class Attachment(Exportable):
    def __init__(self, atatchment: discord.Attachment):
        self.attachment = atatchment

    async def export(self) -> dict:
        return {
            "content_type": self.attachment.content_type,
            "ephemeral": self.attachment.ephemeral,
            "description": self.attachment.description,
            "is_spoiler": self.attachment.is_spoiler(),
            "filename": self.attachment.filename,
            "height": self.attachment.height,
            "id": self.attachment.id,
            "proxy_url": self.attachment.proxy_url,
            "size": self.attachment.size,
            "url": self.attachment.url,
            "width": self.attachment.width,
        }


class Reactions(Exportable):
    def __init__(self, reaction: discord.Reaction):
        self.reaction = reaction

    async def export(self) -> dict:
        return {
            "count": self.reaction.count,
            "emoji": str(self.reaction.emoji),  # TODO: Union[Emoji, PartialEmoji, str]
            "me": self.reaction.me,
        }


class MessageFlags(Exportable):
    def __init__(self, message_flags: discord.MessageFlags):
        self.message_flags = message_flags

    async def export(self) -> dict:
        return {
            "crossposted": self.message_flags.crossposted,
            "is_crosspost": self.message_flags.is_crosspost(),
            "supress_embeds": self.message_flags.suppress_embeds,
            "source_message_deleted": self.message_flags.source_message_deleted,
            "urgent": self.message_flags.urgent,
            "has_thread": self.message_flags.has_thread,
            "ephemeral": self.message_flags.ephemeral,
            "loading": self.message_flags.loading,
            "failed_to_mention_some_roles_in_thread": self.message_flags.failed_to_mention_some_roles_in_thread,
            "suppress_notifications": self.message_flags.suppress_notifications,
        }


class User(Exportable):
    def __init__(self, user: discord.Member | discord.User):
        self.user = user

    async def export(self) -> dict:
        return {
            "id": self.user.id,
            "name": self.user.name,
            "discriminator": self.user.discriminator,
            "avatar_url": self.user.avatar_url,
            "display_name": self.user.display_name,
        }


class Sticker(Exportable):
    def __init__(self, sticker: discord.StickerItem):
        self.sticker = sticker

    async def export(self) -> dict:
        return {
            "format": str(self.sticker.format),
            "id": self.sticker.id,
            "name": self.sticker.name,
            "url": self.sticker.url
        }


class Message(Exportable):
    def __init__(self, message: discord.Message):
        self.message = message

    async def export(self) -> dict:
        # TODO: channel mentions, role_mentions, activity, application, reference, interaction, components, threads
        return {
            "id": self.message.id,
            "content": self.message.content,
            "author": await User(self.message.author).export(),
            "created_at": self.message.created_at,
            "edited_at": self.message.edited_at,
            "pinned": self.message.pinned,
            "tts": self.message.tts,
            "type": str(self.message.type),
            "embeds": [await Embed(embed).export() for embed in self.message.embeds],
            "attachments": [await Attachment(attatchment).export() for attatchment in self.message.attachments],
            "reactions": [await Reactions(reaction).export() for reaction in self.message.reactions],
            "mention_everyone": self.message.mention_everyone,
            "mentions": [await User(user).export() for user in self.message.mentions],
            "webhook_id": self.message.webhook_id,
            "flags": await MessageFlags(self.message.flags).export(),
            "stickers": [await Sticker(sticker).export() for sticker in self.message.stickers],
            "clean_content": self.message.clean_content,
            "is_system": self.message.is_system(),
            "system_content": self.message.system_content,
        }


class Channel(Exportable):
    def __init__(self, channel: discord.TextChannel, messages: list[Message]):
        self.channel = channel
        self.messages = messages

    async def export(self) -> dict:
        # TODO: permissions
        return {
            "id": self.channel.id,
            "name": self.channel.name,
            "messages": [await message.export() for message in self.messages],
            "topic": self.channel.topic,
            "category_id": self.channel.category,
            "created_at": self.channel.created_at,
            "guild_id": self.channel.guild.id,
            "nsfw": self.channel.is_nsfw(),
            "slowmode_delay": self.channel.slowmode_delay,
            "type": str(self.channel.type),
            "position": self.channel.position,
            "jump_url": self.channel.jump_url,
        }


async def scrap_channel(channel: discord.TextChannel, limit: int = 100) -> Channel:
    messages = []
    async for message in channel.history(limit=limit):
        messages.append(Message(message))
    return Channel(channel, messages)

