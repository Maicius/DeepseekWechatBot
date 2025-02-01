import itchat
from itchat.content import *
from DeepWechat import DeepWechat


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 只与指定的微信对象聊天
    target_wechat_name = {"小冬子", "filehelper"}
    print("收到消息", msg.text)
    try:
        if msg['User']['NickName'] not in target_wechat_name:
            return
    except BaseException as e:
        print(e)
        if msg['User']['UserName'] not in target_wechat_name:
            return

    deep_seek_content = deepWechat.apply_for_deepseek(msg)
    msg.user.send('%s' % deep_seek_content)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.text.find("小麦同学") != -1 and not msg.isAt:
        # 在群聊里夸某人
        con_text = "这个消息直接回复，不要把思考过程发出来。{}".format(msg.text)
        if con_text.find('夸') != -1:
            deep_seek_content = deepWechat.apply_for_group(con_text)
            msg.user.send('%s' % deep_seek_content)
    # 在群聊里回应对方的内容，需同时@某人并呼喊"小麦同学"
    if msg.text.find("小麦同学") != -1 and msg.isAt:
        context = [{
            "role": "user", "context": msg.text
        }]
        deep_seek_content = deepWechat.do_apply_deepseek(context)
        msg.user.send('%s' % deep_seek_content)


deepWechat = DeepWechat()
# deepWechat.apply_for_start_msg()
if __name__ == '__main__':
    itchat.auto_login(True)
    itchat.run(True)



