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
        return {
            "title": self.embed.title,
            "description": self.embed.description,
            "color": self.embed.color.value if isinstance(self.embed.color, discord.Color) else self.embed.color,
            "fields": [await scrape_embed_field(field) for field in self.embed.fields],
            "footer": {
                "icon_url": self.embed.footer.icon_url,
                "proxy_icon_url": self.embed.footer.proxy_icon_url,
                "text": self.embed.footer.text,
            },
            "image": await scrape_media(self.embed.image) if self.embed.image else None,
            "thumbnail": await scrape_media(self.embed.thumbnail) if self.embed.thumbnail else None,
            "timestamp": self.embed.timestamp.timestamp() if self.embed.timestamp else None,
            "type": self.embed.type,
            "url": self.embed.url,
            "video": await scrape_media(self.embed.video) if self.embed.video else None,
        }


async def scrape_media(embed_media) -> dict:
    return {
        "height": embed_media.height,
        "proxy_url": embed_media.proxy_url,
        "url": embed_media.url,
        "width": embed_media.width,
    }


async def scrape_embed_field(field: discord.EmbedField) -> dict:
    return {
        "name": field.name,
        "value": field.value,
        "inline": field.inline,
    }


async def scrape_attachment(attachment: discord.Attachment) -> dict:
    return {
        "content_type": attachment.content_type,
        "ephemeral": attachment.ephemeral,
        "description": attachment.description,
        "is_spoiler": attachment.is_spoiler(),
        "filename": attachment.filename,
        "height": attachment.height,
        "id": attachment.id,
        "proxy_url": attachment.proxy_url,
        "size": attachment.size,
        "url": attachment.url,
        "width": attachment.width,
    }


async def scrape_asset(asset: discord.Asset) -> dict:
    return {
        "key": asset.key,
        "url": asset.url
    }


async def scrape_reactions(reaction: discord.Reaction) -> dict:
    return {
        "count": reaction.count,
        "emoji": str(reaction.emoji),  # TODO: Union[Emoji, PartialEmoji, str]
        "me": reaction.me,
    }


async def scrape_message_flags(message_flags: discord.MessageFlags) -> dict:
    return {
        "crossposted": message_flags.crossposted,
        "is_crosspost": message_flags.is_crossposted,
        "supress_embeds": message_flags.suppress_embeds,
        "source_message_deleted": message_flags.source_message_deleted,
        "urgent": message_flags.urgent,
        "has_thread": message_flags.has_thread,
        "ephemeral": message_flags.ephemeral,
        "loading": message_flags.loading,
        "failed_to_mention_some_roles_in_thread": message_flags.failed_to_mention_some_roles_in_thread,
        "suppress_notifications": message_flags.suppress_notifications,
    }


async def scape_user(user: discord.User | discord.Member) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "discriminator": user.discriminator,
        "display_name": user.display_name,
        "accent_color": user.accent_color.value if isinstance(user.accent_color, discord.Color) else user.accent_color,
        "avatar": await scrape_asset(user.avatar),
        "color": user.color.value if isinstance(user.color, discord.Color) else user.color,
        "created_at": user.created_at.timestamp(),
        "default_avatar": await scrape_asset(user.default_avatar),
        "display_avatar": await scrape_asset(user.display_avatar),
        "jump_url": user.jump_url,
        "public_flags": None,  # TODO: public_flags
    }


async def scape_sticker(sticker) -> dict:
    return {
        "format": str(sticker.format),
        "id": sticker.id,
        "name": sticker.name,
        "url": sticker.url
    }


class Component(Exportable):
    def __init__(self, component: discord.Component):
        self.component = component

    async def export(self) -> dict:
        ...  # TODO


async def scrape_message(message: discord.Message) -> dict:
    # TODO: channel mentions, role_mentions, activity, application, reference, interaction, threads
    return {
        "id": message.id,
        "content": message.content,
        "author": await scape_user(message.author),
        "created_at": message.created_at.timestamp(),
        "edited_at": message.edited_at.timestamp() if message.edited_at else None,
        "pinned": message.pinned,
        "tts": message.tts,
        "type": str(message.type),
        "embeds": [await Embed(embed).export() for embed in message.embeds],
        "attachments": [await scrape_attachment(attatchment) for attatchment in message.attachments],
        "reactions": [await scrape_reactions(reaction) for reaction in message.reactions],
        "mention_everyone": message.mention_everyone,
        "mentions": [await scape_user(user) for user in message.mentions],
        "webhook_id": message.webhook_id,
        "flags": await scrape_message_flags(message.flags),
        "stickers": [await scape_sticker(sticker) for sticker in message.stickers],
        "clean_content": message.clean_content,
        "is_system": message.is_system(),
        "system_content": message.system_content,
        "components": [await Component(component).export() for component in message.components],
    }


async def scrape_channel(channel: discord.TextChannel, limit: int = 100) -> dict:
    data = {
            "id": channel.id,
            "name": channel.name,
            "messages": [],
            "topic": channel.topic,
            "category_id": channel.category.id,
            "created_at": channel.created_at.timestamp(),
            "guild_id": channel.guild.id,
            "nsfw": channel.is_nsfw(),
            "slowmode_delay": channel.slowmode_delay,
            "type": str(channel.type),
            "position": channel.position,
            "jump_url": channel.jump_url,
        }
    async for message in channel.history(limit=limit):
        data["messages"].append(await scrape_message(message))

    return data
