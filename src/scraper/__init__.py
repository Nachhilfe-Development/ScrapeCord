import discord


class Scraper:
    def __init__(self, channel: discord.TextChannel, limit: int = 100):
        self.__channel = channel
        self.__limit = limit
        self.__users: dict
        
    async def scrape_channel(self) -> dict:
        self.__users = {}

        data = {
                "id": self.__channel.id,
                "name": self.__channel.name,
                "messages": [],
                "topic": self.__channel.topic,
                "category_id": self.__channel.category.id,
                "created_at": self.__channel.created_at.timestamp(),
                "guild_id": self.__channel.guild.id,
                "nsfw": self.__channel.is_nsfw(),
                "slowmode_delay": self.__channel.slowmode_delay,
                "type": str(self.__channel.type),
                "position": self.__channel.position,
                "jump_url": self.__channel.jump_url,
            }
        async for message in self.__channel.history(limit=self.__limit):
            data["messages"].append(await self.__scrape_message(message))

        data["users"] = self.__users
        return data
    
    async def __scrape_message(self, message: discord.Message) -> dict:
        # TODO: channel mentions, role_mentions, activity, application, interaction, threads
        return {
            "id": message.id,
            "content": message.content,
            "author": await Scraper.__scape_user(message.author, self.__users),
            "created_at": message.created_at.timestamp(),
            "edited_at": message.edited_at.timestamp() if message.edited_at else None,
            "pinned": message.pinned,
            "tts": message.tts,
            "type": str(message.type),
            "embeds": [await Scraper.__scrape_embed(embed) for embed in message.embeds],
            "attachments": [await Scraper.__scrape_attachment(attachment) for attachment in message.attachments],
            "reactions": [await Scraper.__scrape_reactions(reaction) for reaction in message.reactions],
            "mention_everyone": message.mention_everyone,
            "mentions": [await Scraper.__scape_user(user, self.__users) for user in message.mentions],
            "webhook_id": message.webhook_id,
            "flags": await Scraper.__scrape_message_flags(message.flags),
            "stickers": [await Scraper.__scape_sticker(sticker) for sticker in message.stickers],
            "clean_content": message.clean_content,
            "is_system": message.is_system(),
            "system_content": message.system_content,
            "components": [await self.__scrape_component(component) for component in message.components],
            "referenced_message": await self.__scrape_message_reference(message.reference) if message.reference else None,
        }
    
    @staticmethod
    async def __scrape_message_reference(message_reference: discord.MessageReference) -> dict:
        return {
            "channel_id": message_reference.channel_id,
            "guild_id": message_reference.guild_id,
            "message_id": message_reference.message_id,
            "fail_if_not_exists": message_reference.fail_if_not_exists,
            "jump_url": message_reference.jump_url,
        }

    @staticmethod
    async def __scrape_component(component: discord.Component) -> dict:
        if isinstance(component, discord.ActionRow):
            return {
                "type": "action_row",
                "children": [await Scraper.__scrape_component(child) for child in component.children]
            }
        elif isinstance(component, discord.Button):
            return {
                "type": "button",
                "custom_id": component.custom_id,
                "disabled": component.disabled,
                "emoji": str(component.emoji) if component.emoji else None,  # FIXME: may cause errors because of discord.PartialEmoji
                "url": component.url,
                "label": component.label,
                "style": component.style.value
            }
        elif isinstance(component, discord.SelectMenu):
            return {
                "type": "select_menu",
                "channel_types": [str(channel_type) for channel_type in component.channel_types],  # FIXME: type issue
                "custom_id": component.custom_id,
                "min_values": component.min_values,
                "max_values": component.max_values,
                "options": [Scraper.__scrape_select_option(option) for option in component.options],
                "disabled": component.disabled,
            }
        else:
            raise TypeError(f"Unknown component type: {type(component)}")
    
    @staticmethod
    def __scrape_select_option(select_option: discord.SelectOption) -> dict:
        return {
            "label": select_option.label,
            "value": select_option.value,
            "description": select_option.description,
            "default": select_option.default,
        }

    @staticmethod
    async def __scrape_message_flags(message_flags: discord.MessageFlags) -> dict:
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
    
    @staticmethod
    async def __scrape_embed(embed: discord.Embed) -> dict:
        return {
            "title": embed.title if embed.title else None,
            "description": embed.description if embed.description else None,
            "color": embed.color.value if isinstance(embed.color, discord.Color) and embed.color else None,
            "fields": [await Scraper.__scrape_embed_field(field) for field in embed.fields],
            "footer": {
                "icon_url": embed.footer.icon_url if embed.footer.icon_url != discord.Embed.Empty else None,
                "proxy_icon_url": embed.footer.proxy_icon_url if embed.footer.proxy_icon_url else None,
                "text": embed.footer.text if embed.footer.text else None,
            },
            "image": await Scraper.__scrape_embed_media(embed.image) if embed.image else None,
            "thumbnail": await Scraper.__scrape_embed_media(embed.thumbnail) if embed.thumbnail else None,
            "timestamp": embed.timestamp.timestamp() if embed.timestamp else None,
            "type": embed.type,
            "url": embed.url if embed.url else None,
            "video": await Scraper.__scrape_embed_media(embed.video) if embed.video else None,
        }
    
    @staticmethod
    async def __scrape_embed_media(embed_media) -> dict:
        return {
            "height": embed_media.height,
            "proxy_url": embed_media.proxy_url,
            "url": embed_media.url,
            "width": embed_media.width,
        }

    @staticmethod
    async def __scrape_embed_field(field: discord.EmbedField) -> dict:
        return {
            "name": field.name,
            "value": field.value,
            "inline": field.inline,
        }
    
    async def __scape_user(self, user: discord.User | discord.Member) -> int:
        if not user.id in self.__users.keys():
            self.__users[user.id] = {
            "id": user.id,
            "name": user.name,
            "discriminator": user.discriminator,
            "display_name": user.display_name,
            "accent_color": user.accent_color.value if isinstance(user.accent_color, discord.Color) else user.accent_color,
            "avatar": await Scraper.__scrape_asset(user.avatar),
            "color": user.color.value if isinstance(user.color, discord.Color) else user.color,
            "created_at": user.created_at.timestamp(),
            "default_avatar": await Scraper.__scrape_asset(user.default_avatar),
            "display_avatar": await Scraper.__scrape_asset(user.display_avatar),
            "jump_url": user.jump_url,
            "public_flags": None,  # TODO: public_flags
        }
        return user.id

    @staticmethod
    async def __scrape_attachment(attachment: discord.Attachment) -> dict:
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
    
    @staticmethod
    async def __scape_sticker(sticker: discord.StickerItem) -> dict:
        return {
            "format": str(sticker.format),
            "id": sticker.id,
            "name": sticker.name,
            "url": sticker.url
        }
    
    @staticmethod
    async def __scrape_reactions(reaction: discord.Reaction) -> dict:
        return {
            "count": reaction.count,
            "emoji": str(reaction.emoji),  # TODO: Union[Emoji, PartialEmoji, str]
            "me": reaction.me,
        }
    
    @staticmethod
    async def __scrape_asset(asset: discord.Asset) -> dict:
        return {
            "key": asset.key,
            "url": asset.url
        }
