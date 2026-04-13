---
name: naja-api
description: 提供 naja 系统 API 端点的调用能力，方便用户通过 curl 或其他工具获取系统数据和状态。
---

# Naja API Skill

提供 naja 系统各模块 API 端点的调用能力，方便用户通过 curl 或其他工具获取系统数据和状态。

## 功能特性

- **认知系统 API**: 记忆报告、主题信号、注意力提示、思想报告
- **市场热点 API**: 市场状态、热点详情、**A股+美股双市场热点**
- **系统监控 API**: 系统状态、模块状态
- **雷达系统 API**: 雷达事件
- **Bandit 系统 API**: 决策统计
- **数据源和策略 API**: 数据源列表、策略列表
- **智慧系统 API**: 阿那亚觉醒状态

## API 端点列表

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/cognition/memory` | GET | 获取认知系统记忆报告 |
| `/api/cognition/topics` | GET | 获取认知系统主题信号 |
| `/api/cognition/attention` | GET | 获取认知系统注意力提示 |
| `/api/cognition/thought` | GET | 获取认知系统思想报告 |
| `/api/market/state` | GET | 获取市场状态 |
| `/api/market/hotspot` | GET | 获取 A股+美股双市场热点 |
| `/api/market/hotspot/details` | GET | 获取市场热点详情 |
| `/api/system/status` | GET | 获取系统状态 |
| `/api/system/modules` | GET | 获取系统模块状态 |
| `/api/radar/events` | GET | 获取雷达事件 |
| `/api/bandit/stats` | GET | 获取 Bandit 决策统计 |
| `/api/datasource/list` | GET | 获取数据源列表 |
| `/api/strategy/list` | GET | 获取策略列表 |
| `/api/alaya/status` | GET | 获取阿那亚觉醒状态 |

## 使用方法

### 1. 基本 curl 调用

```bash
# 获取认知系统记忆报告
curl http://localhost:8080/api/cognition/memory

# 获取双市场热点（A股+美股）
curl http://localhost:8080/api/market/hotspot

# 获取市场状态
curl http://localhost:8080/api/market/state

# 获取系统状态
curl http://localhost:8080/api/system/status

# 获取雷达事件
curl http://localhost:8080/api/radar/events
```

### 2. 带参数调用

```bash
# 获取认知系统主题信号（指定回溯数量）
curl "http://localhost:8080/api/cognition/topics?lookback=100"

# 获取认知系统注意力提示（指定回溯数量）
curl "http://localhost:8080/api/cognition/attention?lookback=300"
```

### 3. 格式化输出

```bash
# 使用 jq 格式化 JSON 输出
curl -s http://localhost:8080/api/market/hotspot | jq

# 只查看美股热点
curl -s http://localhost:8080/api/market/hotspot | jq '.us'

# 只查看美股热门股票
curl -s http://localhost:8080/api/market/hotspot | jq '.us.hot_stocks'
```

## 双市场热点 API 响应格式

`/api/market/hotspot` 返回 A股 和美股 的双市场数据：

```json
{
  "cn": {
    "hot_blocks": [
      {"block_id": "AI医疗", "name": "AI医疗", "weight": 0.85}
    ],
    "hot_stocks": [
      {"symbol": "sh600519", "name": "贵州茅台", "weight": 0.92}
    ],
    "market_hotspot": 0.74,
    "market_activity": 0.80
  },
  "us": {
    "hot_blocks": [
      {"block_id": "cloud_ai", "name": "cloud_ai", "weight": 0.61}
    ],
    "hot_stocks": [
      {"symbol": "nvda", "name": "nvda", "weight": 1.35, "change_pct": 4.68}
    ],
    "market_hotspot": 0.74,
    "market_activity": 0.80
  },
  "system_status": "running",
  "processed_snapshots": 120
}
```

## 通用响应格式

所有 API 端点返回统一的 JSON 格式：

```json
{
  "timestamp": 1713000000.0,
  "datetime": "2026-04-13 12:00:00",
  "success": true,
  "data": {
    // 具体数据内容
  }
}
```

## 错误处理

当 API 调用失败时，返回格式为：

```json
{
  "timestamp": 1713000000.0,
  "datetime": "2026-04-13 12:00:00",
  "success": false,
  "error": "错误信息"
}
```

## 系统要求

- Naja 系统已启动并运行在端口 8080
- 网络连接正常
- 系统各模块已初始化

## 常见问题

### Q: 为什么返回 "模块未初始化" 错误？
A: 可能是系统刚启动，各模块还未完全初始化。请等待一段时间后重试。

### Q: 如何检查系统是否正常运行？
A: 可以先调用 `/api/system/status` 端点检查系统整体状态。

### Q: API 响应时间过长怎么办？
A: 对于数据量较大的端点（如 `/api/cognition/memory`），响应时间可能会稍长，请耐心等待。

### Q: 美股数据为什么是空的？
A: 美股数据通过新浪 API 获取，首次请求可能需要等待 aiohttp 超时后自动 fallback 到 requests（约 30 秒）。

## 示例脚本

### 1. 监控系统状态

```bash
#!/bin/bash

while true; do
  echo "$(date) - 系统状态检查"
  curl -s http://localhost:8080/api/system/status | jq '.data.overall'
  sleep 60
done
```

### 2. 定期获取双市场热点

```bash
#!/bin/bash

while true; do
  echo "$(date) - 双市场热点检查"
  curl -s http://localhost:8080/api/market/hotspot | jq '{cn_hotspot: .cn.market_hotspot, us_hotspot: .us.market_hotspot, cn_blocks: [.cn.hot_blocks[].block_id], us_blocks: [.us.hot_blocks[].block_id]}'
  sleep 300
done
```

### 3. 导出认知系统数据

```bash
#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
curl -s http://localhost:8080/api/cognition/memory > "cognition_memory_${TIMESTAMP}.json"
echo "数据已导出到 cognition_memory_${TIMESTAMP}.json"
```

## 注意事项

- API 端点返回的数据可能会根据系统状态和配置有所不同
- 对于高频调用，建议适当控制请求频率，避免对系统造成过大负担
- 部分 API 端点可能需要较长时间处理，特别是首次调用时
- 如遇到问题，请检查系统日志获取详细信息
