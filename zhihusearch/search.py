import json
import random
import time
import execjs
import requests
from loguru import logger
import re
import datetime
from lxml import etree
import urllib.parse
from DrissionPage import ChromiumPage, ChromiumOptions


def get_cookie():
    co = ChromiumOptions().use_system_user_path()
    page = ChromiumPage(addr_or_opts=co)
    page.get('https://www.zhihu.com/question/1889652865045341213')
    time.sleep(2)
    cookies_ = page.cookies().as_dict()
    return cookies_


def parse_content(content):
    patten = etree.HTML(content)
    return ''.join(patten.xpath('//*//text()'))


def save(dic):
    with open('./zhichang.txt', 'a+', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False) + '\n')


def search(key):
    headers['referer'] = f'https://www.zhihu.com/search?type=content&q={urllib.parse.quote_plus(key)}'
    url = f'/api/v4/search_v3?gk_version=gz-gaokao&t=general&q={urllib.parse.quote_plus(key)}&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal'
    while True:
        try:
            x_zse_96 = execjs.compile(open('./x_zse_96.js', 'r', encoding='utf-8').read()).call('encrypt', url, cookies['d_c0'],
                                                                                                headers.get("x-zst-81", None))

            headers['x-zse-96'] = x_zse_96
            response = requests.get(f'https://www.zhihu.com{url}', cookies=cookies, headers=headers)
            for item in response.json()['data']:
                try:
                    title = parse_content(item['object']['title'])
                    voteup_count = item['object']['voteup_count']
                    comment_count = item['object']['comment_count']
                    url = item['object']['url']
                    updated_time = item['object']['updated_time']
                    dt_object = datetime.datetime.fromtimestamp(updated_time)
                    date_time_ = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    # print(title, voteup_count, comment_count, date_time_, url)
                    save({
                        'search_key': key,
                        'title': title,
                        'voteup_count': voteup_count,
                        "comment_count": comment_count,
                        'date_time_': date_time_,
                        'url': url,
                    })
                except KeyError:
                    continue
            if not response.json()['paging']['is_end']:
                search_hash_id = response.json()['search_action_info']['search_hash_id']
                lc_idx = response.json()['search_action_info']['lc_idx']
                logger.info(f'{key} == 前 {lc_idx} 成功')
                url = f'/api/v4/search_v3?gk_version=gz-gaokao&t=general&q={urllib.parse.quote_plus(key)}&correction=1&offset={lc_idx}&limit=20&filter_fields=&lc_idx={lc_idx}&show_all_topics=0&search_hash_id={search_hash_id}&search_source=Normal&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0'
                time.sleep(2)
            else:
                break
        except Exception as e:
            logger.error(f'{key} == {e}')
            time.sleep(5)


if __name__ == '__main__':
    cookies = get_cookie()
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-requested-with': 'fetch',
        'x-zse-93': '101_3_3.0',
        'x-zst-81': '3_2.0VhnTj77m-qofgh3TxTnq2_Qq2LYuDhV80wSL7iUZQ6nxE_20m4fBJCHMiqHPD4S1hCS974e1DrNPAQLYlUefii7q26fp2L2ZKgSfnveCgrNOQwXTt_Fq6DQye8t9DGwT9RFZQAuTLbHP2GomybO1VhRTQ6kp-XxmxgNK-GNTjTkxkhkKh0PhHix_F0fpVrHG8C2CohxB3DLB-Uc_uGFGkcVO8USVc6SCvgX0fhe129FVycHCM0omFH_z-bO_YBx9GCo86QXyr03mIGV0Ju2MJ4VfTwY9W9SL0BC8eLVZ0DCKTcHCKhHmXrOf-CX1HDwY_B28iUNKyBCKLU2_DCYOYJe1e029DbxKHrOfQ7NL68ws',
    }
    search('职场')
