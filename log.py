import logging

# Cấu hình logger
logger = logging.getLogger('plugin_logger')
logger.setLevel(logging.DEBUG)  # Ghi tất cả mức độ thông tin, từ DEBUG đến ERROR

# Tạo một handler để ghi ra file .txt
file_handler = logging.FileHandler('logs.txt')
file_handler.setLevel(logging.DEBUG)

# Tạo một định dạng cho các log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Thêm handler vào logger
logger.addHandler(file_handler)
