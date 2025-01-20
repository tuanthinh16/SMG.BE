import logging

# Cấu hình logger
logger = logging.getLogger('plugin_logger')
logger.setLevel(logging.DEBUG)  # Ghi tất cả mức độ thông tin, từ DEBUG đến ERROR

# Tạo một handler để ghi ra file .txt với mã hóa UTF-8
file_handler = logging.FileHandler('logs.txt', mode='w', encoding='utf-8')  # Thêm encoding='utf-8'
file_handler.setLevel(logging.DEBUG)

# Tạo một định dạng cho các log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Thêm handler vào logger
logger.addHandler(file_handler)

# Thêm StreamHandler để ghi log ra console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

