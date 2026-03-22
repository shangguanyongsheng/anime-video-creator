"""
阿里云通义万象视频生成器

使用 DashScope SDK 生成视频
"""
import os
import requests
from typing import Optional
from dataclasses import dataclass
from enum import Enum

try:
    import dashscope
    from dashscope import VideoSynthesis
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False


class VideoStyle(Enum):
    """视频风格"""
    ANIME = "anime"
    REALISTIC = "realistic"
    CARTOON = "cartoon"
    THREE_D = "3d"


@dataclass
class VideoGenerationResult:
    """视频生成结果"""
    video_url: str
    duration: float
    resolution: str
    cost: float
    task_id: str


class WanxVideoGenerator:
    """通义万象视频生成器"""
    
    COST_PER_SECOND = 0.1
    MODELS = {
        "turbo": "wanx2.1-t2v-turbo",
        "plus": "wanx2.1-t2v-plus"
    }
    
    def __init__(self, api_key: Optional[str] = None, model: str = "turbo"):
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("请安装 dashscope: pip install dashscope")
        
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请提供 api_key 或设置环境变量 DASHSCOPE_API_KEY")
        
        dashscope.api_key = self.api_key
        self.model = self.MODELS.get(model, self.MODELS["turbo"])
    
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        style: VideoStyle = VideoStyle.ANIME
    ) -> VideoGenerationResult:
        """生成视频"""
        optimized_prompt = self._optimize_prompt(prompt, style)
        print(f"   提示词: {optimized_prompt[:60]}...")
        
        response = VideoSynthesis.call(
            model=self.model,
            prompt=optimized_prompt
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"视频生成失败: {response.message}")
        
        return VideoGenerationResult(
            video_url=response.output.video_url,
            duration=duration,
            resolution="720p",
            cost=duration * self.COST_PER_SECOND,
            task_id=response.output.task_id
        )
    
    def generate_anime(
        self,
        scene: str,
        subject: str = "动漫少女",
        action: str = "优雅地跳舞",
        duration: int = 5
    ) -> VideoGenerationResult:
        """快捷方法：生成动漫风格视频"""
        prompt = f"{subject}在{scene}中{action}"
        return self.generate(prompt=prompt, duration=duration, style=VideoStyle.ANIME)
    
    def _optimize_prompt(self, prompt: str, style: VideoStyle) -> str:
        """优化提示词"""
        modifiers = {
            VideoStyle.ANIME: "日系动漫风格，色彩鲜艳，线条流畅",
            VideoStyle.REALISTIC: "写实风格，真实光影",
            VideoStyle.CARTOON: "卡通风格，色彩明快",
            VideoStyle.THREE_D: "3D渲染风格"
        }
        return f"{prompt}，{modifiers.get(style, '')}"
    
    def download_video(self, video_url: str, output_path: str) -> str:
        """下载视频到本地"""
        print(f"📥 正在下载视频...")
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 视频已保存: {output_path}")
        return output_path