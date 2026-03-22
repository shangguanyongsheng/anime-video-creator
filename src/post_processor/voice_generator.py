"""
配音生成器

使用 Edge TTS 生成配音（免费）
"""
import asyncio
import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class VoiceType(Enum):
    """配音声音类型"""
    # 中文女声
    ZH_FEMALE_GENTLE = "zh-CN-XiaoxiaoNeural"        # 温柔女声
    ZH_FEMALE_SWEET = "zh-CN-XiaoyiNeural"           # 甜美女声
    ZH_FEMALE_ANGRY = "zh-CN-liaoning-XiaobeiNeural" # 活泼女声
    
    # 中文男声
    ZH_MALE_GENTLE = "zh-CN-YunxiNeural"             # 温柔男声
    ZH_MALE_DEEP = "zh-CN-YunyangNeural"             # 深沉男声
    
    # 日语女声（适合动漫）
    JA_FEMALE_ANIME = "ja-JP-NanamiNeural"           # 日语女声
    
    # 英文
    EN_FEMALE = "en-US-JennyNeural"
    EN_MALE = "en-US-GuyNeural"


@dataclass
class VoiceResult:
    """配音生成结果"""
    success: bool
    audio_path: str = ""
    duration: float = 0.0
    error: str = ""


class VoiceGenerator:
    """
    配音生成器
    
    使用方法：
        generator = VoiceGenerator()
        result = generator.generate(
            text="在樱花树下，一位少女轻盈地跳舞",
            output_path="output/voice.mp3"
        )
    """
    
    def __init__(self):
        """初始化配音生成器"""
        try:
            import edge_tts
            self.edge_tts = edge_tts
        except ImportError:
            raise ImportError("请安装 edge-tts: pip install edge-tts")
    
    def generate(
        self,
        text: str,
        output_path: str,
        voice: VoiceType = VoiceType.ZH_FEMALE_GENTLE,
        rate: str = "+0%",
        volume: str = "+0%"
    ) -> VoiceResult:
        """
        生成配音
        
        Args:
            text: 要转换的文字
            output_path: 输出音频路径
            voice: 声音类型
            rate: 语速调整（如 "+20%" 或 "-10%"）
            volume: 音量调整
        
        Returns:
            VoiceResult: 生成结果
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 使用 edge-tts 生成音频
            communicate = self.edge_tts.Communicate(
                text=text,
                voice=voice.value,
                rate=rate,
                volume=volume
            )
            
            # 同步保存音频
            asyncio.run(communicate.save(output_path))
            
            # 获取音频时长
            duration = self._get_audio_duration(output_path)
            
            return VoiceResult(
                success=True,
                audio_path=output_path,
                duration=duration
            )
            
        except Exception as e:
            return VoiceResult(
                success=False,
                error=str(e)
            )
    
    def generate_anime_narration(
        self,
        scene: str,
        action: str,
        output_path: str
    ) -> VoiceResult:
        """
        快捷方法：生成动漫解说配音
        
        Args:
            scene: 场景描述
            action: 动作描述
            output_path: 输出路径
        
        Returns:
            VoiceResult: 生成结果
        """
        # 生成解说文本
        text = f"在{scene}，{action}。"
        
        return self.generate(
            text=text,
            output_path=output_path,
            voice=VoiceType.ZH_FEMALE_GENTLE,
            rate="-10%"  # 稍慢，适合解说
        )
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """获取音频时长（秒）"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(audio_path)
            return len(audio) / 1000.0
        except:
            # 如果没有 pydub，返回估算值（约每秒 3 个字）
            return 0.0


# ==================== 使用示例 ====================

if __name__ == "__main__":
    generator = VoiceGenerator()
    
    # 生成配音
    result = generator.generate(
        text="在樱花树下，一位动漫少女正在优雅地跳舞。粉色的花瓣随风飘落，营造出浪漫的氛围。",
        output_path="output/voice.mp3",
        voice=VoiceType.ZH_FEMALE_GENTLE
    )
    
    if result.success:
        print(f"✅ 配音已生成: {result.audio_path}")
        print(f"   时长: {result.duration:.1f}秒")
    else:
        print(f"❌ 生成失败: {result.error}")