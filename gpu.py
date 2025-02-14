import torch
print("GPU có sẵn:", torch.cuda.is_available())
print("Số GPU:", torch.cuda.device_count())
print("Tên GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Không có GPU")
