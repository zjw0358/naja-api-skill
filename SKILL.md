---
name: naja-api
description: 提供 naja 系统 API 端点的调用能力，方便用户通过 curl 或其他工具获取系统数据和状态。
---

# Naja API Skill

提供 naja 系统各模块 API 端点的调用能力，方便用户通过 curl 或其他工具获取系统数据和状态。

## 功能特性

- **认知系统 API**: 记忆报告、主题信号、注意力提示、思想报告
- **市场热点 API**: 市场状态、热点详情、**A股+美股双市场热点**
- **Attention 系统 API**: 末那识决策、和谐度、信念验证、持仓跟踪、盲区发现、融合信号
- **系统监控 API**: 系统状态、模块状态
- **雷达系统 API**: 雷达事件
- **Bandit 系统 API**: 决策统计
- **数据源和策略 API**: 数据源列表、策略列表
- **智慧系统 API**: 阿那亚觉醒状态

## API 端点列表（共 34 个）

### 认知系统（4 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/cognition/memory` | GET | 获取认知系统记忆报告 |
| `/api/cognition/topics` | GET | 获取认知系统主题信号 |
| `/api/cognition/attention` | GET | 获取认知系统注意力提示 |
| `/api/cognition/thought` | GET | 获取认知系统思想报告 |

### 市场热点（3 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/market/state` | GET | 获取市场状态 |
| `/api/market/hotspot` | GET | 获取 A股+美股双市场热点 |
| `/api/market/hotspot/details` | GET | 获取市场热点详情 |

### Attention 系统 — P0 核心决策（6 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/attention/manas/state` | GET | 末那识引擎状态（manas_score, timing_score, regime_score, confidence, risk_temperature, should_act） |
| `/api/attention/harmony` | GET | 注意力和谐度（harmony_strength, harmony_state, should_act） |
| `/api/attention/decision` | GET | 交易决策（fused_confidence, manas_score, bias_state, awakening_level） |
| `/api/attention/conviction` | GET | 信念验证（conviction_score, consensus_blocks, divergence_blocks, blind_spots） |
| `/api/attention/conviction/timing` | GET | 时机信号（timing_good/timing_hot/timing_wait） |
| `/api/attention/conviction/should-add` | GET | 是否应该加仓（should_add, reason） |

### Attention 系统 — P1 持仓与跟踪（4 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/attention/portfolio/summary` | GET | 持仓汇总（holdings, watchlist, block_alloc, industry_alloc） |
| `/api/attention/position/metrics` | GET | 持仓指标（return_pct, volatility, price_velocity, max_favorable/adverse_move） |
| `/api/attention/tracking/hotspot` | GET | 热点信号跟踪列表 |
| `/api/attention/tracking/stats` | GET | 跟踪统计（tracking_count, avg_return, win_rate） |

### Attention 系统 — P2 发现与融合（4 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/attention/blind-spots` | GET | 盲区发现（root_cause, resolvers, recommendation） |
| `/api/attention/fusion` | GET | 注意力融合信号（共识/分歧/盲区、时机信号） |
| `/api/attention/focus` | GET | 关注焦点（叙事、题材、股票列表） |
| `/api/attention/narrative-block-matrix` | GET | 叙事-题材关联矩阵 |

### Attention 系统 — P3 状态与报告（6 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/attention/report` | GET | 注意力系统完整报告 |
| `/api/attention/lab/status` | GET | 实验室状态（kernel, awakening, volatility_surface） |
| `/api/attention/liquidity` | GET | 流动性状态（total_value, cash, position_value, daily_pnl） |
| `/api/attention/strategy/top-symbols` | GET | 策略权重最高股票（支持 ?n=20） |
| `/api/attention/strategy/top-blocks` | GET | 策略权重最高题材（支持 ?n=10） |
| `/api/attention/context` | GET | 注意力上下文（awakening_level, volatility_surface, contradiction） |

