# Runway Gen-3 对接方案

## 1. 服务概述

**Runway Gen-3** 是目前 API 最成熟的视频生成服务，动漫风格支持良好。

| 属性 | 值 |
|------|-----|
| 官网 | https://runwayml.com |
| API 文档 | https://docs.runwayml.com/ |
| 定价 | $0.05/秒视频 |
| 最大时长 | 10 秒 |
| 分辨率 | 1080p |
| 动漫风格 | ⭐⭐⭐⭐ |

## 2. API 接入

### 2.1 获取 API Key

1. 注册 Runway 账号：https://runwayml.com/signup
2. 进入 Settings → API Keys
3. 生成 API Key

### 2.2 安装 SDK

```bash
pip install runwayml
```

### 2.3 基础调用示例

```python
import os
from runwayml import RunwayML

# 初始化客户端
client = RunwayML(api_key=os.getenv("RUNWAY_API_KEY"))

# 文生视频
task = client.image_to_video.create(
    model="gen3a_turbo",
    prompt_image: "https://example.com/image.jpg",  # 可选：参考图片
    prompt_text: "动漫风格少女在樱花树下跳舞，优雅的动作，粉色花瓣飘落",
    mode: "standard",
    duration: 5,
    ratio: "16:9",
    watermark: False
)

# 等待生成完成
task_id = task.id
while True:
    status = client.image_to_video.retrieve(task_id=task_id)
    if status.status == "SUCCEEDED":
        video_url = status.output[0]
        break
    elif status.status == "FAILED":
        raise Exception(status.error)
    time.sleep(10)

print(f"视频已生成: {video_url}")
```

### 2.4 动漫风格提示词模板

```python
ANIME_PROMPT_TEMPLATE = """
{scene_description},

Style: Anime, Japanese animation style, vibrant colors, 
clean lines, expressive eyes, detailed backgrounds.

Quality: High quality, smooth animation, 4K, cinematic lighting.

Motion: {motion_type}, {motion_description}
"""

def generate_anime_prompt(scene: str, motion_type: str = "graceful"):
    motion_templates = {
        "graceful": "elegant and fluid movements",
        "dynamic": "fast-paced action scenes",
        "subtle": "gentle and subtle movements",
        "dramatic": "dramatic and impactful moments"
    }
    return ANIME_PROMPT_TEMPLATE.format(
        scene_description=scene,
        motion_type=motion_type,
        motion_description=motion_templates.get(motion_type, "natural movements")
    )
```

## 3. Python 封装

### 3.1 统一接口封装

```python
# video_generator/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoGenerationResult:
    video_url: str
    duration: float
    resolution: str
    cost: float

class VideoGenerator(ABC):
    @abstractmethod
    def generate(
        self, 
        prompt: str, 
        duration: int = 5,
        style: str = "anime",
        reference_image: Optional[str] = None
    ) -> VideoGenerationResult:
        pass

# video_generator/runway.py
from runwayml import RunwayML
import time

class RunwayGenerator(VideoGenerator):
    def __init__(self, api_key: str):
        self.client = RunwayML(api_key=api_key)
        self.cost_per_second = 0.05
    
    def generate(
        self, 
        prompt: str, 
        duration: int = 5,
        style: str = "anime",
        reference_image: Optional[str] = None
    ) -> VideoGenerationResult:
        # 优化提示词
        optimized_prompt = self._optimize_prompt(prompt, style)
        
        # 调用 API
        task = self.client.image_to_video.create(
            model="gen3a_turbo",
            prompt_text=optimized_prompt,
            prompt_image=reference_image,
            duration=duration,
            ratio="16:9",
            watermark=False
        )
        
        # 等待完成
        video_url = self._wait_for_completion(task.id)
        
        return VideoGenerationResult(
            video_url=video_url,
            duration=duration,
            resolution="1080p",
            cost=duration * self.cost_per_second
        )
    
    def _optimize_prompt(self, prompt: str, style: str) -> str:
        style_modifiers = {
            "anime": "Anime style, Japanese animation, vibrant colors",
            "realistic": "Photorealistic, cinematic, high detail",
            "cartoon": "Cartoon style, bold colors, stylized"
        }
        modifier = style_modifiers.get(style, "")
        return f"{prompt}, {modifier}"
    
    def _wait_for_completion(self, task_id: str, timeout: int = 300) -> str:
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.client.image_to_video.retrieve(task_id=task_id)
            if status.status == "SUCCEEDED":
                return status.output[0]
            elif status.status == "FAILED":
                raise Exception(f"Runway generation failed: {status.error}")
            time.sleep(5)
        raise TimeoutError("Video generation timed out")
```

## 4. 成本估算

| 项目 | 价格 |
|------|------|
| 标准质量 | $0.05/秒 |
| 高质量 | $0.10/秒 |
| 5 秒视频 | $0.25 - $0.50 |
| 100 个视频/月 | $25 - $50 |

## 5. 限制与注意事项

1. **时长限制**：单次最长 10 秒，需拼接长视频
2. **网络要求**：国内需要代理访问
3. **并发限制**：免费版并发 1，付费版可提升
4. **水印**：API 调用默认无水印

## 6. 最佳实践

### 6.1 提示词优化
- 添加风格关键词：`anime style, Japanese animation`
- 添加质量词：`high quality, 4K, smooth animation`
- 明确动作描述：`graceful dancing, flowing hair`

### 6.2 错误处理
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_with_retry(prompt: str, **kwargs):
    return generator.generate(prompt, **kwargs)
```

### 6.3 视频拼接
```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concat_runway_videos(video_urls: list[str]) -> str:
    clips = [VideoFileClip(url) for url in video_urls]
    final = concatenate_videoclips(clips)
    output_path = "output/combined.mp4"
    final.write_videofile(output_path)
    return output_path
```