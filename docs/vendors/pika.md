# Pika 对接方案

## 1. 服务概述

**Pika** 是专注于动漫风格的视频生成服务，二次元效果最佳。

| 属性 | 值 |
|------|-----|
| 官网 | https://pika.art |
| API 文档 | https://pika.art/docs |
| 定价 | 按量计费 |
| 最大时长 | 5 秒 |
| 分辨率 | 1080p |
| 动漫风格 | ⭐⭐⭐⭐⭐ |

## 2. API 接入

### 2.1 获取访问权限

1. 注册 Pika 账号
2. 申请 API 访问权限（目前有限开放）
3. 获取 API Key

### 2.2 基础调用示例

```python
import requests

API_URL = "https://api.pika.art/v1/generate"
headers = {"Authorization": f"Bearer {PIKA_API_KEY}"}

response = requests.post(
    API_URL,
    headers=headers,
    json={
        "prompt": "Anime girl dancing under cherry blossom tree",
        "style": "anime",
        "duration": 5,
        "aspect_ratio": "16:9"
    }
)

task_id = response.json()["task_id"]

# 查询结果
result = requests.get(
    f"https://api.pika.art/v1/tasks/{task_id}",
    headers=headers
)
video_url = result.json()["video_url"]
```

## 3. 动漫风格优势

### 3.1 风格模板
- 日系动漫
- 韩系动漫
- 美式卡通
- 水彩风格

### 3.2 角色一致性
```python
# 保持角色一致
response = requests.post(
    API_URL,
    headers=headers,
    json={
        "prompt": "Same anime girl walking in a park",
        "character_reference": "char_abc123",  # 角色 ID
        "style": "anime"
    }
)
```

## 4. 适用场景

- 二次元短视频
- 动漫角色创作
- 风格化视频内容

## 5. 注意事项

1. **时长限制**：单次最长 5 秒，需要拼接
2. **API 开放有限**：需要申请
3. **适合动漫风格**：真人效果一般