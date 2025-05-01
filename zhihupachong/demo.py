import json
import random
import time
import execjs
import requests
from loguru import logger
import re
import datetime
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions


def get_cookie():
    co = ChromiumOptions().use_system_user_path()
    page = ChromiumPage(addr_or_opts=co)
    page.get('https://www.zhihu.com/question/1889652865045341213')
    time.sleep(2)
    cookies_ = page.cookies().as_dict()
    return cookies_


def parse_comment(item):
    name = item['author']['name']
    author_id = item['author']['id']
    content = item['content']
    created_time = item['created_time']
    dt_object = datetime.datetime.fromtimestamp(created_time)
    date_time_ = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    like_count = item['like_count']
    try:
        ip = item['comment_tag'][0]['text']
    except Exception:
        ip = None 
    return {
        'name': name,
        'author_id': author_id,
        'date_time_': date_time_,
        'like_count': like_count,
        'ip': ip,
        'content': parse_content(content),
    }


def comment(url__, id_):
    logger.info(f'正在采集 {url__} === {id_} 评论')
    comments = []
    main_comment_count = 0  # 【新增】主评论计数器
    headers['referer'] = url__
    headers['x-zse-93'] = '101_3_3.0'
    url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{id_}/root_comment?order_by=score&limit=20&offset="
    num = 1
    while True:
        """ 主评论 """
        try:
            x_zse_96 = execjs.compile(open('./x_zse_96.js', 'r', encoding='utf-8').read()).call('encrypt', url,
                                                                                                cookies['d_c0'],
                                                                                                headers.get("x-zst-81",
                                                                                                            None))

            headers['x-zse-96'] = x_zse_96

            response = requests.get(
                url,
                cookies=cookies,
                headers=headers,
            )
            # print(response.text)
            time.sleep(random.randint(3, 5))
            for item in response.json()['data']:
                if main_comment_count >=100:
                    break 
                comments.append(parse_comment(item))
                main_comment_count += 1
                child_comment_count = item['child_comment_count']
                if child_comment_count == 0:
                    continue
                """ 子评论 """
                if child_comment_count > 2:
                    reply_root_comment_id = item['reply_root_comment_id']
                    url_child = f'https://www.zhihu.com/api/v4/comment_v5/comment/{reply_root_comment_id}/child_comment?order_by=ts&limit=20&offset='
                    while True:
                        x_zse_96 = execjs.compile(open('./x_zse_96.js', 'r', encoding='utf-8').read()).call('encrypt',
                                                                                                            url_child,
                                                                                                            cookies[
                                                                                                                'd_c0'])
                        headers['x-zse-96'] = x_zse_96
                        response_child = requests.get(
                            url_child,
                            cookies=cookies,
                            headers=headers,
                        )
                        time.sleep(random.randint(3, 5))
                        for item_ in response_child.json()['data']:
                            comments.append(parse_comment(item_))
                        if not response_child.json()['paging']['is_end']:
                            url_child = response_child.json()['paging']['next']
                        else:
                            break
                else:
                    for item_c in item['child_comments']:
                        comments.append(parse_comment(item_c))
            logger.info(f'{id_} 前{num * 20} 主评论成功')
            if num*20 >= 20:
                break
            num += 1
            if not response.json()['paging']['is_end']:
                url = response.json()['paging']['next']
            else:
                break
        except Exception as e:
            logger.error(e)
            time.sleep(2)
    return comments


def parse_content(content):
    patten = etree.HTML(content)
    return ''.join(patten.xpath('//*//text()'))


def save(dic):
    unique_comments = []
    seen = set()
    for comment in dic['comments']:
        if isinstance(comment, dict):
            tuple_rep = tuple(sorted(comment.items()))
        else:
            tuple_rep = comment
        if tuple_rep not in seen:
            seen.add(tuple_rep)
            unique_comments.append(comment)
    dic['comments'] = unique_comments
    with open('./result.txt', 'a+', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False) + '\n')


def search(search_url):
    """ 解析每一个回答 """
    page_size = 5
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
        if commentCount:
            comments = comment(search_url, id)
        else:
            comments = []
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
            'comments': comments,
        })
    offset = 1
    while True:
        try:
            headers['x-zst-81'] = '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZK0Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFHVMjgCGiBHGciSKbq3Mu9Cyp9NLtDcmaDpOG_pM6gSmc_Y1ZgXOjhXybQoTv0N8WCNB_G31Chr86LFXurL_mMe0BvLCwUXm-u3CbqNCVCXy6MtMYCXqm_3YEug9xGSmt9NCTGpq2hH_oC2xYBxyYqX09g3OWut9AGxOfbLm643_HUF9OqfzwbS1YrX9oCVf68xym0p9IcC0puYOJLCfnw2mWbeLNBcfe4CZNDcLTGNCehX9XBLfwCH_HupYjBYfihHKHBcLLhr_tC2MYwS1K0YmD9XKyrS8QTHLf8gC'

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
            time.sleep(random.randint(3, 5))
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
                if commentCount:
                    comments = comment(search_url, id)
                else:
                    comments = []
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
                    'comments': comments,
                })
            if not response_next.json()['paging']['is_end']:
                if offset >= 20: 
                    break 
                offset += 1
            else:
                break
        except Exception as e:
            logger.error(e)
            time.sleep(10)


if __name__ == '__main__':
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
    search('https://www.zhihu.com/question/354466873')
