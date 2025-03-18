import aiohttp
import asyncio
from typing import Callable, Optional, Dict, Any, List, Union
from .filter import Filters
from .update_wrapper import UpdateWrapper
from collections import defaultdict
from .InlineKeyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .filter import Filters

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

class File:
    def __init__(self, file_data: dict):
        self.file_id = file_data.get("file_id")
        self.file_unique_id = file_data.get("file_unique_id")
        self.file_size = file_data.get("file_size")
        self.file_path = file_data.get("file_path")

    def __str__(self):
        return (
            f"File(\n"
            f"    file_id={self.file_id},\n"
            f"    file_unique_id={self.file_unique_id},\n"
            f"    file_size={self.file_size},\n"
            f"    file_path={self.file_path}\n"
            f")"
        )

class CopyTextButton:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {
            "text": self.text,
            "callback_data": f"copy:{self.text}"
        }

class ChatPhoto:
    def __init__(self, small_file_id: str, big_file_id: str):
        self.small_file_id = small_file_id
        self.big_file_id = big_file_id

    def to_dict(self):
        return {
            "small_file_id": self.small_file_id,
            "big_file_id": self.big_file_id
        }

class InputMedia:
    def __init__(self, type: str, media: str, caption: str = None, parse_mode: str = None):
        self.type = type
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode

    def to_dict(self):
        data = {
            "type": self.type,
            "media": self.media
        }
        if self.caption:
            data["caption"] = self.caption
        if self.parse_mode:
            data["parse_mode"] = self.parse_mode
        return data

class InputMediaPhoto(InputMedia):
    def __init__(self, media: str, caption: str = None, parse_mode: str = None):
        super().__init__("photo", media, caption, parse_mode)

class InputMediaVideo(InputMedia):
    def __init__(self, media: str, caption: str = None, parse_mode: str = None, width: int = None, height: int = None, duration: int = None):
        super().__init__("video", media, caption, parse_mode)
        self.width = width
        self.height = height
        self.duration = duration

    def to_dict(self):
        data = super().to_dict()
        if self.width:
            data["width"] = self.width
        if self.height:
            data["height"] = self.height
        if self.duration:
            data["duration"] = self.duration
        return data

class InputMediaAnimation(InputMedia):
    def __init__(self, media: str, caption: str = None, parse_mode: str = None, duration: int = None, width: int = None, height: int = None):
        super().__init__("animation", media, caption, parse_mode)
        self.duration = duration
        self.width = width
        self.height = height

    def to_dict(self):
        data = super().to_dict()
        if self.duration:
            data["duration"] = self.duration
        if self.width:
            data["width"] = self.width
        if self.height:
            data["height"] = self.height
        return data

class InputMediaAudio(InputMedia):
    def __init__(self, media: str, caption: str = None, parse_mode: str = None, duration: int = None, performer: str = None, title: str = None):
        super().__init__("audio", media, caption, parse_mode)
        self.duration = duration
        self.performer = performer
        self.title = title

    def to_dict(self):
        data = super().to_dict()
        if self.duration:
            data["duration"] = self.duration
        if self.performer:
            data["performer"] = self.performer
        if self.title:
            data["title"] = self.title
        return data

class InputMediaDocument(InputMedia):
    def __init__(self, media: str, caption: str = None, parse_mode: str = None, disable_content_type_detection: bool = None):
        super().__init__("document", media, caption, parse_mode)
        self.disable_content_type_detection = disable_content_type_detection

    def to_dict(self):
        data = super().to_dict()
        if self.disable_content_type_detection is not None:
            data["disable_content_type_detection"] = self.disable_content_type_detection
        return data

class InputFile:
    def __init__(self, file_path: str, file_name: str = None, mime_type: str = None):
        self.file_path = file_path
        self.file_name = file_name
        self.mime_type = mime_type

    def to_dict(self):
        data = {
            "file_path": self.file_path
        }
        if self.file_name:
            data["file_name"] = self.file_name
        if self.mime_type:
            data["mime_type"] = self.mime_type
        return data

