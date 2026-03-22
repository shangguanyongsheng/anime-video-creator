# 阿里百炼 视频生成对接方案

## 1. 百炼平台概述

**阿里百炼**是阿里云的一站式大模型平台，你可能已经购买的套餐中包含：

| 能力 | 模型 | 状态 |
|------|------|------|
| **文本生成** | 通义千问 | ✅ 包含 |
| **图像生成** | 通义万象 | ✅ 包含 |
| **视频生成** | 通义万象视频 | ⚠️ 需确认 |
| **语音合成** | 通义听悟 | ✅ 包含 |

### 确认视频生成能力

**步骤**：
1. 登录百炼控制台：https://bailian.console.aliyun.com
2. 点击「模型市场」
3. 搜索「视频」或「万象」
4. 查看是否有 `wanx-video` 或类似模型

---

## 2. API 对接代码

### 2.1 安装 SDK

```bash
pip install dashscope
```

### 2.2 基础调用

```python
import dashscope
from dashscope import VideoSynthesis
import os

# 设置 API Key（从百炼控制台获取）
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def generate_anime_video(
    prompt: str,
    duration: int = 5,
    style: str = "anime"
) -> str:
    """
    生成动漫风格视频

    Args:
        prompt: 视频描述
        duration: 时长（秒）
        style: 风格（anime/realistic/cartoon）

    Returns:
        视频 URL
    """
    # 优化提示词
    optimized_prompt = f"""
    {prompt}

    风格：日系动漫风格，色彩鲜艳，线条流畅
    质量：高清，流畅动画，电影级光影
    """

    # 调用 API
    response = VideoSynthesis.call(
        model="wanx-v1",  # 实际模型名以控制台为准
        prompt=optimized_prompt,
        duration=duration,
        resolution="1080p",
        style=style
    )

    if response.status_code == 200:
        return response.output.video_url
    else:
        raise Exception(f"视频生成失败: {response.message}")

# 使用示例
if __name__ == "__main__":
    video_url = generate_anime_video(
        prompt="一个动漫少女在樱花树下优雅地跳舞",
        duration=5,
        style="anime"
    )
    print(f"视频已生成: {video_url}")
```

### 2.3 异步调用（推荐）

```python
import time

def generate_video_async(prompt: str, duration: int = 5) -> str:
    """异步生成视频，适合长时间任务"""

    # 提交任务
    response = VideoSynthesis.async_call(
        model="wanx-v1",
        prompt=prompt,
        duration=duration
    )

    task_id = response.output.task_id
    print(f"任务已提交: {task_id}")

    # 轮询结果
    while True:
        result = VideoSynthesis.fetch(task_id=task_id)
        status = result.output.task_status

        if status == "SUCCEEDED":
            return result.output.video_url
        elif status == "FAILED":
            raise Exception(f"生成失败: {result.output.message}")

        print(f"生成中... ({status})")
        time.sleep(10)
```

---

## 3. 提示词优化

### 3.1 动漫风格模板

```python
ANIME_TEMPLATES = {
    "跳舞": """
        {subject}在{scene}中优雅地跳舞，
        动作流畅自然，裙摆随风飘动，
        背景光效柔和，营造梦幻氛围
    """,
    "战斗": """
        {subject}在{scene}中进行激烈的战斗，
        动作凌厉，特效华丽，
        镜头动态切换，紧张刺激
    """,
    "日常": """
        {subject}在{scene}中的日常生活片段，
        动作轻松自然，表情生动，
        画面温馨治愈
    """,
    "风景": """
        {scene}的美丽风景，
        日系动漫风格的色彩，
        光影变化细腻，氛围唯美
    """
}

def build_prompt(template_name: str, subject: str, scene: str) -> str:
    template = ANIME_TEMPLATES.get(template_name, ANIME_TEMPLATES["日常"])
    return template.format(subject=subject, scene=scene)
```

---

## 4. 如果百炼不支持视频生成

**备选方案**：

| 优先级 | 厂商 | 原因 |
|:------:|------|------|
| 1 | 阿里云视频 AI | 同生态，可复用账号 |
| 2 | Runway | API 成熟，动漫风格好 |
| 3 | 火山引擎 | 抖音生态 |

---

## 5. 费用说明

**百炼平台计费**：
- 如果你已购买套餐，可能已包含视频生成额度
- 超出部分按量计费

**查询方式**：
1. 百炼控制台 → 费用中心
2. 查看套餐包含的服务
3. 查看用量统计