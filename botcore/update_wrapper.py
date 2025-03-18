class User:
    def __init__(self, user_data: dict):
        self.id = user_data.get("id")
        self.is_bot = user_data.get("is_bot")
        self.first_name = user_data.get("first_name")
        self.last_name = user_data.get("last_name")
        self.username = user_data.get("username")
        self.language_code = user_data.get("language_code")

    def __str__(self):
        return (
            f"User(\n"
            f"    id={self.id},\n"
            f"    is_bot={self.is_bot},\n"
            f"    first_name={self.first_name},\n"
            f"    last_name={self.last_name},\n"
            f"    username={self.username},\n"
            f"    language_code={self.language_code}\n"
            f")"
        )

class Chat:
    def __init__(self, chat_data: dict):
        self.id = chat_data.get("id")
        self.type = chat_data.get("type")
        self.title = chat_data.get("title")
        self.username = chat_data.get("username")
        self.photo = chat_data.get("photo")
        self.description = chat_data.get("description")
        self.invite_link = chat_data.get("invite_link")
        self.permissions = chat_data.get("permissions")

    def __str__(self):
        return (
            f"Chat(\n"
            f"    id={self.id},\n"
            f"    type={self.type},\n"
            f"    title={self.title},\n"
            f"    username={self.username},\n"
            f"    photo={self.photo},\n"
            f"    description={self.description},\n"
            f"    invite_link={self.invite_link},\n"
            f"    permissions={self.permissions}\n"
            f")"
        )

class ChatMember:
    def __init__(self, chat_member_data: dict):
        self.user = User(chat_member_data.get("user", {}))
        self.status = chat_member_data.get("status")
        self.custom_title = chat_member_data.get("custom_title")
        self.until_date = chat_member_data.get("until_date")
        self.can_be_edited = chat_member_data.get("can_be_edited")
        self.can_post_messages = chat_member_data.get("can_post_messages")
        self.can_edit_messages = chat_member_data.get("can_edit_messages")
        self.can_delete_messages = chat_member_data.get("can_delete_messages")
        self.can_restrict_members = chat_member_data.get("can_restrict_members")
        self.can_promote_members = chat_member_data.get("can_promote_members")
        self.can_change_info = chat_member_data.get("can_change_info")
        self.can_invite_users = chat_member_data.get("can_invite_users")
        self.can_pin_messages = chat_member_data.get("can_pin_messages")
        self.is_member = chat_member_data.get("is_member")
        self.can_send_messages = chat_member_data.get("can_send_messages")
        self.can_send_media_messages = chat_member_data.get("can_send_media_messages")
        self.can_send_polls = chat_member_data.get("can_send_polls")
        self.can_send_other_messages = chat_member_data.get("can_send_other_messages")
        self.can_add_web_page_previews = chat_member_data.get("can_add_web_page_previews")

    def __str__(self):
        return (
            f"ChatMember(\n"
            f"    user={self.user},\n"
            f"    status={self.status},\n"
            f"    custom_title={self.custom_title},\n"
            f"    until_date={self.until_date},\n"
            f"    can_be_edited={self.can_be_edited},\n"
            f"    can_post_messages={self.can_post_messages},\n"
            f"    can_edit_messages={self.can_edit_messages},\n"
            f"    can_delete_messages={self.can_delete_messages},\n"
            f"    can_restrict_members={self.can_restrict_members},\n"
            f"    can_promote_members={self.can_promote_members},\n"
            f"    can_change_info={self.can_change_info},\n"
            f"    can_invite_users={self.can_invite_users},\n"
            f"    can_pin_messages={self.can_pin_messages},\n"
            f"    is_member={self.is_member},\n"
            f"    can_send_messages={self.can_send_messages},\n"
            f"    can_send_media_messages={self.can_send_media_messages},\n"
            f"    can_send_polls={self.can_send_polls},\n"
            f"    can_send_other_messages={self.can_send_other_messages},\n"
            f"    can_add_web_page_previews={self.can_add_web_page_previews}\n"
            f")"
        )