class MainBot:
    def __init__(self, Token: str, url: str, concurrency_limit: int = None, proxy: str = None):
        self.token = Token
        self.base_url = url
        self.handlers: List[Dict] = []
        self.callback_handlers: List[Dict] = []
        self.running = asyncio.Event()
        self.user_states: Dict[str, Dict[int, str]] = {}
        self.filters = Filters(self)
        self.initialize_handlers: List[Callable] = []
        self.concurrency_limit = concurrency_limit
        self.active_tasks = set()
        self.proxy = proxy

    class ChatParameter:
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
                f"ChatParameter(\n"
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

    async def get_chat(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/getChat"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()
                if response_data.get("ok"):
                    return self.ChatParameter(response_data["result"])
                else:
                    return None

    def set_user_state(self, user_id: int, state: str):
        if self.token not in self.user_states:
            self.user_states[self.token] = {}
        self.user_states[self.token][user_id] = state

    def get_user_state(self, user_id: int) -> str:
        if self.token in self.user_states and user_id in self.user_states[self.token]:
            return self.user_states[self.token][user_id]
        return None

    def clear_user_state(self, user_id: int):
        if self.token in self.user_states and user_id in self.user_states[self.token]:
            del self.user_states[self.token][user_id]

    def Message(self, _filter: Filters):
        def decorator(func: Callable):
            self.handlers.append({"filter": _filter, "func": func})
            return func
        return decorator

    async def get_me(self):
        url = f"{self.base_url}/bot{self.token}/getMe"
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_updates(self, offset=None, timeout=30):
        url = f"{self.base_url}/bot{self.token}/getUpdates"
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, proxy=self.proxy) as response:
                    if response.status != 200:
                        print(f"HTTP Error: {response.status}")
                        return None

                    response_data = await response.json()

                    if response_data is None:
                        print("Empty response from server")
                        return None

                    if not isinstance(response_data, dict) or "ok" not in response_data:
                        print("Invalid response format")
                        return None

                    if not response_data.get("ok"):
                        print(f"API Error: {response_data.get('description', 'Unknown error')}")
                        return None

                    return response_data.get("result", [])
        except Exception as e:
            print(f"An error occurred in get_updates: {e}")
            return None

    async def process_updates(self):
        offset = None
        while self.running.is_set():
            try:
                updates = await self.get_updates(offset=offset)
                if updates is None:
                    print("No updates received or invalid response.")
                    continue
                for update in updates:
                    offset = update["update_id"] + 1
                    update_wrapper = UpdateWrapper(update)
                    if self.concurrency_limit is not None and len(self.active_tasks) >= self.concurrency_limit:
                        print("Concurrency limit reached, skipping update.")
                        continue
                    task = asyncio.create_task(self._process_update(update_wrapper))
                    self.active_tasks.add(task)
                    task.add_done_callback(self.active_tasks.discard)
            except Exception as e:
                print(f"An error occurred in process_updates: {e}")

    async def _process_update(self, update_wrapper):
        try:
            if update_wrapper is None or update_wrapper.message is None:
                print("Invalid update or message is None.")
                return

            user_id = update_wrapper.message.from_user.id
            current_state = self.get_user_state(user_id)
            handled = False

            for handler in self.handlers:
                if handler["filter"](update_wrapper.update):
                    await handler["func"](
                        self, 
                        update_wrapper.update, 
                        update_wrapper.update, 
                        update_wrapper.message,
                        User=User,
                        File=File
                    )
                    handled = True
                    break

            if not handled:
                self.clear_user_state(user_id)

        except Exception as e:
            print(f"An error occurred in _process_update: {e}")

    def Initialize(self):
        def decorator(func: Callable):
            self.initialize_handlers.append(func)
            return func
        return decorator

    async def run_initialize_handlers(self):
        for handler in self.initialize_handlers:
            await handler(self)

    async def start(self):
        self.running.set()
        try:
            bot_info = await self.get_me()
            if bot_info.get("ok"):
                print(f"Bot is running! Username: @{bot_info['result']['username']}")
            else:
                print("Failed to start the bot. Please check your token and API URL.")
                return
        except Exception as e:
            print(f"An error occurred while starting the bot: {e}")
            return

        await self.run_initialize_handlers()
        await self.process_updates()

    async def stop(self):
        self.running.clear()
        print("Bot has been stopped.")

    async def delete_message_auto(self, message: dict):
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        return await self.delete_message(chat_id=chat_id, message_id=message_id)

    async def edit_message_text_auto(self, message: dict, text: str, reply_markup=None):
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        return await self.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    async def edit_message_caption_auto(
        self,
        chat_id: int,
        message_id: int,
        caption: str,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/editMessageCaption"
        params = {"chat_id": chat_id, "message_id": message_id, "caption": caption}
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def schedule_message(
        self,
        chat_id: int,
        text: str,
        delay_seconds: int,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
    ):
        await asyncio.sleep(delay_seconds)
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
        )

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
        edit_message_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        params = {"chat_id": chat_id, "text": text}
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        url = f"{self.base_url}/bot{self.token}/sendMessage"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_animation(
        self,
        chat_id: int,
        animation: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendAnimation"
        params = {"chat_id": chat_id, "animation": animation}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_audio(
        self,
        chat_id: int,
        audio: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendAudio"
        params = {"chat_id": chat_id, "audio": audio}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_contact(
        self,
        chat_id: int,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendContact"
        params = {"chat_id": chat_id, "phone_number": phone_number, "first_name": first_name}
        if last_name:
            params["last_name"] = last_name
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_document(
        self,
        chat_id: int,
        document: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendDocument"
        params = {"chat_id": chat_id, "document": document}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_location(
        self,
        chat_id: int,
        latitude: float,
        longitude: float,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendLocation"
        params = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude}
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_media_group(
        self,
        chat_id: int,
        media: List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaAudio, InputMediaDocument]],
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendMediaGroup"
        params = {
            "chat_id": chat_id,
            "media": [m.to_dict() for m in media]
        }
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                return await response.json()

    async def send_input_file(
        self,
        chat_id: int,
        input_file: InputFile,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendDocument"
        params = {
            "chat_id": chat_id,
            "document": input_file.to_dict()
        }
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                return await response.json()

    async def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
    ):
        if edit_message_id:
            return await self.edit_message_caption(chat_id=chat_id, message_id=edit_message_id, caption=caption, reply_markup=reply_markup)
        else:
            url = f"{self.base_url}/bot{self.token}/sendPhoto"
            params = {"chat_id": chat_id, "photo": photo}
            if caption:
                params["caption"] = caption
            if reply_to_message_id:
                params["reply_to_message_id"] = reply_to_message_id
            if reply_markup:
                params["reply_markup"] = reply_markup
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=params, proxy=self.proxy) as response:
                    response_data = await response.json()

    async def send_video(
        self,
        chat_id: int,
        video: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendVideo"
        params = {"chat_id": chat_id, "video": video}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_voice(
        self,
        chat_id: int,
        voice: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendVoice"
        params = {"chat_id": chat_id, "voice": voice}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_sticker(
        self,
        chat_id: int,
        sticker: str,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendSticker"
        params = {"chat_id": chat_id, "sticker": sticker}
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def send_chat_action(self, chat_id: int, action: str):
        url = f"{self.base_url}/bot{self.token}/sendChatAction"
        params = {"chat_id": chat_id, "action": action}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/editMessageText"
        params = {"chat_id": chat_id, "message_id": message_id, "text": text}
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def delete_message(self, chat_id: int, message_id: int):
        url = f"{self.base_url}/bot{self.token}/deleteMessage"
        params = {"chat_id": chat_id, "message_id": message_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def forward_message(
        self,
        chat_id: int,
        from_chat_id: int,
        message_id: int,
    ):
        url = f"{self.base_url}/bot{self.token}/forwardMessage"
        params = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def get_chat_administrators(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/getChatAdministrators"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def get_chat_member(self, chat_id: int, user_id: int):
        url = f"{self.base_url}/bot{self.token}/getChatMember"
        params = {"chat_id": chat_id, "user_id": user_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def get_chat_members_count(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/getChatMembersCount"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def get_file(self, file_id: str):
        url = f"{self.base_url}/bot{self.token}/getFile"
        params = {"file_id": file_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def get_sticker_set(self, name: str):
        url = f"{self.base_url}/bot{self.token}/getStickerSet"
        params = {"name": name}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def invite_user(self, chat_id: int, user_id: int):
        url = f"{self.base_url}/bot{self.token}/inviteUser"
        params = {"chat_id": chat_id, "user_id": user_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def leave_chat(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/leaveChat"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def promote_chat_member(
        self,
        chat_id: int,
        user_id: int,
        can_change_info: bool = None,
        can_post_messages: bool = None,
        can_edit_messages: bool = None,
        can_delete_messages: bool = None,
        can_invite_users: bool = None,
        can_restrict_members: bool = None,
        can_pin_messages: bool = None,
        can_promote_members: bool = None,
    ):
        url = f"{self.base_url}/bot{self.token}/promoteChatMember"
        params = {"chat_id": chat_id, "user_id": user_id}
        if can_change_info is not None:
            params["can_change_info"] = can_change_info
        if can_post_messages is not None:
            params["can_post_messages"] = can_post_messages
        if can_edit_messages is not None:
            params["can_edit_messages"] = can_edit_messages
        if can_delete_messages is not None:
            params["can_delete_messages"] = can_delete_messages
        if can_invite_users is not None:
            params["can_invite_users"] = can_invite_users
        if can_restrict_members is not None:
            params["can_restrict_members"] = can_restrict_members
        if can_pin_messages is not None:
            params["can_pin_messages"] = can_pin_messages
        if can_promote_members is not None:
            params["can_promote_members"] = can_promote_members
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def set_chat_photo(self, chat_id: int, photo: str):
        url = f"{self.base_url}/bot{self.token}/setChatPhoto"
        params = {"chat_id": chat_id, "photo": photo}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def unban_chat_member(self, chat_id: int, user_id: int):
        url = f"{self.base_url}/bot{self.token}/unbanChatMember"
        params = {"chat_id": chat_id, "user_id": user_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def copy_message(
        self,
        chat_id: int,
        from_chat_id: int,
        message_id: int,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/copyMessage"
        params = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id}
        if caption:
            params["caption"] = caption
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        png_sticker: str,
        emojis: str,
        mask_position: dict = None,
    ):
        url = f"{self.base_url}/bot{self.token}/addStickerToSet"
        params = {"user_id": user_id, "name": name, "png_sticker": png_sticker, "emojis": emojis}
        if mask_position:
            params["mask_position"] = mask_position
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        png_sticker: str,
        emojis: str,
        contains_masks: bool = None,
        mask_position: dict = None,
    ):
        url = f"{self.base_url}/bot{self.token}/createNewStickerSet"
        params = {"user_id": user_id, "name": name, "title": title, "png_sticker": png_sticker, "emojis": emojis}
        if contains_masks is not None:
            params["contains_masks"] = contains_masks
        if mask_position:
            params["mask_position"] = mask_position
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def upload_sticker_file(self, user_id: int, png_sticker: str):
        url = f"{self.base_url}/bot{self.token}/uploadStickerFile"
        params = {"user_id": user_id, "png_sticker": png_sticker}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def create_chat_invite_link(
        self,
        chat_id: int,
        expire_date: int = None,
        member_limit: int = None,
    ):
        url = f"{self.base_url}/bot{self.token}/createChatInviteLink"
        params = {"chat_id": chat_id}
        if expire_date:
            params["expire_date"] = expire_date
        if member_limit:
            params["member_limit"] = member_limit
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def delete_chat_photo(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/deleteChatPhoto"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def delete_sticker_from_set(self, sticker: str):
        url = f"{self.base_url}/bot{self.token}/deleteStickerFromSet"
        params = {"sticker": sticker}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def edit_message_caption(
        self,
        chat_id: int,
        message_id: int,
        caption: str,
        reply_markup=None,
    ):
        url = f"{self.base_url}/bot{self.token}/editMessageCaption"
        params = {"chat_id": chat_id, "message_id": message_id, "caption": caption}
        if reply_markup:
            params["reply_markup"] = reply_markup
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def export_chat_invite_link(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/exportChatInviteLink"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def pin_chat_message(
        self,
        chat_id: int,
        message_id: int,
        disable_notification: bool = None,
    ):
        url = f"{self.base_url}/bot{self.token}/pinChatMessage"
        params = {"chat_id": chat_id, "message_id": message_id}
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def restrict_chat_member(
        self,
        chat_id: int,
        user_id: int,
        until_date: int = None,
        can_send_messages: bool = None,
        can_send_media_messages: bool = None,
        can_send_other_messages: bool = None,
        can_add_web_page_previews: bool = None,
    ):
        url = f"{self.base_url}/bot{self.token}/restrictChatMember"
        params = {"chat_id": chat_id, "user_id": user_id}
        if until_date:
            params["until_date"] = until_date
        if can_send_messages is not None:
            params["can_send_messages"] = can_send_messages
        if can_send_media_messages is not None:
            params["can_send_media_messages"] = can_send_media_messages
        if can_send_other_messages is not None:
            params["can_send_other_messages"] = can_send_other_messages
        if can_add_web_page_previews is not None:
            params["can_add_web_page_previews"] = can_add_web_page_previews
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: str):
        url = f"{self.base_url}/bot{self.token}/revokeChatInviteLink"
        params = {"chat_id": chat_id, "invite_link": invite_link}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def set_chat_description(self, chat_id: int, description: str):
        url = f"{self.base_url}/bot{self.token}/setChatDescription"
        params = {"chat_id": chat_id, "description": description}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def set_chat_title(self, chat_id: int, title: str):
        url = f"{self.base_url}/bot{self.token}/setChatTitle"
        params = {"chat_id": chat_id, "title": title}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def unpin_all_chat_messages(self, chat_id: int):
        url = f"{self.base_url}/bot{self.token}/unpinAllChatMessages"
        params = {"chat_id": chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def unpin_chat_message(self, chat_id: int, message_id: int = None):
        url = f"{self.base_url}/bot{self.token}/unpinChatMessage"
        params = {"chat_id": chat_id}
        if message_id:
            params["message_id"] = message_id
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def reply_message_auto(self, update: dict, text: str, reply_markup=None):
        update_wrapper = UpdateWrapper(update)
        if update_wrapper.message:
            chat_id = update_wrapper.message.chat.id
            message_id = update_wrapper.message.message_id
            return await self.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=message_id,
                reply_markup=reply_markup,
            )
        return {"ok": False, "error": "Invalid update format"}

    async def reply_video_auto(self, update: dict, video: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_video(
            chat_id=chat_id,
            video=video,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_voice_auto(self, update: dict, voice: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_voice(
            chat_id=chat_id,
            voice=voice,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_sticker_auto(self, update: dict, sticker: str, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_document_auto(self, update: dict, document: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_document(
            chat_id=chat_id,
            document=document,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_animation_auto(self, update: dict, animation: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_animation(
            chat_id=chat_id,
            animation=animation,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_audio_auto(self, update: dict, audio: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_audio(
            chat_id=chat_id,
            audio=audio,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_photo_auto(self, update: dict, photo: str, caption: str = None, reply_markup=None):
        chat_id = update_wrapper.message.chat.id
        message_id = update_wrapper.message.message_id
        return await self.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_message(self, chat_id: int, text: str, message_id: int, reply_markup=None):
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_video(self, chat_id: int, video: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_video(
            chat_id=chat_id,
            video=video,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_voice(self, chat_id: int, voice: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_voice(
            chat_id=chat_id,
            voice=voice,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_sticker(self, chat_id: int, sticker: str, message_id: int, reply_markup=None):
        return await self.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_document(self, chat_id: int, document: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_document(
            chat_id=chat_id,
            document=document,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_animation(self, chat_id: int, animation: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_animation(
            chat_id=chat_id,
            animation=animation,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_audio(self, chat_id: int, audio: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_audio(
            chat_id=chat_id,
            audio=audio,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    async def reply_photo(self, chat_id: int, photo: str, message_id: int, caption: str = None, reply_markup=None):
        return await self.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    def CallbackQuery(self, _filter: Filters = None):
        if _filter is None:
            _filter = self.filters.callback_query_all()
        def decorator(func: Callable):
            self.callback_handlers.append({
                "filter": _filter, 
                "func": lambda bot, update: func(bot, update)
            })
            return func
        return decorator


    async def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False):
        url = f"{self.base_url}/bot{self.token}/answerCallbackQuery"
        params = {"callback_query_id": callback_query_id}
        if text:
            params["text"] = text
        if show_alert:
            params["show_alert"] = show_alert
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    def LabeledPrice(label: str, amount: int):
        def decorator(func):
            def wrapper(*args, **kwargs):
                prices = [
                    {"label": label, "amount": amount},
                ]
                return func(*args, prices=prices, **kwargs)
            return wrapper
        return decorator


    def PreCheckoutQuery(self):
        def decorator(func: Callable):
            self.callback_handlers.append({"filter": self.filters.pre_checkout_query(), "func": func})
            return func
        return decorator


    class SuccessfulPayment:
        def __init__(self, successful_payment_data: dict):
            self.currency = successful_payment_data.get("currency")
            self.total_amount = successful_payment_data.get("total_amount")
            self.invoice_payload = successful_payment_data.get("invoice_payload")
            self.telegram_payment_charge_id = successful_payment_data.get("telegram_payment_charge_id")

    async def send_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        prices: list,
        photo_url: str = None,
        reply_to_message_id: int = None,
    ):
        url = f"{self.base_url}/bot{self.token}/sendInvoice"
        params = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "prices": prices,
        }

        if photo_url:
            params["photo_url"] = photo_url
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: str = None,
    ):
        url = f"{self.base_url}/bot{self.token}/answerPreCheckoutQuery"
        params = {
            "pre_checkout_query_id": pre_checkout_query_id,
            "ok": ok,
        }
        if error_message:
            params["error_message"] = error_message

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, proxy=self.proxy) as response:
                response_data = await response.json()

class Chat:
    def __init__(self, chat_data: dict):
        self.id = chat_data.get("id")
        self.type = chat_data.get("type")

class Message:
    def __init__(self, message_data: dict):
        self.chat = Chat(message_data.get("chat", {}))
        self.message_id = message_data.get("message_id")
        self.text = message_data.get("text")
        self.data = message_data

class EvenBot(MainBot):
    def __init__(self, Token: str, url: str, bot_type: str = "telegram"):
        super().__init__(Token, url)
        self.bot_type = bot_type

    def set_user_state(self, user_id: int, state: str):
        return super().set_user_state(user_id, state)

    def get_user_state(self, user_id: int) -> str:
        return super().get_user_state(user_id)

    def clear_user_state(self, user_id: int):
        return super().clear_user_state(user_id)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            text = f"{text}"
        elif self.bot_type == "bale":
            text = f"{text}"
        return await super().send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_video(
        self,
        chat_id: int,
        video: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_video(
            chat_id=chat_id,
            video=video,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_audio(
        self,
        chat_id: int,
        audio: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_audio(
            chat_id=chat_id,
            audio=audio,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_document(
        self,
        chat_id: int,
        document: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_document(
            chat_id=chat_id,
            document=document,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_animation(
        self,
        chat_id: int,
        animation: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_animation(
            chat_id=chat_id,
            animation=animation,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_voice(
        self,
        chat_id: int,
        voice: str,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            caption = f"{caption}" if caption else None
        elif self.bot_type == "bale":
            caption = f"{caption}" if caption else None
        return await super().send_voice(
            chat_id=chat_id,
            voice=voice,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_sticker(
        self,
        chat_id: int,
        sticker: str,
        reply_to_message_id: int = None,
        reply_markup=None,
        edit_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            pass
        elif self.bot_type == "bale":
            pass
        return await super().send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            edit_message_id=edit_message_id,
            **kwargs
        )

    async def send_contact(
        self,
        chat_id: int,
        phone_number: str,
        first_name: str,
        reply_to_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            pass
        elif self.bot_type == "bale":
            pass
        return await super().send_contact(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )

    async def send_location(
        self,
        chat_id: int,
        latitude: float,
        longitude: float,
        reply_to_message_id: int = None,
        **kwargs
    ):
        if self.bot_type == "telegram":
            pass
        elif self.bot_type == "bale":
            pass
        return await super().send_location(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=reply_to_message_id,
            **kwargs
        )

    async def edit_message_text(self, chat_id: int, message_id: int, text: str, **kwargs):
        if self.bot_type == "telegram":
            text = f"{text}"
        elif self.bot_type == "bale":
            text = f"{text}"
        return await super().edit_message_text(chat_id, message_id, text, **kwargs)

    async def delete_message(self, chat_id: int, message_id: int, **kwargs):
        return await super().delete_message(chat_id, message_id, **kwargs)

    async def forward_message(self, chat_id: int, from_chat_id: int, message_id: int, **kwargs):
        return await super().forward_message(chat_id, from_chat_id, message_id, **kwargs)

    async def get_chat_administrators(self, chat_id: int, **kwargs):
        return await super().get_chat_administrators(chat_id, **kwargs)

    async def get_chat_member(self, chat_id: int, user_id: int, **kwargs):
        return await super().get_chat_member(chat_id, user_id, **kwargs)

    async def get_chat_members_count(self, chat_id: int, **kwargs):
        return await super().get_chat_members_count(chat_id, **kwargs)

    async def get_chat(self, chat_id: int, **kwargs):
        return await super().get_chat(chat_id, **kwargs)

    async def get_file(self, file_id: str, **kwargs):
        return await super().get_file(file_id, **kwargs)

    async def get_sticker_set(self, name: str, **kwargs):
        return await super().get_sticker_set(name, **kwargs)

    async def invite_user(self, chat_id: int, user_id: int, **kwargs):
        return await super().invite_user(chat_id, user_id, **kwargs)

    async def leave_chat(self, chat_id: int, **kwargs):
        return await super().leave_chat(chat_id, **kwargs)

    async def promote_chat_member(self, chat_id: int, user_id: int, **kwargs):
        return await super().promote_chat_member(chat_id, user_id, **kwargs)

    async def unban_chat_member(self, chat_id: int, user_id: int, **kwargs):
        return await super().unban_chat_member(chat_id, user_id, **kwargs)

    async def add_sticker_to_set(self, user_id: int, name: str, png_sticker: str, emojis: str, **kwargs):
        return await super().add_sticker_to_set(user_id, name, png_sticker, emojis, **kwargs)

    async def create_new_sticker_set(self, user_id: int, name: str, title: str, png_sticker: str, emojis: str, **kwargs):
        return await super().create_new_sticker_set(user_id, name, title, png_sticker, emojis, **kwargs)

    async def upload_sticker_file(self, user_id: int, png_sticker: str, **kwargs):
        return await super().upload_sticker_file(user_id, png_sticker, **kwargs)

    async def delete_sticker_from_set(self, sticker: str, **kwargs):
        return await super().delete_sticker_from_set(sticker, **kwargs)

    async def create_chat_invite_link(self, chat_id: int, **kwargs):
        return await super().create_chat_invite_link(chat_id, **kwargs)

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: str, **kwargs):
        return await super().revoke_chat_invite_link(chat_id, invite_link, **kwargs)

    async def export_chat_invite_link(self, chat_id: int, **kwargs):
        return await super().export_chat_invite_link(chat_id, **kwargs)

    async def set_chat_photo(self, chat_id: int, photo: str, **kwargs):
        return await super().set_chat_photo(chat_id, photo, **kwargs)

    async def delete_chat_photo(self, chat_id: int, **kwargs):
        return await super().delete_chat_photo(chat_id, **kwargs)

    async def set_chat_title(self, chat_id: int, title: str, **kwargs):
        return await super().set_chat_title(chat_id, title, **kwargs)

    async def set_chat_description(self, chat_id: int, description: str, **kwargs):
        return await super().set_chat_description(chat_id, description, **kwargs)

    async def pin_chat_message(self, chat_id: int, message_id: int, **kwargs):
        return await super().pin_chat_message(chat_id, message_id, **kwargs)

    async def unpin_chat_message(self, chat_id: int, message_id: int = None, **kwargs):
        return await super().unpin_chat_message(chat_id, message_id, **kwargs)

    async def unpin_all_chat_messages(self, chat_id: int, **kwargs):
        return await super().unpin_all_chat_messages(chat_id, **kwargs)

    async def restrict_chat_member(self, chat_id: int, user_id: int, **kwargs):
        return await super().restrict_chat_member(chat_id, user_id, **kwargs)

    async def reply_message_auto(self, update: dict, text: str, **kwargs):
        return await super().reply_message_auto(update, text, **kwargs)

    async def reply_video_auto(self, update: dict, video: str, **kwargs):
        return await super().reply_video_auto(update, video, **kwargs)

    async def reply_voice_auto(self, update: dict, voice: str, **kwargs):
        return await super().reply_voice_auto(update, voice, **kwargs)

    async def reply_sticker_auto(self, update: dict, sticker: str, **kwargs):
        return await super().reply_sticker_auto(update, sticker, **kwargs)

    async def reply_document_auto(self, update: dict, document: str, **kwargs):
        return await super().reply_document_auto(update, document, **kwargs)

    async def reply_animation_auto(self, update: dict, animation: str, **kwargs):
        return await super().reply_animation_auto(update, animation, **kwargs)

    async def reply_audio_auto(self, update: dict, audio: str, **kwargs):
        return await super().reply_audio_auto(update, audio, **kwargs)

    async def reply_photo_auto(self, update: dict, photo: str, **kwargs):
        return await super().reply_photo_auto(update, photo, **kwargs)

    def CallbackQuery(self, _filter=None):
        return super().CallbackQuery(_filter)

    async def answer_callback_query(self, callback_query_id: str, **kwargs):
        return await super().answer_callback_query(callback_query_id, **kwargs)

    async def delete_message_auto(self, message: dict, **kwargs):
        return await super().delete_message_auto(message, **kwargs)

    async def edit_message_text_auto(self, message: dict, text: str, reply_markup=None, **kwargs):
        return await super().edit_message_text_auto(message, text, reply_markup, **kwargs)

    async def edit_message_caption_auto(self, chat_id: int, message_id: int, caption: str, reply_markup=None, **kwargs):
        return await super().edit_message_caption_auto(chat_id, message_id, caption, reply_markup, **kwargs)

    async def send_media_group(
        self,
        chat_id: int,
        media: list,
        reply_to_message_id: int = None,
        reply_markup=None,
        **kwargs
    ):
        return await super().send_media_group(chat_id, media, reply_to_message_id, reply_markup, **kwargs)

    async def copy_message(
        self,
        chat_id: int,
        from_chat_id: int,
        message_id: int,
        caption: str = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        **kwargs
    ):
        return await super().copy_message(chat_id, from_chat_id, message_id, caption, reply_to_message_id, reply_markup, **kwargs)

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        png_sticker: str,
        emojis: str,
        mask_position: dict = None,
        **kwargs
    ):
        return await super().add_sticker_to_set(user_id, name, png_sticker, emojis, mask_position, **kwargs)

    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        png_sticker: str,
        emojis: str,
        contains_masks: bool = None,
        mask_position: dict = None,
        **kwargs
    ):
        return await super().create_new_sticker_set(user_id, name, title, png_sticker, emojis, contains_masks, mask_position, **kwargs)

    async def upload_sticker_file(self, user_id: int, png_sticker: str, **kwargs):
        return await super().upload_sticker_file(user_id, png_sticker, **kwargs)

    async def delete_sticker_from_set(self, sticker: str, **kwargs):
        return await super().delete_sticker_from_set(sticker, **kwargs)

    async def create_chat_invite_link(
        self,
        chat_id: int,
        expire_date: int = None,
        member_limit: int = None,
        **kwargs
    ):
        return await super().create_chat_invite_link(chat_id, expire_date, member_limit, **kwargs)

    async def delete_chat_photo(self, chat_id: int, **kwargs):
        return await super().delete_chat_photo(chat_id, **kwargs)

    async def export_chat_invite_link(self, chat_id: int, **kwargs):
        return await super().export_chat_invite_link(chat_id, **kwargs)

    async def pin_chat_message(
        self,
        chat_id: int,
        message_id: int,
        disable_notification: bool = None,
        **kwargs
    ):
        return await super().pin_chat_message(chat_id, message_id, disable_notification, **kwargs)

    async def restrict_chat_member(
        self,
        chat_id: int,
        user_id: int,
        until_date: int = None,
        can_send_messages: bool = None,
        can_send_media_messages: bool = None,
        can_send_other_messages: bool = None,
        can_add_web_page_previews: bool = None,
        **kwargs
    ):
        return await super().restrict_chat_member(chat_id, user_id, until_date, can_send_messages, can_send_media_messages, can_send_other_messages, can_add_web_page_previews, **kwargs)

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: str, **kwargs):
        return await super().revoke_chat_invite_link(chat_id, invite_link, **kwargs)

    async def set_chat_description(self, chat_id: int, description: str, **kwargs):
        return await super().set_chat_description(chat_id, description, **kwargs)

    async def set_chat_title(self, chat_id: int, title: str, **kwargs):
        return await super().set_chat_title(chat_id, title, **kwargs)

    async def unpin_all_chat_messages(self, chat_id: int, **kwargs):
        return await super().unpin_all_chat_messages(chat_id, **kwargs)

    async def unpin_chat_message(self, chat_id: int, message_id: int = None, **kwargs):
        return await super().unpin_chat_message(chat_id, message_id, **kwargs)

    def LabeledPrice(label: str, amount: int):
        return super().LabeledPrice(label, amount)

    def PreCheckoutQuery(self):
        return super().PreCheckoutQuery()

    class SuccessfulPayment:
        def __init__(self, successful_payment_data: dict):
            super().__init__(successful_payment_data)

    async def send_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        prices: list,
        photo_url: str = None,
        reply_to_message_id: int = None,
    ):
        return await super().send_invoice(chat_id, title, description, payload, provider_token, prices, photo_url, reply_to_message_id)

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: str = None,
    ):
        return await super().answer_pre_checkout_query(pre_checkout_query_id, ok, error_message)

    async def reply_message(self, chat_id: int, text: str, message_id: int, reply_markup=None):
        return await super().reply_message(chat_id, text, message_id, reply_markup)

    async def reply_video(self, chat_id: int, video: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_video(chat_id, video, message_id, caption, reply_markup)

    async def reply_voice(self, chat_id: int, voice: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_voice(chat_id, voice, message_id, caption, reply_markup)

    async def reply_sticker(self, chat_id: int, sticker: str, message_id: int, reply_markup=None):
        return await super().reply_sticker(chat_id, sticker, message_id, reply_markup)

    async def reply_document(self, chat_id: int, document: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_document(chat_id, document, message_id, caption, reply_markup)

    async def reply_animation(self, chat_id: int, animation: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_animation(chat_id, animation, message_id, caption, reply_markup)

    async def reply_audio(self, chat_id: int, audio: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_audio(chat_id, audio, message_id, caption, reply_markup)

    async def reply_photo(self, chat_id: int, photo: str, message_id: int, caption: str = None, reply_markup=None):
        return await super().reply_photo(chat_id, photo, message_id, caption, reply_markup)

    def Message(self, _filter: Filters):
        return super().Message(_filter)

    def Initialize(self):
        return super().Initialize()

    async def get_me(self):
        return await super().get_me()

    async def get_updates(self, offset=None, timeout=30):
        return await super().get_updates(offset, timeout)

    async def process_updates(self):
        return await super().process_updates()

    async def run_initialize_handlers(self):
         await super().run_initialize_handlers()

    async def start(self):
        return await super().start()

    async def stop(self):
        return await super().stop()