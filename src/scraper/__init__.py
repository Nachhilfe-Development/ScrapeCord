import discord


async def scrape_embed(embed: discord.Embed) -> dict:
    return {
        "title": embed.title if embed.title else None,
        "description": embed.description if embed.description else None,
        "color": embed.color.value if isinstance(embed.color, discord.Color) and embed.color else None,
        "fields": [await scrape_embed_field(field) for field in embed.fields],
        "footer": {
            "icon_url": embed.footer.icon_url if embed.footer.icon_url != discord.Embed.Empty else None,
            "proxy_icon_url": embed.footer.proxy_icon_url if embed.footer.proxy_icon_url else None,
            "text": embed.footer.text if embed.footer.text else None,
        },
        "image": await scrape_embed_media(embed.image) if embed.image else None,
        "thumbnail": await scrape_embed_media(embed.thumbnail) if embed.thumbnail else None,
        "timestamp": embed.timestamp.timestamp() if embed.timestamp else None,
        "type": embed.type,
        "url": embed.url if embed.url else None,
        "video": await scrape_embed_media(embed.video) if embed.video else None,
    }


async def scrape_embed_media(embed_media) -> dict:
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


async def scape_user(user: discord.User | discord.Member, users: dict) -> int:
    if not user.id in users.keys():
        users[user.id] = {
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
    return user.id


async def scape_sticker(sticker: discord.StickerItem) -> dict:
    return {
        "format": str(sticker.format),
        "id": sticker.id,
        "name": sticker.name,
        "url": sticker.url
    }


def scrape_select_option(select_option: discord.SelectOption) -> dict:
    return {
        "label": select_option.label,
        "value": select_option.value,
        "description": select_option.description,
        "default": select_option.default,
    }


async def scrape_component(component: discord.Component) -> dict:
    if isinstance(component, discord.ActionRow):
        return {
            "type": "action_row",
            "children": [await scrape_component(child) for child in component.children]
        }
    elif isinstance(component, discord.Button):
        return {
            "type": "button",
            "custom_id": component.custom_id,
            "disabled": component.disabled,
            "emoji": str(component.emoji) if component.emoji else None,  # FIXME: may cause errors because of discord.PartialEmoji
            "url": component.url,
            "label": component.label,
        }
    elif isinstance(component, discord.SelectMenu):
        return {
            "type": "select_menu",
            "channel_types": [str(channel_type) for channel_type in component.channel_types],  # FIXME: type issue
            "custom_id": component.custom_id,
            "min_values": component.min_values,
            "max_values": component.max_values,
            "options": [scrape_select_option(option) for option in component.options],
            "disabled": component.disabled,
        }
    else:
        raise TypeError(f"Unknown component type: {type(component)}")


async def scrape_message_reference(message_reference: discord.MessageReference) -> dict:
    return {
        "channel_id": message_reference.channel_id,
        "guild_id": message_reference.guild_id,
        "message_id": message_reference.message_id,
        "fail_if_not_exists": message_reference.fail_if_not_exists,
        "jump_url": message_reference.jump_url,
    }


async def scrape_message(message: discord.Message, users: dict) -> dict:
    # TODO: channel mentions, role_mentions, activity, application, interaction, threads
    return {
        "id": message.id,
        "content": message.content,
        "author": await scape_user(message.author, users),
        "created_at": message.created_at.timestamp(),
        "edited_at": message.edited_at.timestamp() if message.edited_at else None,
        "pinned": message.pinned,
        "tts": message.tts,
        "type": str(message.type),
        "embeds": [await scrape_embed(embed) for embed in message.embeds],
        "attachments": [await scrape_attachment(attachment) for attachment in message.attachments],
        "reactions": [await scrape_reactions(reaction) for reaction in message.reactions],
        "mention_everyone": message.mention_everyone,
        "mentions": [await scape_user(user, users) for user in message.mentions],
        "webhook_id": message.webhook_id,
        "flags": await scrape_message_flags(message.flags),
        "stickers": [await scape_sticker(sticker) for sticker in message.stickers],
        "clean_content": message.clean_content,
        "is_system": message.is_system(),
        "system_content": message.system_content,
        "components": [await scrape_component(component) for component in message.components],
        "referenced_message": await scrape_message_reference(message.reference) if message.reference else None,
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
    users = {}
    async for message in channel.history(limit=limit):
        data["messages"].append(await scrape_message(message, users))

    data["users"] = users
    return data