### 系统监控（2 个）

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/system/status` | GET | 获取系统状态 |
| `/api/system/modules` | GET | 获取系统模块状态 |

### 其他（5 个）

| 端点 | 方法 | 描述 |
|------|------|------|
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

# 获取末那识决策状态
curl http://localhost:8080/api/attention/manas/state

# 获取和谐度
curl http://localhost:8080/api/attention/harmony

# 获取信念验证
curl http://localhost:8080/api/attention/conviction

# 获取时机信号
curl http://localhost:8080/api/attention/conviction/timing

# 获取持仓汇总
curl http://localhost:8080/api/attention/portfolio/summary

# 获取盲区发现
curl http://localhost:8080/api/attention/blind-spots

# 获取注意力上下文
curl http://localhost:8080/api/attention/context

# 获取系统状态
curl http://localhost:8080/api/system/status
```

### 2. 带参数调用

```bash
# 获取认知系统主题信号（指定回溯数量）
curl "http://localhost:8080/api/cognition/topics?lookback=100"

# 获取策略权重前20股票
curl "http://localhost:8080/api/attention/strategy/top-symbols?n=20"

# 获取策略权重前10题材
curl "http://localhost:8080/api/attention/strategy/top-blocks?n=10"
```

### 3. 格式化输出

```bash
# 使用 jq 格式化 JSON 输出
curl -s http://localhost:8080/api/market/hotspot | jq

# 只查看美股热点
curl -s http://localhost:8080/api/market/hotspot | jq '.us'

# 只查看末那识核心指标
curl -s http://localhost:8080/api/attention/manas/state | jq '.data | {manas_score, timing_score, confidence, should_act}'

# 只查看和谐度
curl -s http://localhost:8080/api/attention/harmony | jq '.data'
```

### 4. Python 客户端

```bash
# 末那识状态
python scripts/api_client.py manas-state

# 双市场热点
python scripts/api_client.py market-hotspot

# 信念验证
python scripts/api_client.py conviction

# 持仓汇总
python scripts/api_client.py portfolio-summary

# 注意力上下文
python scripts/api_client.py attention-context --output text
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

## Attention API 响应格式

所有 Attention 端点返回统一格式：

```json
{
  "success": true,
  "data": {
    // 具体数据内容
  }
}
```

错误时：

```json
{
  "success": false,
  "error": "模块未初始化"
}
```

## 系统要求

- Naja 系统已启动并运行在端口 8080
- 网络连接正常
- 系统各模块已初始化（部分 Attention 端点需要完整启动模式）

## 常见问题

### Q: 为什么返回 "模块未初始化" 错误？
A: 部分高级 Attention 端点（conviction、blind-spots、fusion 等）依赖 `attention_integration` 模块，需要在完整启动模式下使用。

### Q: 如何检查系统是否正常运行？
A: 可以先调用 `/api/system/status` 端点检查系统整体状态。

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

### 3. 监控末那识决策

```bash
#!/bin/bash
while true; do
  echo "$(date) - 末那识决策检查"
  curl -s http://localhost:8080/api/attention/manas/state | jq '.data | {manas_score, timing_score, confidence, should_act, harmony_state}'
  curl -s http://localhost:8080/api/attention/harmony | jq '.data'
  sleep 60
done
```

### 4. 监控信念验证

```bash
#!/bin/bash
while true; do
  echo "$(date) - 信念验证检查"
  curl -s http://localhost:8080/api/attention/conviction | jq '.data'
  curl -s http://localhost:8080/api/attention/conviction/timing | jq '.data'
  sleep 120
done
```

## 注意事项

- API 端点返回的数据可能会根据系统状态和配置有所不同
- 对于高频调用，建议适当控制请求频率，避免对系统造成过大负担
- 部分 API 端点可能需要较长时间处理，特别是首次调用时
- 如遇到问题，请检查系统日志获取详细信息
