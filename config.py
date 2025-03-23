import os
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

# 邮件设置
EMAIL = {
    "sender": os.getenv("EMAIL_SENDER"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "default_recipient": os.getenv("EMAIL_RECIPIENT")
}

# 生日数据文件路径
DATA_FILE = "data.json"

# 默认提前提醒的天数
DEFAULT_ADVANCE_DAYS = 3

def load_birthday_data():
    """加载生日数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"birthdays": []}

def save_birthday_data(data):
    """保存生日数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 