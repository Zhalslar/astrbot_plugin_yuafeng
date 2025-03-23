import os

from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig
from astrbot.core.message.components import Video, Record
from astrbot.core.platform import AstrMessageEvent
from .project.media import Mappings, YuafengApiMedia
from .project.query_ip import fetch_ip_info
from .project.stickerSearch import search_stickers
from .project.translator import translate_text

API = YuafengApiMedia(mappings=Mappings)
text_keywords = set(Mappings.get('text', {}).keys())
image_keywords = set(Mappings.get('image', {}).keys())
video_keywords = set(Mappings.get('video', {}).keys())
audio_keywords = set(Mappings.get('audio', {}).keys())

@register("对接枫林API", "Zhalslar", "枫林插件", "1.0.0", "https://github.com/Zhalslar/astrbot_plugin_yuafeng")
class YuafengAPI(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.save_text = self.config.get('media_config', {}).get('save_text', False)
        self.save_image = self.config.get('media_config', {}).get('save_image', False)
        self.save_video = self.config.get('media_config', {}).get('save_video', False)
        self.save_audio = self.config.get('media_config', {}).get('save_audio', False)


    @filter.regex(r'(' + '|'.join(text_keywords) + r')', desc="匹配文案关键词")
    async def handle_writing(self, event: AstrMessageEvent):
        keyword = next((k for k in text_keywords if k in event.get_message_str()), None)
        if text := API.fetch_text(keyword=keyword):
            yield event.plain_result(text)

    @filter.regex(r'(' + '|'.join(image_keywords) + r')',desc="匹配图片关键词")
    async def handle_image(self, event: AstrMessageEvent):
        keyword = next((k for k in image_keywords if k in event.get_message_str()), None)
        if image_path := API.fetch_image(keyword=keyword):
            yield event.image_result(image_path)
        if not self.save_image:
            os.remove(image_path)

    @filter.regex(r'(' + '|'.join(video_keywords) + r')',desc="匹配视频关键词")
    async def handle_video(self, event: AstrMessageEvent):
        keyword = next((k for k in video_keywords if k in event.get_message_str()), None)
        if video_path := API.fetch_video(keyword=keyword):
            file = Video.fromFileSystem(video_path)
            yield event.chain_result([file])
        if not self.save_video:
            os.remove(video_path)


    @filter.regex(r'(' + '|'.join(audio_keywords) + r')',desc="匹配音频关键词")
    async def handle_audio(self, event: AstrMessageEvent):
        keyword = next((k for k in audio_keywords if k in event.get_message_str()), None)
        if file_path := API.fetch_audio(keyword=keyword):
            record = Record.fromURL(file_path)
            yield event.chain_result([record])

    @filter.command("翻译", desc="翻译文本")
    async def translate_handler(self, event: AstrMessageEvent, text: str = None):
        if not text:
            text = event.get_message_str()
        translated = translate_text(text)
        if translated:
            yield event.plain_result(translated)

    @filter.command("查ip",desc="查询ip对应的实际地址")
    async def handle_query(self, event: AstrMessageEvent, input_ip: str = None):
        """提取用户输入的IP地址（支持无参数查询本机）"""
        result = await fetch_ip_info(input_ip if input_ip else None)
        if result:
            yield event.plain_result(result)

    @filter.command("搜表情")
    async def handle_query(self, event: AstrMessageEvent, keyword: str = None):
        """根据关键词搜索QQ表情"""
        result = await search_stickers(keyword)
        if result:
            yield event.plain_result(result)
