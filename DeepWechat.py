import json
from openai import OpenAI


class DeepWechat(object):
    def __init__(self):
        try:
            with open("api_key.json", encoding="utf-8") as r:
                self.api_key = json.load(r)
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
        self.apply_for_start_msg()
        self.apply_for_start_msg_group()

    def init_start_msg(self):
        """
        只保留最初的上下文，即最早的提问和回答
        :return:
        """
        self.msg = self.msg[0:2]
        print("消息长度:", len(self.msg))

    def apply_for_start_msg(self):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.msg,
            stream=False
        )
        self.msg.append(response.choices[0].message)
        print("初始化成功", self.msg)

    def apply_for_start_msg_group(self):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.group_context,
            stream=False
        )
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
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.msg,
            stream=False,
            timeout=10.0
        )
        print("请求结束")
        self.msg.append(response.choices[0].message)
        return response.choices[0].message.content