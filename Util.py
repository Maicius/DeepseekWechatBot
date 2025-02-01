import pandas as pd


def process_records():
    data = pd.read_csv("小冬子.csv")
    data = data[['StrContent', 'StrTime', 'NickName']]
    data['emoji'] = data['StrContent'].str.contains('<msg')
    data.apply(lambda x: pro_emoji(x), axis=1)
    data['records'] = data.apply(lambda x: '{}-{}:{}\n'.format(x['StrTime'], x['NickName'], x['StrContent']), axis=1)
    # deepseek token长度限制为65532
    records_text = data['records'].sum()[:60000]
    records_text.replace("\"", "").replace('\'', "")
    return records_text

def pro_emoji(x):
    if x['emoji']:
        x['StrContent'] = 'emoji'


if __name__ == '__main__':
    process_records()