class PhotoSize:
    def __init__(self, photo_data: dict):
        self.file_id = photo_data.get("file_id")
        self.file_unique_id = photo_data.get("file_unique_id")
        self.width = photo_data.get("width")
        self.height = photo_data.get("height")
        self.file_size = photo_data.get("file_size")

    def __str__(self):
        return (
            f"PhotoSize(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    width={self.width},\n"
            f"    height={self.height},\n"
            f"    file_size={self.file_size}\n"
            f")"
        )

class Audio:
    def __init__(self, audio_data: dict):
        self.file_id = audio_data.get("file_id")
        self.file_unique_id = audio_data.get("file_unique_id")
        self.duration = audio_data.get("duration")
        self.performer = audio_data.get("performer")
        self.title = audio_data.get("title")
        self.file_name = audio_data.get("file_name")
        self.mime_type = audio_data.get("mime_type")
        self.file_size = audio_data.get("file_size")
        self.thumbnail = PhotoSize(audio_data.get("thumbnail", {})) if audio_data.get("thumbnail") else None

    def __str__(self):
        return (
            f"Audio(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    duration={self.duration},\n"
            f"    performer={self.performer},\n"
            f"    title={self.title},\n"
            f"    file_name={self.file_name},\n"
            f"    mime_type={self.mime_type},\n"
            f"    file_size={self.file_size},\n"
            f"    thumbnail={self.thumbnail}\n"
            f")"
        )

class Document:
    def __init__(self, document_data: dict):
        self.file_id = document_data.get("file_id")
        self.file_unique_id = document_data.get("file_unique_id")
        self.file_name = document_data.get("file_name")
        self.mime_type = document_data.get("mime_type")
        self.file_size = document_data.get("file_size")
        self.thumbnail = PhotoSize(document_data.get("thumbnail", {})) if document_data.get("thumbnail") else None

    def __str__(self):
        return (
            f"Document(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    file_name={self.file_name},\n"
            f"    mime_type={self.mime_type},\n"
            f"    file_size={self.file_size},\n"
            f"    thumbnail={self.thumbnail}\n"
            f")"
        )

class Voice:
    def __init__(self, voice_data: dict):
        self.file_id = voice_data.get("file_id")
        self.file_unique_id = voice_data.get("file_unique_id")
        self.duration = voice_data.get("duration")
        self.mime_type = voice_data.get("mime_type")
        self.file_size = voice_data.get("file_size")

    def __str__(self):
        return (
            f"Voice(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    duration={self.duration},\n"
            f"    mime_type={self.mime_type},\n"
            f"    file_size={self.file_size}\n"
            f")"
        )

class Location:
    def __init__(self, location_data: dict):
        self.longitude = location_data.get("longitude")
        self.latitude = location_data.get("latitude")
        self.horizontal_accuracy = location_data.get("horizontal_accuracy")
        self.live_period = location_data.get("live_period")
        self.heading = location_data.get("heading")
        self.proximity_alert_radius = location_data.get("proximity_alert_radius")

    def __str__(self):
        return (
            f"Location(\n"
            f"    longitude={self.longitude},\n"
            f"    latitude={self.latitude},\n"
            f"    horizontal_accuracy={self.horizontal_accuracy},\n"
            f"    live_period={self.live_period},\n"
            f"    heading={self.heading},\n"
            f"    proximity_alert_radius={self.proximity_alert_radius}\n"
            f")"
        )

class Invoice:
    def __init__(self, invoice_data: dict):
        self.title = invoice_data.get("title")
        self.description = invoice_data.get("description")
        self.start_parameter = invoice_data.get("start_parameter")
        self.currency = invoice_data.get("currency")
        self.total_amount = invoice_data.get("total_amount")

    def __str__(self):
        return (
            f"Invoice(\n"
            f"    title={self.title},\n"
            f"    description={self.description},\n"
            f"    start_parameter={self.start_parameter},\n"
            f"    currency={self.currency},\n"
            f"    total_amount={self.total_amount}\n"
            f")"
        )

