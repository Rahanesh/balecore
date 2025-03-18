class InlineKeyboardMarkup:
    def __init__(self, *rows):
        self.inline_keyboard = []
        for row in rows:
            self.inline_keyboard.append([button.to_dict() for button in row])

    def to_dict(self):
        return {"inline_keyboard": self.inline_keyboard}

    def __call__(self):
        return self.to_dict()

class WebAppInfo:
    def __init__(self, url: str):
        self.url = url

    def to_dict(self):
        return {"url": self.url}

class InlineKeyboardButton:
    def __init__(self, text: str, url: str = None, callback_data: str = None, web_app: WebAppInfo = None):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.web_app = web_app

    def to_dict(self):
        data = {"text": self.text}
        if self.url:
            data["url"] = self.url
        if self.callback_data:
            data["callback_data"] = self.callback_data
        if self.web_app:
            data["web_app"] = self.web_app.to_dict()
        return data