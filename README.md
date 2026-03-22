# 🎬 动漫短视频 AI 创作工具

> AI 驱动的动漫短视频自动生成方案研究

## 项目背景

基于抖音、B站等平台的动漫短视频需求，探索 AI 辅助创作的技术方案。

## 核心能力

### 1. 视频生成能力
- 脚本生成（LLM）
- 配音生成（TTS）
- 素材匹配（图库/视频库 API）
- 视频合成（FFmpeg）
- 字幕生成

### 2. 动漫风格支持
- 二次元风格转换
- 动漫角色一致性
- 表情/动作生成

### 3. 自动化流程
- 热点发现 → 脚本 → 素材 → 配音 → 成片
- 批量生产
- 多平台分发

## 技术栈

| 组件 | 方案 |
|------|------|
| 语音识别 | WhisperX |
| TTS | Edge TTS / GPT-SoVITS |
| LLM | GPT-4o / Claude / 通义千问 |
| 视频处理 | FFmpeg + MoviePy |
| 素材源 | Pexels / Pixabay / 阿里云素材库 |
| 图像生成 | DALL-E 3 / Stable Diffusion / Midjourney |

## 参考项目

| 项目 | Stars | 定位 | 链接 |
|------|-------|------|------|
| VideoLingo | 16.2k | Netflix 级字幕翻译配音 | [GitHub](https://github.com/Huanshere/VideoLingo) |
| FireRed-OpenStoryline | 1.2k | 对话式视频编辑 | [GitHub](https://github.com/FireRedTeam/FireRed-OpenStoryline) |
| YumCut | 713 | 短视频一键生成 | [GitHub](https://github.com/IgorShadurin/app.yumcut.com) |
| Director | 1.3k | AI 视频代理框架 | [GitHub](https://github.com/video-db/Director) |

## 文档目录

- [AI 视频创作助手分析](./docs/ai-video-creator-analysis.md) - GitHub 项目调研
- [视频平台趋势分析](./docs/video-platform-trends.md) - 抖音/YouTube 热门内容
- [厂商能力调研](./docs/ai-video-vendors.md) - 各大厂商 AI 视频能力（待补充）

## 快速开始

```bash
# 安装依赖
pip install ffmpeg-python moviepy openai whisperx edge-tts

# 运行示例
python scripts/generate_video.py --topic "动漫角色盘点" --style anime
```

## 许可证

MIT License