# 生日提醒工具（基础版）

这是一个简单的生日提醒工具，支持阳历和农历生日提醒。它通过QQ邮箱发送提醒，可以设置提前几天提醒，并支持管理多个生日联系人。

## 功能特点

- 支持阳历（公历）和农历生日
- 通过QQ邮箱发送电子邮件提醒
- 可以设置提前多少天发送提醒
- 支持管理多个联系人生日
- 命令行接口，简单易用

## 安装步骤

1. 克隆此仓库到本地：
   ```bash
   git clone https://github.com/你的用户名/birthday-basicmodel.git
   cd birthday-basicmodel
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置邮箱信息：
   - 复制`.env.example`文件并重命名为`.env`
   - 编辑`.env`文件，填入你的QQ邮箱信息：
     ```
     EMAIL_SENDER=你的QQ邮箱地址
     EMAIL_PASSWORD=你的QQ邮箱授权码（不是登录密码）
     EMAIL_RECIPIENT=默认接收提醒的邮箱地址
     ```
   
   > 注意：QQ邮箱授权码需要在QQ邮箱设置中申请，具体可参考[QQ邮箱POP3/SMTP设置](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)

## 使用方法

### 添加生日
```bash
# 添加阳历生日
python birthday_reminder.py add "张三" "1990-01-01"

# 添加农历生日
python birthday_reminder.py add "李四" "1992-02-02" --lunar

# 添加生日并设置提前5天提醒
python birthday_reminder.py add "王五" "1995-05-05" --advance 5
```

### 查看已添加的生日列表
```bash
python birthday_reminder.py list
```

### 删除生日
```bash
# 首先通过list命令查看生日列表，然后根据索引号删除
python birthday_reminder.py list
python birthday_reminder.py remove 1  # 删除索引为1的生日
```

### 手动检查并发送提醒
```bash
python birthday_reminder.py check "接收提醒的邮箱@example.com"
```

### 手动检查不发送邮件
```bash
python birthday_reminder.py check
```

## 自动化部署

要实现自动化生日提醒，可以通过以下方法：

1. **使用系统定时任务（Cron）**：
   在Linux/macOS系统上，可以使用crontab设置定时任务：
   ```bash
   # 编辑crontab
   crontab -e
   
   # 添加以下内容，每天上午8点执行
   0 8 * * * cd /path/to/birthday-basicmodel && python birthday_reminder.py check "your-email@example.com"
   ```

2. **使用Windows任务计划程序**：
   在Windows系统上，可以使用任务计划程序设置定时任务。

## 注意事项

- 为保证农历日期转换的准确性，建议添加完整的生日日期（年-月-日）
- 首次使用QQ邮箱发送邮件可能需要进行安全验证
- 生日数据存储在本地的`data.json`文件中，请谨慎管理此文件

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT 