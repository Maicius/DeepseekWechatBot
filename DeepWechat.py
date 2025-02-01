import json
from openai import OpenAI
from Util import process_records


class DeepWechat(object):
    def __init__(self):
        try:
            with open("api_key.json", encoding="utf-8") as r:
                self.api_key = json.load(r)['api_key']
        except BaseException as e:
            print("ERROR:载入API KEY 失败")
            raise e
        with open("promot.json", encoding="utf-8") as r:
            self.promot = json.load(r)
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        self.msg = [
            {'role': 'user', 'content': self.promot['init_msg']}
        ]
        self.group_context = [
            {"role": 'user', 'content': self.promot['kuakua']}
        ]

    def init_start_msg(self):
        """
        只保留最初的上下文，即最早的提问和回答
        :return:
        """
        self.msg = self.msg[0:4]
        print("消息长度:", len(self.msg))

    def apply_for_start_msg(self):
        print("开始初始化")
        response = self.do_apply_deepseek(self.msg)
        self.msg.append(response.choices[0].message)
        print("初始化成功，开始学习聊天记录", response.choices[0].message)
        self.init_records()

    def do_apply_deepseek(self, msg):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=msg,
                stream=False,
                timeout=10.0
            )
            return response
        except BaseException as e:
            print("ERROR================\n网络出错，请稍后再试")
            raise e

    def apply_for_start_msg_group(self):
        response = self.do_apply_deepseek(self.group_context)
        self.group_context.append(response.choices[0].message)
        print("初始化成功", self.group_context)

    def apply_for_group(self, message):
        self.group_context.append({
            "role": "user",
            "content": message
        })
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.group_context,
            stream=False,
            timeout=10.0
        )
        if message.find("结束本轮对话") != -1:
            self.group_context = self.group_context[0:2]
        else:
            self.group_context.append(response.choices[0].message)
        return response.choices[0].message.content

    def apply_for_deepseek(self, messages):
        self.msg.append({
            "role": "user",
            "content": messages.text
        })
        print("开始请求,", self.msg)
        response = self.do_apply_deepseek(self.msg)
        print("请求结束,{}".format(response.choices[0].message.content))
        self.msg.append(response.choices[0].message)
        return response.choices[0].message.content

    def init_records(self):
        records_text = process_records()
        # 发送聊天记录
        records_text = "这是我们的聊天记录，如果你学会了，就说一句我最常说的话。\n{}".format(records_text)
        self.msg.append({"role": "user", "content": records_text})
        response = self.do_apply_deepseek(self.msg)
        print("学习聊天记录成功,{}".format(response.choices[0].message.content))
        self.msg.append(response.choices[0].message)
        # 告诉deepseek正式开始
        self.msg.append({"role": "user", "content": self.promot['begin_msg']})
        response = self.do_apply_deepseek(self.msg)
        self.msg.append(response.choices[0].message)
        print("{}".format(response.choices[0].message.content))


if __name__ == '__main__':
    deep = DeepWechat()
    deep.apply_for_start_msg()