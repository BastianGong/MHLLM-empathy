# -*- coding: utf-8 -*-
import json
import os
import re
import time
import random
import datetime
import execjs
import requests
from loguru import logger
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions


#使用时应该关闭全部谷歌浏览器
def get_cookie():
    # co = ChromiumOptions()
    # co.set_browser_path(r'D:\Program Files\Google\Chrome\Application\chrome.exe')
    # co.set_argument(r'--user-data-dir=C:\Users\restrain\AppData\Local\Google\Chrome\User Data')
    # # ✅ 保证使用 Default 用户配置（即默认登录的配置）
    # co.set_argument('--profile-directory=Default')
    # co.set_argument('--remote-debugging-port=9222')

    co = ChromiumOptions().use_system_user_path()

    page = ChromiumPage(addr_or_opts=co)
    page.get('https://www.zhihu.com/question/1889652865045341213')
    time.sleep(2)
    cookies_ = page.cookies().as_dict()
    return cookies_


def parse_content(content):
    patten = etree.HTML(content)
    return ''.join(patten.xpath('//*//text()'))


def save(dic, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False) + '\n')


def search(search_url, save_path):
    """ 解析每一个回答 """
    page_size = 50
    questions_id = search_url.rsplit("/", 1)[-1]
    response = requests.get(search_url, cookies=cookies, headers=headers)
    patten = etree.HTML(response.text)
    question = ''.join(patten.xpath('//h1[@class="QuestionHeader-title"]/text()'))
    print(question)
    answer_lst = re.search(r'<script id="js-initialData" type="text/json">(.*?)</script>', response.text, re.S).group(1)
    cursor = json.loads(answer_lst)['initialState']['question']['answers'][questions_id]['newIds'][-1]['cursor']
    sessionId = json.loads(answer_lst)['initialState']['question']['answers'][search_url.rsplit("/", 1)[-1]][
        'sessionId']
    for key, value in json.loads(answer_lst)['initialState']['entities']['answers'].items():
        name = value['author']['name']
        author_id = value['author']['id']
        content = value['content']
        commentCount = value['commentCount']
        id = value['id']
        voteupCount = value['voteupCount']
        createdTime = value['updatedTime']
        dt_object = datetime.datetime.fromtimestamp(createdTime)
        date_time_ = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        save({
            'name': name,
            'question': question,
            "search_url": search_url,
            'author_id': author_id,
            'content': parse_content(content),
            'commentCount': commentCount,
            'id': id,
            'voteupCount': voteupCount,
            'createdTime': date_time_,
        }, save_path)
    offset = 1
    while True:
        try:
            headers[
                'x-zst-81'] = '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZK0Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFHVMjgCGiBHGciSKbq3Mu9Cyp9NLtDcmaDpOG_pM6gSmc_Y1ZgXOjhXybQoTv0N8WCNB_G31Chr86LFXurL_mMe0BvLCwUXm-u3CbqNCVCXy6MtMYCXqm_3YEug9xGSmt9NCTGpq2hH_oC2xYBxyYqX09g3OWut9AGxOfbLm643_HUF9OqfzwbS1YrX9oCVf68xym0p9IcC0puYOJLCfnw2mWbeLNBcfe4CZNDcLTGNCehX9XBLfwCH_HupYjBYfihHKHBcLLhr_tC2MYwS1K0YmD9XKyrS8QTHLf8gC'

            url_ = f'/api/v4/questions/{questions_id}/feeds?cursor={cursor}&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Ckvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit={page_size}&offset={offset}&order=default&platform=desktop&session_id={sessionId}&ws_qiangzhisafe=0'

            x_zse_96 = execjs.compile(open('./x_zse_96.js', 'r', encoding='utf-8').read()).call('encrypt', url_,
                                                                                                cookies['d_c0'],
                                                                                                headers.get("x-zst-81",
                                                                                                            None))
            headers['x-zse-93'] = '101_3_3.0'
            headers['x-zse-96'] = x_zse_96
            response_next = requests.get(
                f'https://www.zhihu.com{url_}',
                cookies=cookies,
                headers=headers,
            )

            time.sleep(random.randint(0, 1))
            for ii in response_next.json()['data']:
                name = ii['target']['author']['name']
                author_id = ii['target']['author']['id']
                content = ii['target']['content']
                commentCount = ii['target']['comment_count']
                cursor = ii['cursor']
                id = ii['target']['id']
                voteupCount = ii['target']['voteup_count']
                createdTime = ii['target']['updated_time']
                dt_object = datetime.datetime.fromtimestamp(createdTime)
                date_time_ = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                save({
                    'name': name,
                    'question': question,
                    "search_url": search_url,
                    'author_id': author_id,
                    'content': parse_content(content),
                    'commentCount': commentCount,
                    'id': id,
                    'voteupCount': voteupCount,
                    'createdTime': date_time_,
                }, save_path)
            if page_size * offset > 100:
                break
            if not response_next.json()['paging']['is_end']:
                offset += 1
            else:
                break
        except Exception as e:
            logger.error(e)
            time.sleep(10)



def convert_txt_to_json(input_file_parent,output_file_parent):
    num_files = 20
    for i in range(num_files):

        input_file = f"{input_file_parent}/r{i:02}.txt"
        output_file = f"{output_file_parent}/result{i}.json"

        data = []

        if not os.path.exists(input_file):
            print(f"文件不存在：{input_file}")
            continue

        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        obj = json.loads(line)
                        data.append(obj)
                    except json.JSONDecodeError as e:
                        print(f"[{input_file} - 第 {line_num} 行] JSON 解析错误：{e}")
                        print(f"出错内容：{line}")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"已转换：{input_file} -> {output_file}")


if __name__ == '__main__':

    input_links_file = r"E:\restrain\Desktop\zhihu\result\jiaolv\top_20_titlesjiaolv.txt"
    with open(input_links_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        match = re.search(r'(https://www\.zhihu\.com/question/\d+)', line)
        if not match:
            print(f"第{i}行未匹配到链接，跳过")
            continue

        url = match.group(1)
        print(f'\n===== 开始处理第{i}条：{url} =====')

  
  
        cookies = get_cookie()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

   
        save_path = f'../result/jiaolv/r{i:02}.txt'
        search(url, save_path)

    input_file_parent = f"../result/jiaolv"
    output_file_parent = f"../result/jiaolv"
  
    convert_txt_to_json(input_file_parent,output_file_parent)
