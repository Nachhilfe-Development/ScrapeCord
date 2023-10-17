# ScrapeCord

## Root Keys
- `id`: channel id
- `name` channel name
- `topic`: channel topic
- `type`: channel type
- `guild_id`: guild id
- `position`: channel position
- `messages`: array of messages (see Message Keys)
- `nsfw`: is nsfw
- `jump_url`: jump url
- `slowmode_delay`: slow-mode delay
- `category_id`: category id
- `created_at`: created at unix timestamp
- `users`: Map\[UserID, User Keys\] (see User Keys)
- `roles`: Map\[RoleID, Role Keys\] (see Role Keys)

## Message Keys
- `id`: message id
- `content`: message content
- `author`: message author id
- `edited_at`: edited at unix timestamp or null
- `pinned`: is pinned
- `tts`: is tts
- `type`: message type
- `embeds`: array of embeds (see Embed Keys)
- `attachments`: array of attachments (see Attachment Keys)
- `reactions`: array of reactions (see Reaction Keys)
- `mentions_everyone`: if message mentions everyone
- `mentions`: array of mentioned user ids
- `webhook_id`: webhook id or null
- `flags`: message flags (see Message Flags)
- `stickers`: array of stickers (see Sticker Keys)
- `clean_content`: message content with mentions removed I guess
- `is_system`: is system message
- `system_content`: system message content
- `components`: array of components (see Component Keys)
- `referenced_message`: referenced message or null (see Message Reference Keys)

## User Keys
- `id`: user id
- `name`: username
- `discriminator`: discriminator
- `display_name`: display name
- `accent_color`: accent color (integer)
- `avatar`: avatar (see Asset Keys)
- `color`: color (integer)
- `created_at`: created at unix timestamp
- `default_avatar`: default avatar (see Asset Keys)
- `display_avatar`: display avatar (see Asset Keys)
- `jump_url`: jump url
- `public_flags`: null -> TODO
- `roles`: list of role ids that the user has

## Embed Keys
- `title`: title
- `description`: description or null
- `color`: color (integer)
- `fields`: array of fields (see Embed Field Keys)
- `footer`: footer (see Embed Footer Keys)
- `image`: image (see Embed Media Keys)
- `thumbnail`: thumbnail (see Embed Media Keys)
- `timestamp`: unix timestamp or null
- `type`: embed type -> "rich", "image", "video", "gifv", "article", "link", "auto_moderation_message"
- `url`: url or null
- `video`: video (see Embed Media Keys)

### Embed Field Keys
- `name`: name
- `value`: value
- `inline`: if inline

### Embed Footer Keys
- `icon_url`: icon url or null
- `proxy_icon_url`: proxy icon url or null
- `text`: text or null

### Embed Media Keys
- `height`: height (int)
- `proxy_url`: proxy url
- `url`: url
- `width`: width (int)

## Attachment Keys
- `content_type`: media type https://en.wikipedia.org/wiki/Media_type
- `ephemeral`: if ephemeral
- `description`: attachments description
- `is_spoiler`: if the attachment contains spoiler
- `filename`: filename
- `height`: height (int)
- `id`: attachment id (int)
- `proxy_url`: proxy url
- `size`: size in bytes (int)
- `url`: url
- `width`: width (int)

## Reaction Keys
- `count`: reaction count
- `me`: if user/bot reacted
- `emoji`: emoji (see Emoji Keys)

## Message Flags
All Booleans
- `crossposted`:  if the message is the original cross-posted message
- `is_crosspost`:  if the message was cross-posted from another channel
- `suppress_embeds`:  if the message's embeds have been suppressed
- `source_message_deleted`:  if the source message for this cross post has been deleted
- `urgent`: if message source is urgent (discord system or discord Trust and Safety)
- `has_thread`: if message is associated with a thread
- `ephemeral`: if message is ephemeral
- `loading`: if user sees a 'thinking' state
- `failed_to_mention_some_roles_in_thread`: if some roles are failed to mention in a thread 
- `suppress_notifications`: if the source message does not trigger push and desktop notifications

## Sticker Keys
- `format`: the format for the sticker's image
- `id`: the id of the sticker (int)
- `name`: the name of the sticker (str)
- `url`: the url of the sticker's image

## Component Keys
- `type`: component type (`action_row`, `button`, `select_menu`)

### Action Row Keys
- `children`: array of components (see Component Keys)

### Button Keys
- `custom_id`: custom id or null
- `disabled`: if disabled
- `emoji`: emoji (see Emoji Keys)
- `url`: url or null
- `label`: label or null
- `style`: See Button Style 
#### Button Style
- primary = 1
- secondary = 2
- success = 3
- danger = 4
- link = 5

### Select Menu Keys
- `custom_id`: custom id or null
- `disabled`: if disabled
- `channel_types`: TODO
- `max_values`: max values (int)
- `min_values`: min values (int)
- `options`: array of options (see Select Option Keys)

#### Select Option Keys
- `label`: label
- `value`: value
- `description`: description or null
- `default`: if default

## Asset Keys
- `key`: asset key -> identifier
- `url`: asset url

## Emoji Keys
TODO

## Message Reference Keys
- `channel_id`: channel id
- `guild_id`: guild id or null
- `message_id`: message id or null
- `fail_if_not_exists`: if fail the message does not exist / could not be found
- `jump_url`: jump url

## Role Keys
- `color`: the color of the role
- `id`: the role id
- `name`: the name of the role
- `position`: the position of the role
- `mentionable`: if the role can be mentioned by users
- `hoist`: Indicates if the role will be displayed separately from other members
- `icon`: the icon (see Asset Keys) or null
- `unicode_emoji`: the unicode emoji as string or null
