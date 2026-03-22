"""
阿里云通义万象视频生成器

支持：
- 文生视频
- 图生视频
- 动漫风格视频生成
"""
import os
import time
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class VideoStyle(Enum):
    """视频风格"""
    ANIME = "anime"           # 日系动漫
    REALISTIC = "realistic"   # 写实风格
    CARTOON = "cartoon"       # 卡通风格
    3D = "3d"                 # 3D 风格


class VideoResolution(Enum):
    """视频分辨率"""
    HD_720P = "720p"
    FHD_1080P = "1080p"
    QHD_2K = "2k"


@dataclass
class VideoGenerationResult:
    """视频生成结果"""
    video_url: str           # 视频 URL
    duration: float          # 视频时长（秒）
    resolution: str          # 分辨率
    cost: float              # 费用（元）
    task_id: str             # 任务 ID


class WanxVideoGenerator:
    """
    通义万象视频生成器
    
    使用方法：
        generator = WanxVideoGenerator(api_key="your-api-key")
        result = generator.generate(
            prompt="动漫少女在樱花树下跳舞",
            duration=5,
            style=VideoStyle.ANIME
        )
        print(f"视频已生成: {result.video_url}")
    """
    
    # API 端点
    API_BASE = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation"
    
    # 价格（元/秒）
    COST_PER_SECOND = 0.1
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: str = "wanx-v1"
    ):
        """
        初始化生成器
        
        Args:
            api_key: 阿里云 API Key，不传则从环境变量 DASHSCOPE_API_KEY 获取
            model: 模型名称，默认 wanx-v1
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请提供 api_key 或设置环境变量 DASHSCOPE_API_KEY")
        
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        style: VideoStyle = VideoStyle.ANIME,
        resolution: VideoResolution = VideoResolution.FHD_1080P,
        reference_image: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        wait: bool = True,
        timeout: int = 300
    ) -> VideoGenerationResult:
        """
        生成视频
        
        Args:
            prompt: 视频描述提示词
            duration: 视频时长（秒），默认 5 秒
            style: 视频风格
            resolution: 视频分辨率
            reference_image: 参考图片 URL（图生视频时使用）
            negative_prompt: 负面提示词
            wait: 是否等待生成完成
            timeout: 超时时间（秒）
        
        Returns:
            VideoGenerationResult: 生成结果
        """
        # 构建请求体
        payload = self._build_payload(
            prompt=prompt,
            duration=duration,
            style=style,
            resolution=resolution,
            reference_image=reference_image,
            negative_prompt=negative_prompt
        )
        
        # 提交任务
        task_id = self._submit_task(payload)
        print(f"✅ 任务已提交: {task_id}")
        
        if wait:
            # 等待完成
            video_url = self._wait_for_completion(task_id, timeout)
        else:
            # 返回任务 ID，让用户自己查询
            return VideoGenerationResult(
                video_url="",
                duration=duration,
                resolution=resolution.value,
                cost=0,
                task_id=task_id
            )
        
        return VideoGenerationResult(
            video_url=video_url,
            duration=duration,
            resolution=resolution.value,
            cost=duration * self.COST_PER_SECOND,
            task_id=task_id
        )
    
    def generate_anime(
        self,
        scene: str,
        subject: str = "动漫少女",
        action: str = "优雅地跳舞",
        duration: int = 5
    ) -> VideoGenerationResult:
        """
        快捷方法：生成动漫风格视频
        
        Args:
            scene: 场景描述（如：樱花树下、海边、城市街道）
            subject: 主体（如：动漫少女、武士、精灵）
            action: 动作（如：优雅地跳舞、战斗、奔跑）
            duration: 时长（秒）
        
        Returns:
            VideoGenerationResult: 生成结果
        
        Example:
            result = generator.generate_anime(
                scene="樱花树下",
                subject="动漫少女",
                action="优雅地跳舞"
            )
        """
        prompt = self._build_anime_prompt(scene, subject, action)
        return self.generate(
            prompt=prompt,
            duration=duration,
            style=VideoStyle.ANIME
        )
    
    def query_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询任务状态
        
        Args:
            task_id: 任务 ID
        
        Returns:
            任务状态信息
        """
        url = f"{self.API_BASE}/task/{task_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def download_video(
        self, 
        video_url: str, 
        output_path: str
    ) -> str:
        """
        下载视频到本地
        
        Args:
            video_url: 视频 URL
            output_path: 本地保存路径
        
        Returns:
            本地文件路径
        """
        print(f"📥 正在下载视频...")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 视频已保存: {output_path}")
        return output_path
    
    # ==================== 私有方法 ====================
    
    def _build_payload(
        self,
        prompt: str,
        duration: int,
        style: VideoStyle,
        resolution: VideoResolution,
        reference_image: Optional[str],
        negative_prompt: Optional[str]
    ) -> Dict[str, Any]:
        """构建 API 请求体"""
        # 优化提示词
        optimized_prompt = self._optimize_prompt(prompt, style)
        
        payload = {
            "model": self.model,
            "input": {
                "prompt": optimized_prompt,
                "duration": duration,
                "resolution": resolution.value
            },
            "parameters": {
                "style": style.value
            }
        }
        
        if reference_image:
            payload["input"]["reference_image"] = reference_image
        
        if negative_prompt:
            payload["input"]["negative_prompt"] = negative_prompt
        
        return payload
    
    def _optimize_prompt(self, prompt: str, style: VideoStyle) -> str:
        """优化提示词，提升生成质量"""
        style_modifiers = {
            VideoStyle.ANIME: "日系动漫风格，色彩鲜艳，线条流畅，精致细节",
            VideoStyle.REALISTIC: "写实风格，真实光影，高清细节",
            VideoStyle.CARTOON: "卡通风格，色彩明快，可爱生动",
            VideoStyle.THREE_D: "3D 渲染风格，立体感强，质感细腻"
        }
        
        quality_boosters = "高质量，流畅动画，电影级光影，专业渲染"
        
        modifier = style_modifiers.get(style, "")
        return f"{prompt}，{modifier}，{quality_boosters}"
    
    def _build_anime_prompt(
        self, 
        scene: str, 
        subject: str, 
        action: str
    ) -> str:
        """构建动漫风格提示词"""
        templates = {
            "樱花树下": "粉色樱花花瓣飘落，梦幻浪漫的氛围",
            "海边": "蔚蓝的大海和天空，阳光明媚，海浪轻拍",
            "城市街道": "现代城市背景，霓虹灯光，繁华热闹",
            "森林": "阳光穿透树叶，绿意盎然，自然清新",
            "雪山": "白雪皑皑，纯净美丽，寒冷清新的空气"
        }
        
        scene_detail = templates.get(scene, f"美丽的{scene}背景")
        
        return f"""
        {subject}在{scene}中{action}，
        {scene_detail}，
        动作流畅自然，表情生动，
        光影效果柔和，营造梦幻氛围
        """.strip().replace("\n", " ")
    
    def _submit_task(self, payload: Dict[str, Any]) -> str:
        """提交生成任务"""
        url = f"{self.API_BASE}/submission"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result["output"]["task_id"]
    
    def _wait_for_completion(
        self, 
        task_id: str, 
        timeout: int = 300
    ) -> str:
        """等待任务完成"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.query_task(task_id)
            status = result.get("output", {}).get("task_status", "UNKNOWN")
            
            if status == "SUCCEEDED":
                print(f"✅ 视频生成成功!")
                return result["output"]["video_url"]
            
            elif status == "FAILED":
                error = result.get("output", {}).get("message", "未知错误")
                raise RuntimeError(f"视频生成失败: {error}")
            
            elif status in ["PENDING", "RUNNING"]:
                print(f"⏳ 生成中... ({status})")
                time.sleep(5)
            
            else:
                print(f"⚠️ 未知状态: {status}")
                time.sleep(5)
        
        raise TimeoutError(f"视频生成超时（{timeout}秒）")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化生成器
    generator = WanxVideoGenerator()
    
    # 方式 1：使用快捷方法生成动漫视频
    result = generator.generate_anime(
        scene="樱花树下",
        subject="动漫少女",
        action="优雅地跳舞",
        duration=5
    )
    
    print(f"🎬 视频已生成: {result.video_url}")
    print(f"💰 费用: ¥{result.cost:.2f}")
    
    # 下载到本地
    generator.download_video(result.video_url, "output/anime_girl_dancing.mp4")
    
    # 方式 2：自定义提示词
    # result = generator.generate(
    #     prompt="一个穿着和服的少女在月光下弹奏古筝",
    #     duration=5,
    #     style=VideoStyle.ANIME
    # )