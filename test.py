import time
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

start_time = time.time()  # Lấy thời gian bắt đầu

response = client.chat.completions.create(
    model="gemma2:2b",
    messages=[
        {"role": "user", "content": "Bạn biết những ngôn ngữ nào"}
    ]
)

end_time = time.time()  # Lấy thời gian kết thúc

# Lấy nội dung phản hồi
message_content = response.choices[0].message.content

# Tính thời gian phản hồi
response_time = end_time - start_time

# Hiển thị kết quả
print(f"⏳ Thời gian phản hồi: {response_time:.2f} giây")
print(f"🤖 AI: {message_content}")