class Sticker:
    def __init__(self, sticker_data: dict):
        self.file_id = sticker_data.get("file_id")
        self.file_unique_id = sticker_data.get("file_unique_id")
        self.width = sticker_data.get("width")
        self.height = sticker_data.get("height")
        self.is_animated = sticker_data.get("is_animated")
        self.is_video = sticker_data.get("is_video")
        self.emoji = sticker_data.get("emoji")
        self.set_name = sticker_data.get("set_name")
        self.mask_position = sticker_data.get("mask_position")
        self.file_size = sticker_data.get("file_size")
        self.thumbnail = PhotoSize(sticker_data.get("thumbnail", {})) if sticker_data.get("thumbnail") else None

    def __str__(self):
        return (
            f"Sticker(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    width={self.width},\n"
            f"    height={self.height},\n"
            f"    is_animated={self.is_animated},\n"
            f"    is_video={self.is_video},\n"
            f"    emoji={self.emoji},\n"
            f"    set_name={self.set_name},\n"
            f"    mask_position={self.mask_position},\n"
            f"    file_size={self.file_size},\n"
            f"    thumbnail={self.thumbnail}\n"
            f")"
        )

class CallbackQuery:
    def __init__(self, callback_query_data: dict):
        self.id = callback_query_data.get("id")
        self.from_user = User(callback_query_data.get("from", {}))
        self.message = Message(callback_query_data.get("message", {})) if callback_query_data.get("message") else None
        self.inline_message_id = callback_query_data.get("inline_message_id")
        self.chat_instance = callback_query_data.get("chat_instance")
        self.data = callback_query_data.get("data")
        self.game_short_name = callback_query_data.get("game_short_name")

    def __str__(self):
        return (
            f"CallbackQuery(\n"
            f"    id={self.id},\n"
            f"    from_user={self.from_user},\n"
            f"    message={self.message},\n"
            f"    inline_message_id={self.inline_message_id},\n"
            f"    chat_instance={self.chat_instance},\n"
            f"    data={self.data},\n"
            f"    game_short_name={self.game_short_name}\n"
            f")"
        )

class Message:
    def __init__(self, message_data: dict):
        self.message_id = message_data.get("message_id")
        self.from_user = User(message_data.get("from", {})) if message_data.get("from") else None
        self.date = message_data.get("date")
        self.chat = Chat(message_data.get("chat", {}))
        self.text = message_data.get("text")
        self.caption = message_data.get("caption")
        self.audio = Audio(message_data.get("audio", {})) if message_data.get("audio") else None
        self.document = Document(message_data.get("document", {})) if message_data.get("document") else None
        self.photo = [PhotoSize(photo) for photo in message_data.get("photo", [])] if message_data.get("photo") else None
        self.voice = Voice(message_data.get("voice", {})) if message_data.get("voice") else None
        self.location = Location(message_data.get("location", {})) if message_data.get("location") else None
        self.reply_to_message = Message(message_data.get("reply_to_message", {})) if message_data.get("reply_to_message") else None
        self.invoice = Invoice(message_data.get("invoice", {})) if message_data.get("invoice") else None
        self.sticker = Sticker(message_data.get("sticker", {})) if message_data.get("sticker") else None

    def __str__(self):
        return (
            f"Message(\n"
            f"    message_id={self.message_id},\n"
            f"    from_user={self.from_user},\n"
            f"    date={self.date},\n"
            f"    chat={self.chat},\n"
            f"    text={self.text},\n"
            f"    caption={self.caption},\n"
            f"    audio={self.audio},\n"
            f"    document={self.document},\n"
            f"    photo={self.photo},\n"
            f"    voice={self.voice},\n"
            f"    location={self.location},\n"
            f"    reply_to_message={self.reply_to_message},\n"
            f"    invoice={self.invoice},\n"
            f"    sticker={self.sticker}\n"
            f")"
        )

class UpdateWrapper:
    def __init__(self, update: dict):
        self.update = update
        self.update_id = update.get("update_id")
        self.message = Message(update.get("message", {})) if update.get("message") else None
        self.callback_query = CallbackQuery(update.get("callback_query", {})) if update.get("callback_query") else None

    def __str__(self):
        return (
            f"UpdateWrapper(\n"
            f"    update_id={self.update_id},\n"
            f"    message={self.message},\n"
            f"    callback_query={self.callback_query}\n"
            f")"
        )