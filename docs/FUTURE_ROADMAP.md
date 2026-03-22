# Simple BI Agent - 未来规划路线图

> 最后更新: 2026-03-22

---

## 🚀 v5.0 规划方向

### 1. 儿童绘本故事视频生成器

**项目定位**: 基于 Simple BI Agent 的 AI 能力，扩展儿童内容创作方向

**核心流程**:
```
故事文本输入
     ↓
AI 分镜脚本生成 (Claude/Qwen)
     ↓
AI 插图生成 (通义万相/Midjourney)
     ↓
配音合成 (阿里云 TTS)
     ↓
视频合成 (FFmpeg)
     ↓
儿童绘本视频输出
```

**技术栈**:
- LLM: 阿里云 Qwen / Claude
- 图像生成: 通义万相 API
- 配音: 阿里云语音合成
- 视频: FFmpeg + MoviePy

**目标用户**:
- 有 3-8 岁小孩的家庭
- 幼儿园/早教机构
- 儿童内容创作者

**变现模式**:
- 小程序订阅: 9.9元/月
- 单视频生成: 1.9元/次
- 批量生成套餐

**开发阶段**:
- [ ] Phase 1: 分镜脚本生成模块
- [ ] Phase 2: 集成通义万相绘图
- [ ] Phase 3: TTS 配音集成
- [ ] Phase 4: 视频合成模块
- [ ] Phase 5: 小程序前端

---

### 2. AI 平台免费额度聚合监控

**项目定位**: 监控各 AI 平台免费额度，帮助用户省钱

**监控平台**:

| 平台 | 免费额度 | 刷新周期 | API |
|------|---------|---------|-----|
| Groq | 无限制 | - | OpenAI 兼容 |
| 百度千帆 | 5万次/天 | 每日 | REST API |
| 阿里云 DashScope | 2小时/月 | 每月 | REST API |
| Google AI Studio | 免费 | - | Gemini API |
| Hugging Face | 免费 | - | Inference API |
| Claude (Anthropic) | $5 额度 | 一次性 | REST API |
| OpenAI | $18 新用户 | 一次性 | REST API |
| 智谱 AI (GLM) | 免费额度 | 每日 | REST API |

**核心功能**:
- 自动检测账号剩余额度
- 每日推送「可用免费资源清单」
- 网页仪表盘实时展示
- 额度预警提醒

**技术架构**:
```
定时任务 (Cron)
     ↓
各平台 API 轮询
     ↓
额度数据聚合
     ↓
存储 (SQLite/Redis)
     ↓
推送 (QQ Bot / 邮件 / Web)
```

**输出示例**:
```
📊 今日 AI 免费资源清单

✅ Groq: 无限制，推荐使用 Whisper
✅ 百度千帆: 剩余 49,823 次
⚠️ 阿里云: 剩余 1.2 小时 (本月)
✅ Google AI Studio: Gemini Pro 免费
⚠️ Claude: 新用户 $5 额度待领取

💡 今日推荐: 用 Groq Whisper 做语音识别
```

**开发阶段**:
- [ ] Phase 1: 各平台 API 接入
- [ ] Phase 2: 数据存储和展示
- [ ] Phase 3: 定时推送集成
- [ ] Phase 4: Web 仪表盘
- [ ] Phase 5: 多账号管理

---

## 📋 优先级排序

| 项目 | 价值 | 难度 | 优先级 |
|------|------|------|--------|
| 免费额度监控 | ⭐⭐⭐⭐ | ⭐⭐ | **P0** 先做 |
| 儿童绘本视频 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **P1** 紧随 |

---

## 🔗 相关资源

- [AI 视频创作分析](../../ai-agent-research/docs/market-research/ai-video-creator-analysis.md)
- [多Agent协作调研](../../ai-agent-research/docs/多Agent协作社区调研报告.md)
- [ClawHub 技能市场](https://clawhub.com)

---

*此文档记录项目未来发展方向，定期更新*
