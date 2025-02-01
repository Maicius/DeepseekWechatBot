import itchat
from itchat.content import *
from DeepWechat import DeepWechat

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 只与指定的微信对象聊天
    target_wechat_name = {"小冬子", "filehelper"}
    print(msg.text)
    if msg['FromUserName'] not in target_wechat_name:
        return
    deep_seek_content = deepWechat.apply_for_deepseek(msg)
    if deep_seek_content.find('不是祝福语') == -1:
        msg.user.send('%s' % deep_seek_content)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.text.find("小麦同学") != -1 and not msg.isAt:
        con_text = "这个消息直接回复，不要把思考过程发出来。{}".format(msg.text)
        if con_text.find('夸') != -1:
            deep_seek_content = deepWechat.apply_for_group(con_text)
            msg.user.send('%s' % deep_seek_content)
    if msg.text.find("小麦同学") != -1 and msg.isAt:
        deep_seek_content = deepWechat.apply_for_deepseek(msg)
        msg.user.send('%s' % deep_seek_content)


deepWechat = DeepWechat()
if __name__ == '__main__':
    itchat.auto_login(True)
    itchat.run(True)



