# ScrapeCord

## Root Keys
- `id`: channel id
- `name` channel namee
- `topic`: channel topic
- `type`: channel type
- `guild_id`: guild id
- `position`: channel position
- `messages`: array of messages (see Message Keys)
- `nsfw`: is nsfw
- `jump_url`: jump url
- `slowmode_delay`: slowmode delay
- `category_id`: category id
- `created_at`: created at unix timestamp

## Message Keys
- `id`: message id
- `content`: message content
- `author`: message author (see User Keys)
- `created_at`: created at unix timestamp
- `edited_at`: edited at unix timestamp or null
- `pinned`: is pinned
- `tts`: is tts
- `type`: message type
- `embeds`: array of embeds (see Embed Keys)
- `attachments`: array of attachments (see Attachment Keys)
- `reactions`: array of reactions (see Reaction Keys)
- `mentions_everyone`: if message mentions everyone
- `mentions`: array of mentions (see User Keys)
- `webhook_id`: webhook id or null
- `flags`: message flags (see Message Flags)
- `stickers`: array of stickers (see Sticker Keys)
- `clean_content`: message content with mentions removed i guess
- `is_system`: is system message
- `system_content`: system message content
- `components`: array of components (see Component Keys)

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

## Embed Keys
TODO

## Attachment Keys
TODO

## Reaction Keys
- `count`: reaction count
- `me`: if user/bot reacted
- `emoji`: emoji (see Emoji Keys)

## Message Flags
All Booleans
- `crossposted`:  if the message is the original crossposted message
- `is_crosspost`:  if the message was crossposted from another channel
- `suppress_embeds`:  if the message's embeds have been suppressed
- `source_message_deleted`:  if the source message for this crosspost has been deleted
- `urgent`: if message source is urgent (discord system or discord Trust and Safety)
- `has_thread`: if message is associated with a thread
- `ephemeral`: if message is ephemeral
- `loading`: if usersees a 'thinking' state
- `failed_to_mention_some_roles_in_thread`: if some roles are failed to mention in a thread 
- `suppress_notifications`: if the source message does not trigger push and desktop notifications

## Sticker Keys
TODO

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

### Select Menu Keys
- `custom_id`: custom id or null
- `disabled`: if disabled
- `channel_types`: TODO
- `max_values`: max values (int)
- `min_values`: min values (int)
- `options`: TODO

## Asset Keys
TODO

## Emoji Keys
TODO
