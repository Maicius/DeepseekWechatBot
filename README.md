# DeepseekWechatBot

基于Deepseek和Itchat的微信聊天机器人

### 主要功能：
> 1.使用deepseek学习和指定微信好友之间的聊天记录，然后模仿自己和该好友对话。
不是模型微调，只是把聊天记录先发过去，保存对话对上下文。

> 2.夸夸夸机器人，在微信群中呼喊"小麦同学"，并说"夸XXX"，就会对指定对象吹彩虹屁。

### LIMIT

> 1.本项目基于itchat，即使用网页微信登陆，必须先确保自己的微信号能登陆[网页微信](https://wx.qq.com/)才可以使用。

> 2.由于deepseek接口不稳定，所以经常失败

### PREPARE

使用第三方工具导出聊天记录，经测试，只能在windows环境下进行，这里推荐两个工具：

1.[WeChatMsg](https://github.com/LC044/WeChatMsg)

2.[PyWxDump](https://github.com/xaoyaoo/PyWxDump)

将导出的聊天记录保存为csv，csv处理的代码在[Util.py](./Util.py)中

#### 申请Deepseek API KEY

[Deepseek开发者平台](https://www.deepseek.com/)
有免费的10块钱额度，够用很多次了。

#### 在main.py中修改指定聊天微信对象的昵称。

为便于测试，同时把文件传输助手filehelper加上
> target_wechat_name = {"XXX", "filehelper}

### BEGIN

做好以上准备工作：
> python main.py

### NOTICE

若出现HTMLParse错误，请参考：[使用python3.9，会报错](https://github.com/littlecodersh/ItChat/issues/963)