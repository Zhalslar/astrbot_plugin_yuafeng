import requests

from astrbot import logger

yuafeng_api ="https://api.yuafeng.cn/API/"

def translate_text(text):
    base_url = f"{yuafeng_api}/ydfy/api.php"
    params = {
        "msg": text,
        "type": 'json'
    }
    try:
        # {'code': '200', 'msg': {'original': 'Hello, stranger.', 'translated': '你好,陌生人。'}}
        response = requests.get(base_url,  params=params)
        if response.status_code  == 200:
            data = response.json()
            translated = data['msg']['translated']
            return translated
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"请求过程中出现异常: {e}")
        return None







