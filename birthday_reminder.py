#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lunar_python import Lunar, Solar
import argparse
import sys
import json

from config import EMAIL, load_birthday_data, save_birthday_data, DEFAULT_ADVANCE_DAYS

class BirthdayReminder:
    def __init__(self):
        self.data = load_birthday_data()
        self.today = datetime.date.today()
    
    def add_birthday(self, name, date, is_lunar=False, advance_days=DEFAULT_ADVANCE_DAYS):
        """添加生日信息"""
        try:
            # 解析日期字符串 (格式: YYYY-MM-DD)
            if "-" in date:
                year, month, day = map(int, date.split('-'))
            else:
                print("错误: 日期格式应为YYYY-MM-DD")
                return False
            
            birthday = {
                "name": name,
                "date": date,
                "is_lunar": is_lunar,
                "advance_days": advance_days
            }
            
            self.data["birthdays"].append(birthday)
            save_birthday_data(self.data)
            print(f"已添加 {name} 的{'农历' if is_lunar else '阳历'}生日: {date}, 提前{advance_days}天提醒")
            return True
        except Exception as e:
            print(f"添加生日时出错: {str(e)}")
            return False
    
    def list_birthdays(self):
        """列出所有生日信息"""
        if not self.data["birthdays"]:
            print("没有保存的生日信息")
            return
        
        print("已保存的生日信息:")
        for i, birthday in enumerate(self.data["birthdays"]):
            print(f"{i+1}. {birthday['name']}: {birthday['date']} ({'农历' if birthday['is_lunar'] else '阳历'}), 提前{birthday['advance_days']}天提醒")
    
    def remove_birthday(self, index):
        """删除生日信息"""
        try:
            index = int(index) - 1
            if 0 <= index < len(self.data["birthdays"]):
                removed = self.data["birthdays"].pop(index)
                save_birthday_data(self.data)
                print(f"已删除 {removed['name']} 的生日信息")
                return True
            else:
                print("无效的索引")
                return False
        except Exception as e:
            print(f"删除生日时出错: {str(e)}")
            return False
    
    def _convert_lunar_to_solar(self, year, month, day):
        """将农历日期转换为阳历日期"""
        # 使用当前年份计算农历生日对应的阳历日期
        current_year = self.today.year
        try:
            # 创建农历日期对象
            lunar_date = Lunar.fromYmd(current_year, month, day)
            # 转换为阳历日期
            solar_date = lunar_date.getSolar()
            return datetime.date(solar_date.getYear(), solar_date.getMonth(), solar_date.getDay())
        except Exception as e:
            # 如果转换失败，尝试使用下一年的日期
            try:
                lunar_date = Lunar.fromYmd(current_year + 1, month, day)
                solar_date = lunar_date.getSolar()
                return datetime.date(solar_date.getYear(), solar_date.getMonth(), solar_date.getDay())
            except Exception as e:
                print(f"农历日期转换错误: {month}-{day}, {str(e)}")
                return None
    
    def _get_next_birthday(self, birthday):
        """计算下一个生日日期"""
        date_str = birthday["date"]
        is_lunar = birthday["is_lunar"]
        
        try:
            year, month, day = map(int, date_str.split('-'))
            
            if is_lunar:
                # 农历生日转换为今年的阳历日期
                next_birthday = self._convert_lunar_to_solar(None, month, day)
                if not next_birthday:
                    return None
            else:
                # 阳历生日
                # 今年的生日日期
                this_year_birthday = datetime.date(self.today.year, month, day)
                # 如果今年的生日已经过了，计算明年的生日
                if this_year_birthday < self.today:
                    next_birthday = datetime.date(self.today.year + 1, month, day)
                else:
                    next_birthday = this_year_birthday
            
            return next_birthday
        except Exception as e:
            print(f"计算下一个生日时出错: {str(e)}")
            return None
    
    def check_birthdays(self, recipient=None):
        """检查需要提醒的生日"""
        reminders = []
        
        for birthday in self.data["birthdays"]:
            next_birthday = self._get_next_birthday(birthday)
            if not next_birthday:
                continue
            
            days_until_birthday = (next_birthday - self.today).days
            
            # 检查是否需要提醒
            if days_until_birthday <= birthday["advance_days"] and days_until_birthday >= 0:
                reminders.append({
                    "name": birthday["name"],
                    "date": next_birthday.strftime("%Y-%m-%d"),
                    "days_left": days_until_birthday,
                    "is_lunar": birthday["is_lunar"]
                })
        
        # 如果有需要提醒的生日，发送邮件
        if reminders and recipient:
            self.send_email(recipient, reminders)
        
        return reminders
    
    def send_email(self, to_email, reminders):
        """发送生日提醒邮件"""
        if not reminders:
            print("没有需要提醒的生日")
            return True
        
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = EMAIL["sender"]
            msg['To'] = to_email
            msg['Subject'] = "生日提醒"
            
            # 构建邮件内容
            body = "您有以下生日需要注意：\n\n"
            for reminder in reminders:
                birthday_type = "农历" if reminder["is_lunar"] else "阳历"
                if reminder["days_left"] == 0:
                    body += f"今天是 {reminder['name']} 的{birthday_type}生日({reminder['date']})！\n"
                else:
                    body += f"距离 {reminder['name']} 的{birthday_type}生日({reminder['date']})还有 {reminder['days_left']} 天\n"
            
            body += "\n这是自动发送的邮件。"
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 连接到SMTP服务器并发送邮件
            server = smtplib.SMTP(EMAIL["smtp_server"], EMAIL["smtp_port"])
            server.starttls()
            server.login(EMAIL["sender"], EMAIL["password"])
            server.send_message(msg)
            server.quit()
            
            print(f"已成功发送生日提醒邮件到 {to_email}")
            return True
        except Exception as e:
            print(f"发送邮件时出错: {str(e)}")
            return False
    
    def run_reminder(self, to_email):
        """运行生日提醒检查并发送邮件"""
        reminders = self.check_birthdays()
        if reminders:
            result = self.send_email(to_email, reminders)
            return result
        else:
            print("今天没有需要提醒的生日")
            return True

