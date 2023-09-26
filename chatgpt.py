import requests 
import json
url = 'https://api.binjie.fun/api/generateStream'
headers = {'content-type': 'application/json', 'origin': 'https://chat2.jinshutuan.com', 'referer': 'https://chat2.jinshutuan.com/'}
def chat(input_data):
    data = {
    "prompt": input_data,
    "network": True,
    "withoutContext": True,
    "stream": False
    }
    json_data = json.dumps(data)
    response = requests.post(url,headers=headers,data=json_data)
    return response.content.decode('utf8')
    # print(response.content.decode('utf8'))
if __name__ == '__main__':
    data = f'''
    你是纽约时报的编辑，用下列单词写一个英语故事。
    要求：
    1.逻辑自洽，让人有代入感，而不是泛泛而谈。
    2.开头是英文，一句英文一句中文翻译交替显示，
    3.最后列出使用的单词和在文章中的意思
    20个单词：Apple,good,cat,mouse,possession'''
    print(chat(data))