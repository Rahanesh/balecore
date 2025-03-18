from typing import List, Tuple
import asyncio

class Filter:
    def __init__(self, filter_func):
        self.filter_func = filter_func

    def __call__(self, update):
        return self.filter_func(update)

    def __and__(self, other):
        return Filter(lambda update: self(update) and other(update))

    def __or__(self, other):
        return Filter(lambda update: self(update) or other(update))

class Filters:
    def __init__(self, bot):
        self.bot = bot

    def is_member_of_channels(self, channel_links: List[Tuple[str, int]]):
        async def check_membership(update):
            if not isinstance(update, dict):
                return False
            
            if "message" not in update:
                return False
            
            user_id = update["message"]["from"]["id"]
            for link, channel_id in channel_links:
                try:
                    chat_member = await self.bot.get_chat_member(channel_id, user_id)
                    if chat_member.get("status") not in ["member", "administrator", "creator"]:
                        return False
                except Exception as e:
                    print(f"Error checking membership for channel {channel_id}: {e}")
                    return False
            return True
        
        return check_membership  # بازگرداندن تابع قابل فراخوانی

    def state(self, state: str):
        return Filter(lambda update: "message" in update and self.bot.get_user_state(update["message"]["from"]["id"]) == state)

    def private(self):
        return Filter(lambda update: "message" in update and "chat" in update["message"] and update["message"]["chat"]["type"] == "private")

    def group(self):
        return Filter(lambda update: "message" in update and "chat" in update["message"] and update["message"]["chat"]["type"] == "group")

    def channel(self):
        return Filter(lambda update: "message" in update and "chat" in update["message"] and update["message"]["chat"]["type"] == "channel")

    def text(self):
        return Filter(lambda update: "message" in update and "text" in update["message"])

    def video(self):
        return Filter(lambda update: "message" in update and "video" in update["message"])

    def reply(self):
        return Filter(lambda update: "message" in update and "reply_to_message" in update["message"])

    def supergroup_chat_created(self):
        return Filter(lambda update: "message" in update and "supergroup_chat_created" in update["message"])

    def pinned_message(self):
        return Filter(lambda update: "message" in update and "pinned_message" in update["message"])

    def new_chat_title(self):
        return Filter(lambda update: "message" in update and "new_chat_title" in update["message"])

    def new_chat_photo(self):
        return Filter(lambda update: "message" in update and "new_chat_photo" in update["message"])

    def new_chat_members(self):
        return Filter(lambda update: "message" in update and "new_chat_members" in update["message"])

    def media(self):
        return Filter(lambda update: "message" in update and ("photo" in update["message"] or "video" in update["message"] or "document" in update["message"] or "audio" in update["message"] or "voice" in update["message"]))

    def left_chat_member(self):
        return Filter(lambda update: "message" in update and "left_chat_member" in update["message"])

    def group_chat_created(self):
        return Filter(lambda update: "message" in update and "group_chat_created" in update["message"])

    def forward(self):
        return Filter(lambda update: "message" in update and "forward_from" in update["message"])

    def document(self):
        return Filter(lambda update: "message" in update and "document" in update["message"])

    def contact(self):
        return Filter(lambda update: "message" in update and "contact" in update["message"])

    def channel_chat_created(self):
        return Filter(lambda update: "message" in update and "channel_chat_created" in update["message"])

    def caption(self):
        return Filter(lambda update: "message" in update and "caption" in update["message"])

    def all(self):
        return Filter(lambda update: True)

    def audio(self):
        return Filter(lambda update: "message" in update and "audio" in update["message"])

    def sticker(self):
        return Filter(lambda update: "message" in update and "sticker" in update["message"])

    def voice(self):
        return Filter(lambda update: "message" in update and "voice" in update["message"])

    def command(self, q: str):
        return Filter(lambda update: "message" in update and "text" in update["message"] and update["message"]["text"].startswith(f"/{q}"))

    def pattern(self, q: str):
        return Filter(lambda update: "message" in update and "text" in update["message"] and update["message"]["text"].startswith(f"{q}"))

    def fix(self, q: str):
        return Filter(lambda update: "message" in update and "text" in update["message"] and update["message"]["text"].startswith(f"^{q}&"))

    def multi_command(self, commands: List[str]):
        return Filter(lambda update: "message" in update 
                and "text" in update["message"] 
                and any(update["message"]["text"].startswith(f"/{cmd}") or update["message"]["text"].startswith(cmd) for cmd in commands))

    def callback_query(self, data: str = None):
        return Filter(lambda update: "callback_query" in update and (data is None or update["callback_query"]["data"] == data))

    def callback_query_data_startswith(self, prefix: str):
        return Filter(lambda update: "callback_query" in update and update["callback_query"]["data"].startswith(prefix))

    def callback_query_all(self):
        return Filter(lambda update: "callback_query" in update)

    def pre_checkout_query(self):
        return Filter(lambda update: "pre_checkout_query" in update)

    def successful_payment(self):
        return Filter(lambda update: "message" in update and "successful_payment" in update["message"])

    def contains_keywords(self, keywords: List[str]):
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and any(keyword in update["message"]["text"] for keyword in keywords)
        )

    def long_message(self, min_length: int):
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and len(update["message"]["text"]) >= min_length
        )

    def contains_link(self):
        import re
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and url_pattern.search(update["message"]["text"])
        )

    def contains_mention(self):
        import re
        mention_pattern = re.compile(r'@\w+')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and mention_pattern.search(update["message"]["text"])
        )

    def contains_emoji(self):
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+"
        )
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and emoji_pattern.search(update["message"]["text"])
        )

    def contains_phone_number(self):
        import re
        phone_pattern = re.compile(r'(\+98|0)?9\d{9}')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and phone_pattern.search(update["message"]["text"])
        )

    def contains_location(self):
        return Filter(lambda update: "message" in update 
            and "location" in update["message"]
        )

    def contains_file_type(self, file_types: List[str]):
        return Filter(lambda update: "message" in update 
            and "document" in update["message"] 
            and any(update["message"]["document"]["mime_type"].endswith(file_type) for file_type in file_types)
        )

    def contains_hashtag(self):
        import re
        hashtag_pattern = re.compile(r'#\w+')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and hashtag_pattern.search(update["message"]["text"])
        )

    def contains_number(self):
        import re
        number_pattern = re.compile(r'\d+')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and number_pattern.search(update["message"]["text"])
        )

    def contains_date(self):
        import re
        date_pattern = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and date_pattern.search(update["message"]["text"])
        )

    def contains_time(self):
        import re
        time_pattern = re.compile(r'\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?', re.IGNORECASE)
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and time_pattern.search(update["message"]["text"])
        )

    def contains_postal_code(self):
        import re
        postal_code_pattern = re.compile(r'\b\d{10}\b')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and postal_code_pattern.search(update["message"]["text"])
        )

    def contains_national_code(self):
        import re
        national_code_pattern = re.compile(r'\b\d{10}\b')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and national_code_pattern.search(update["message"]["text"])
        )

    def contains_bank_card(self):
        import re
        bank_card_pattern = re.compile(r'\b\d{16}\b')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and bank_card_pattern.search(update["message"]["text"])
        )

    def contains_hex_color(self):
        import re
        hex_color_pattern = re.compile(r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and hex_color_pattern.search(update["message"]["text"])
        )

    def contains_html(self):
        import re
        html_pattern = re.compile(r'<[^>]+>')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and html_pattern.search(update["message"]["text"])
        )

    def contains_json(self):
        import json
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and self._is_json(update["message"]["text"])
        )
        
    def _is_json(self, text: str):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False

    def contains_xml(self):
        import re
        xml_pattern = re.compile(r'<[^>]+>[^<]+</[^>]+>')
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and xml_pattern.search(update["message"]["text"])
        )

    def contains_sql(self):
        import re
        sql_pattern = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b', re.IGNORECASE)
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and sql_pattern.search(update["message"]["text"])
        )

    def contains_code(self):
        import re
        code_pattern = re.compile(r'\b(def|function|class|import|console\.log|print)\b', re.IGNORECASE)
        return Filter(lambda update: "message" in update 
            and "text" in update["message"] 
            and code_pattern.search(update["message"]["text"])
        )

    @property
    def pre_checkout_query_id(self):
        return self.pre_checkout_query.get("id")

    @property
    def pre_checkout_query_from(self):
        return self.pre_checkout_query.get("from", {})

    @property
    def pre_checkout_query_currency(self):
        return self.pre_checkout_query.get("currency")

    @property
    def pre_checkout_query_total_amount(self):
        return self.pre_checkout_query.get("total_amount")

    @property
    def pre_checkout_query_invoice_payload(self):
        return self.pre_checkout_query.get("invoice_payload")

    @property
    def successful_payment_currency(self):
        return self.successful_payment.get("currency")

    @property
    def successful_payment_total_amount(self):
        return self.successful_payment.get("total_amount")

    @property
    def successful_payment_invoice_payload(self):
        return self.successful_payment.get("invoice_payload")

    @property
    def successful_payment_telegram_payment_charge_id(self):
        return self.successful_payment.get("telegram_payment_charge_id")