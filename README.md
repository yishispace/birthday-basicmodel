# 生日提醒工具（基础版）

这是一个简单的生日提醒工具，支持阳历和农历生日提醒。它通过QQ邮箱发送提醒，可以设置提前几天提醒，并支持管理多个生日联系人。

## 功能特点

- 支持阳历（公历）和农历生日
- 通过QQ邮箱发送电子邮件提醒
- 可以设置提前多少天发送提醒
- 支持管理多个联系人生日
- 命令行接口，简单易用

## 零基础使用指南

### 一、创建个人仓库（不需要编程知识）

1. **注册GitHub账号**：
   - 打开 [GitHub官网](https://github.com) 并点击右上角的"Sign up"
   - 按照提示填写用户名、邮箱和密码
   - 完成验证步骤

2. **创建新仓库**：
   - 登录后，点击页面右上角的"+"，然后选择"New repository"
   - 在仓库名称框中输入：`birthday-basicmodel`
   - 描述可以填写：`我的生日提醒工具`
   - 选择"Public"（公开）
   - 勾选"Add a README file"（添加一个README文件）
   - 点击"Create repository"（创建仓库）

3. **导入本项目代码**：
   - 在新创建的仓库页面中，点击"Import code"按钮
   - 在"Your old repository's clone URL"中输入：`https://github.com/pufeng-yi/birthday-basicmodel.git`
   - 点击"Begin import"，等待导入完成

### 二、配置邮箱和密钥（保证能发送邮件）

1. **获取QQ邮箱授权码**：
   - 登录QQ邮箱网页版
   - 点击左上角的"设置"图标，选择"账户"
   - 在页面底部找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
   - 开启"POP3/SMTP服务"
   - 按照提示完成验证，获取授权码（注意保存，这将作为发送邮件的密码）

2. **添加GitHub密钥**：
   - 回到你的GitHub仓库页面
   - 点击顶部的"Settings"（设置）选项卡
   - 在左侧栏找到"Secrets and variables"，点击展开后选择"Actions"
   - 点击"New repository secret"按钮添加以下三个密钥：
     
     a. 添加第一个密钥：
     - Name(名称): `EMAIL_SENDER`
     - Secret(值): 你的QQ邮箱地址（例如：12345678@qq.com）
     - 点击"Add secret"
     
     b. 添加第二个密钥：
     - Name(名称): `EMAIL_PASSWORD`
     - Secret(值): 你之前获取的QQ邮箱授权码（不是登录密码）
     - 点击"Add secret"
     
     c. 添加第三个密钥：
     - Name(名称): `EMAIL_RECIPIENT`
     - Secret(值): 接收提醒的邮箱地址（可以是你自己的邮箱）
     - 点击"Add secret"

### 三、启用自动运行（每天自动检查并发送提醒）

1. **启用GitHub Actions**：
   - 在你的仓库页面中，点击顶部的"Actions"选项卡
   - 如果看到提示，点击"I understand my workflows, go ahead and enable them"
   - 在列表中找到"Daily Birthday Check"工作流
   - 点击进入后，点击右侧的"Enable workflow"按钮

2. **手动测试运行**：
   - 在工作流页面中，点击"Run workflow"按钮
   - 点击绿色的"Run workflow"确认
   - 等待几分钟，观察运行状态（绿色勾表示成功）
   - 检查你的接收邮箱，确认是否收到测试邮件

### 四、管理生日信息（自定义生日提醒）

1. **在线编辑生日数据**：
   - 在你的仓库页面，找到并点击`data.json`文件
   - 点击右上角的编辑按钮（铅笔图标）
   - 参照以下格式添加或修改生日信息：
   ```json
   {
     "birthdays": [
       {
         "name": "张三",         // 姓名
         "date": "1990-01-01",  // 生日日期（格式必须是YYYY-MM-DD）
         "is_lunar": false,     // 是否为农历生日（false表示阳历，true表示农历）
         "advance_days": 3      // 提前几天发送提醒
       },
       {
         "name": "李四",
         "date": "1992-02-02",
         "is_lunar": true,      // 这是一个农历生日
         "advance_days": 5      // 提前5天发送提醒
       }
       // 可以按照同样格式添加更多人的生日
     ]
   }
   ```
   - 修改完成后，滚动到页面底部
   - 在"Commit changes"框中输入说明，如："更新生日信息"
   - 点击"Commit changes"按钮保存更改

2. **修改提醒天数**：
   - 如上所示，在`data.json`文件中，每个生日信息中的`advance_days`参数控制提前几天发送提醒
   - 例如，想提前7天收到提醒，就将对应人的`advance_days`值改为`7`

3. **设置阴历/阳历**：
   - 在`data.json`文件中，每个生日信息中的`is_lunar`参数控制是否为农历生日
   - `false`表示阳历（公历）生日
   - `true`表示农历（阴历）生日

### 五、自定义运行时间（调整自动检查的时间点）

1. **修改每日运行时间**：
   - 在你的仓库中找到并点击`.github/workflows/daily-check.yml`文件
   - 点击编辑按钮（铅笔图标）
   - 找到以下内容（大约在第5-6行）：
   ```yaml
   schedule:
     # 每天早上8点运行 (UTC时间，对应北京时间16点)
     - cron: '0 0 * * *'
   ```
   - 修改`cron`表达式来调整运行时间，格式为：`分钟 小时 日期 月份 星期`
   - 例如：
     - `0 0 * * *` 表示每天UTC时间0点0分（北京时间8点）
     - `0 12 * * *` 表示每天UTC时间12点0分（北京时间20点）
     - `30 22 * * *` 表示每天UTC时间22点30分（北京时间次日6点30分）
   - **注意**：GitHub使用UTC时间，比北京时间晚8小时
   - 修改后，滚动到页面底部输入提交说明并点击"Commit changes"保存

2. **设置多个运行时间**：
   - 如果想要一天多次检查，可以添加多个cron表达式，例如：
   ```yaml
   schedule:
     - cron: '0 0 * * *'   # 每天UTC时间0点（北京时间8点）
     - cron: '0 12 * * *'  # 每天UTC时间12点（北京时间20点）
   ```

### 六、常见问题解答

1. **我没有收到邮件提醒怎么办？**
   - 检查"Actions"标签页中最近一次运行是否成功（绿色勾表示成功）
   - 检查你的垃圾邮件文件夹，提醒邮件可能被误判为垃圾邮件
   - 确认你的QQ邮箱授权码是否正确设置
   - 确认接收邮箱地址是否正确

2. **如何只在有生日的日子才发送邮件？**
   - 系统默认只会在有人生日时（或到达提前提醒天数时）才发送邮件
   - 如果在没有生日的日子收到了邮件，请检查data.json文件中的生日信息是否正确

3. **农历生日转换不准确怎么办？**
   - 确保添加的生日日期格式正确（YYYY-MM-DD）
   - 对于特殊的农历日期（如闰月），可能需要特别注意转换

4. **GitHub Actions没有运行怎么办？**
   - 确认你已经启用了Actions功能
   - 检查仓库的Actions标签页中是否有错误提示
   - 尝试手动触发运行来检查问题

5. **我想添加很多生日，有简单的方法吗？**
   - 可以一次性在data.json文件中批量添加多个生日信息
   - 确保JSON格式正确，每个生日信息之间用逗号分隔

### 七、高级自定义（可选）

如果你有一定的编程基础，还可以进行以下高级自定义：

1. **修改邮件标题和内容**：
   - 编辑`birthday_reminder.py`文件中的`send_email`方法
   - 修改`msg['Subject']`可以自定义邮件标题
   - 修改`body`变量的内容可以自定义邮件正文

2. **自定义更多命令**：
   - 编辑`birthday_reminder.py`文件中的`main`函数
   - 可以添加新的子命令和参数

3. **本地使用此工具**：
   - 克隆仓库到本地：`git clone https://github.com/你的用户名/birthday-basicmodel.git`
   - 进入目录：`cd birthday-basicmodel`
   - 安装依赖：`pip install -r requirements.txt`
   - 创建并配置`.env`文件
   - 使用命令行运行工具

## 使用方法（命令行）

如果你想在自己的电脑上运行这个工具，可以使用以下命令：

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

## 自动化部署（本地）

要在本地计算机上实现自动化生日提醒，可以通过以下方法：

1. **使用系统定时任务（Cron）**：
   在Linux/macOS系统上，可以使用crontab设置定时任务：
   ```bash
   # 编辑crontab
   crontab -e
   
   # 添加以下内容，每天上午8点执行
   0 8 * * * cd /path/to/birthday-basicmodel && python birthday_reminder.py check "your-email@example.com"
   ```

2. **使用Windows任务计划程序**：
   - 打开"任务计划程序"（在开始菜单中搜索）
   - 点击"创建基本任务"
   - 输入任务名称（如"生日提醒"）和描述
   - 选择"每天"触发
   - 设置开始时间和运行频率
   - 选择"启动程序"
   - 浏览并选择Python程序路径（如"C:\Python\python.exe"）
   - 在"添加参数"中输入："birthday_reminder.py check your-email@example.com"
   - 在"起始于"中输入你的项目目录路径
   - 完成设置并保存

## 注意事项

- 为保证农历日期转换的准确性，建议添加完整的生日日期（年-月-日）
- 首次使用QQ邮箱发送邮件可能需要进行安全验证
- 生日数据存储在本地的`data.json`文件中，请谨慎管理此文件
- GitHub Actions有运行次数限制，但对个人使用完全足够

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT 
