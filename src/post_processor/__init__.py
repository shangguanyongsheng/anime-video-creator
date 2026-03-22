"""
视频后处理模块

支持：
- 配音生成（Edge TTS）
- 字幕生成（SRT）
- 视频合并（FFmpeg）
"""
from .voice_generator import VoiceGenerator
from .subtitle_generator import SubtitleGenerator
from .video_composer import VideoComposer

__all__ = ["VoiceGenerator", "SubtitleGenerator", "VideoComposer"]