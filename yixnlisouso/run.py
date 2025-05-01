import os.path
import requests
import execjs
import json

with open('sign.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

headers = {
    'authority': 's.xinli001.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'origin': 'https://static.xinli001.com',
    'pragma': 'no-cache',
    'referer': 'https://static.xinli001.com/',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
}

keywords = input('输入关键词(空格隔开)：')
for keyword in keywords.split(' '):
    p = 0
    while True:
        p += 1
        print(f'正在爬取 {keyword} 第{p}页')
        params = {
            'keyword': keyword,
            'page': f'{p}',
        }
        params = execjs.compile(js_code).call('getRequestSign', params)['params']

        response = requests.get('https://s.xinli001.com/v1/question', params=params, headers=headers)

        print(response.json())
        if not os.path.exists(f'{keyword}.json'):
            Data = {
                "keyword": keyword,
                "question": []
            }
        else:
            with open(f'{keyword}.json', 'r', encoding='utf-8') as f:
                Data = json.load(f)
        if 'Server Error' in response.text:
            print('请求失败')
        data = response.json()['data']['data']
        for d in data:
            Data['question'].append({
                "title": d['title'],
                "content": d['content'],
                "useful": int(d['zan_num']),
                "reply": int(d['comment_num']),
            })
        with open(f'{keyword}.json', 'w', encoding='utf-8') as f:
            json.dump(Data, f, ensure_ascii=False, indent=4)
        if p == 1000:
            break

print('爬取完成')