def main():
    parser = argparse.ArgumentParser(description="生日提醒工具 - 基础版")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加生日")
    add_parser.add_argument("name", help="姓名")
    add_parser.add_argument("date", help="生日日期 (YYYY-MM-DD)")
    add_parser.add_argument("--lunar", action="store_true", help="是否为农历")
    add_parser.add_argument("--advance", type=int, default=DEFAULT_ADVANCE_DAYS, help="提前几天提醒")
    
    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="删除生日")
    remove_parser.add_argument("index", help="要删除的生日索引")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有生日")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查今天是否有人生日")
    check_parser.add_argument("recipient", nargs="?", help="收件人邮箱")
    
    args = parser.parse_args()
    reminder = BirthdayReminder()
    
    if args.command == "add":
        reminder.add_birthday(args.name, args.date, args.lunar, args.advance)
    elif args.command == "remove":
        reminder.remove_birthday(args.index)
    elif args.command == "list":
        reminder.list_birthdays()
    elif args.command == "check":
        if args.recipient:
            reminder.check_birthdays(args.recipient)
        else:
            birthdays = reminder.check_birthdays()
            if birthdays:
                print("今天需要提醒的生日:")
                for bday in birthdays:
                    birthday_type = "农历" if bday["is_lunar"] else "阳历"
                    if bday["days_left"] == 0:
                        print(f"今天是 {bday['name']} 的{birthday_type}生日！")
                    else:
                        print(f"距离 {bday['name']} 的{birthday_type}生日还有 {bday['days_left']} 天")
            else:
                print("今天没有需要提醒的生日")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 