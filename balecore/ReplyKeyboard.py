class ReplyKeyboardMarkup:
    def __init__(self, *rows, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self.keyboard = []
        for row in rows:
            self.keyboard.append([button.to_dict() for button in row])
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def to_dict(self):
        return {
            "keyboard": self.keyboard,
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard,
        }

    def __call__(self):
        return self.to_dict()

class WebAppInfo:
    def __init__(self, url: str):
        self.url = url

    def to_dict(self):
        return {"url": self.url}

class KeyboardButton:
    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False, web_app: WebAppInfo = None):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app

    def to_dict(self):
        data = {"text": self.text}
        if self.request_contact:
            data["request_contact"] = self.request_contact
        if self.request_location:
            data["request_location"] = self.request_location
        if self.web_app:
            data["web_app"] = self.web_app.to_dict()
        return data