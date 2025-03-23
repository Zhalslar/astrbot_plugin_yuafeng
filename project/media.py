
import json
import requests
from pathlib import Path
from astrbot import logger

# 定义基础缓存路径
DATA_PATH = Path("./data/yuafeng_data")
DATA_PATH.mkdir(parents=True, exist_ok=True)

# 单独定义各个子路径
TEXT_DIR = DATA_PATH / "text"
IMAGE_DIR = DATA_PATH / "image"
VIDEO_DIR = DATA_PATH / "video"
AUDIO_DIR = DATA_PATH / "audio"
for path in [IMAGE_DIR, VIDEO_DIR, TEXT_DIR, AUDIO_DIR]:
    path.mkdir(parents=True, exist_ok=True)

TEXT_PATH = TEXT_DIR / "all_texts.json"
if not TEXT_PATH.exists():
    TEXT_PATH.write_text(json.dumps({}, ensure_ascii=False, indent=4), encoding='utf-8')

# 定义映射表
Mappings = {
    'text': {
        "社会": "shehui",
        "人生": "rensheng",
        "笑话": "xiaohua",
        "爱情": "aiqing",
        "温柔": "wenrou",
        "摆烂": "wzrjcs",
        "古诗": "gushi",
        "毒鸡汤": "djt",
        "舔狗": "tiangou",
        "情话": "twqh",
        "伤感": "shanggan",
        "骚话": "saohua",
        "英汉": "yhyl",
    },
    'image':  {
        "壁纸": "dnbz/api",
        "头像": "ecr/api",
        "手机壁纸": "bizhi",
    },
    'video': {
        "美女": "cqng",
        "姐姐": "sjxl",
        "玉足": "yzxl",
        "漫画": "mhy",
        "emo": "emo",
        "动漫": "dmxl",
        "治愈": "zyxl",
        "帅哥": "sgxl",
        "色色": "sp",
    },
    'audio': {
        "语音": "sjyy"
    }
}

yuafeng_api ="https://api.yuafeng.cn/API/"

class YuafengApiMedia:
    def __init__(self, mappings: dict):
        self.base_url = yuafeng_api
        self.mappings = mappings

    @staticmethod
    def _make_request(url, params=None):
        """
        发送GET请求

        :param url: 请求的URL地址
        :param params: 请求参数，默认为None
        :return: 响应对象或None
        """
        try:
            response = requests.get(url=url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP请求出错: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"连接错误: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"请求超时: {timeout_err}")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
        return None


    def fetch_text(self, keyword)-> str | None:
        api_keyword = self.mappings['text'].get(keyword, '')
        url = f"{self.base_url}ly/{api_keyword}.php?type=json"
        response = self._make_request(url)
        text: str = response.json().get('Msg', '')
        try:
            data = json.loads(TEXT_PATH.read_text(encoding='utf-8'))
            # 更新数据
            data.setdefault(keyword, []).append(text)
            # 写回更新后的数据
            TEXT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')
            return text
        except Exception as e:
            logger.error(f"处理文本时发生错误：{e}")
            return None

    def fetch_image(self, keyword) -> str | None:
        api_keyword = self.mappings['image'].get(keyword, None)
        url = f"{self.base_url}{api_keyword}.php"
        response = self._make_request(url)
        image: bytes = response.content
        # 确保存储图片的目录存在
        save_dir = IMAGE_DIR / keyword
        save_dir.mkdir(parents=True, exist_ok=True)
        # 计算新图片的文件名
        index = len(list(save_dir.rglob('*.jpg')))
        save_path = save_dir / f"{keyword}_{index}.jpg"
        # 保存图片到磁盘
        with open(save_path, 'wb') as f:
            f.write(image)
        return str(save_path)


    def fetch_video(self, keyword) -> str | None:
        api_keyword = self.mappings['video'].get(keyword, None)
        url = f"{self.base_url}ly/{api_keyword}.php"
        response = self._make_request(url)
        video_content: bytes = response.content
        # 确保存储视频的目录存在
        save_dir = VIDEO_DIR / keyword
        save_dir.mkdir(parents=True, exist_ok=True)
        # 计算新视频的文件名
        index = len(list(save_dir.rglob('*.mp4')))
        save_path = save_dir / f"{keyword}_{index}.mp4"
        # 保存视频到磁盘
        with open(save_path, 'wb') as f:
            f.write(video_content)
        print(f"视频已保存到：{save_path}")
        return str(save_path)


    def fetch_audio(self, keyword)-> str | None:
        api_keyword = self.mappings['audio'].get(keyword, '')
        url = f"{self.base_url}ly/{api_keyword}.php"
        response = self._make_request(url, params={"type": "json"})
        audio_url = response.json().get("Audio")
        return audio_url








