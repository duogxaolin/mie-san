import ollama

# ✅ Tải trước mô hình để tránh phải load lại mỗi lần
ollama.pull("gemma2:2b")

# ✅ Tạo một session cho cả chương trình thay vì gọi lại nhiều lần
class OllamaChat:
    def __init__(self, model="gemma2:2b"):
        self.model = model
        self.chat_history = []  # ✅ Giữ lịch sử hội thoại để mô hình phản hồi nhanh hơn

    def chat(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        response = ollama.chat(model=self.model, messages=self.chat_history)
        
        # ✅ Lưu phản hồi để duy trì ngữ cảnh
        self.chat_history.append({"role": "assistant", "content": response['message']})

        return response['message']

# ✅ Chạy thử
if __name__ == "__main__":
    chat_bot = OllamaChat()
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chat_bot.chat(user_input)
        print("Mie-san:", response)
