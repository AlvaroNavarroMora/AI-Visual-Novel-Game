class ChatManager:
    def __init__(self):
        self.messages = []
        self.new_image = "book-cover.png"

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_ai_message(self, message):
        self.messages.append({"role": "assistant", "content": message})

    def get_conversation_history(self):
        return self.messages.copy()
    
    def clear_conversation(self):
        self.messages = []
        self.new_image = "book-cover.png"
        
    def set_new_image(self, image):
        self.new_image = image
        
    def get_new_image(self):
        return self.new_image
