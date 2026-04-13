# Naja API Skill

> Naja 系统的完整 API 接口层，提供 **34 个 REST 端点**，覆盖认知、市场、注意力决策、持仓跟踪、盲区发现等全部核心能力。

## 快速开始

```bash
# 1. 启动 Naja
python -m deva.naja --news-radar-sim --port 8080

# 2. 检查系统状态
curl -s http://localhost:8080/api/system/status | jq '.data.overall'
# → "🟢 正常"

# 3. 获取双市场热点
curl -s http://localhost:8080/api/market/hotspot | jq '{cn: .cn.market_hotspot, us: .us.market_hotspot}'

# 4. 查看注意力决策
curl -s http://localhost:8080/api/attention/context | jq '.data'
```

## 安装

```bash
# 克隆到 SOLO skills 目录
git clone https://github.com/zjw0358/naja-api-skill.git

# Python 客户端依赖
pip install requests
```

## 34 个 API 端点一览

### 认知系统（4 个）— Naja 在想什么

| 端点 | 描述 |
|------|------|
| `GET /api/cognition/memory` | 记忆报告（短期/中期/长期记忆） |
| `GET /api/cognition/topics` | 主题信号（叙事话题 + 关注度） |
| `GET /api/cognition/attention` | 注意力提示（用户关注焦点） |
| `GET /api/cognition/thought` | 思想报告 |

### 市场热点（3 个）— 哪些在涨

| 端点 | 描述 |
|------|------|
| `GET /api/market/hotspot` | **A股+美股双市场热点**（题材权重 + 热门股票） |
| `GET /api/market/state` | 市场状态（聚焦度、活跃度、趋势） |
| `GET /api/market/hotspot/details` | 热点详情 |

### Attention P0 核心决策（6 个）— 系统的判断

| 端点 | 描述 |
|------|------|
| `GET /api/attention/manas/state` | 末那识状态（manas_score, timing, confidence, should_act） |
| `GET /api/attention/harmony` | 和谐度（harmony_strength, harmony_state） |
| `GET /api/attention/decision` | 交易决策（fused_confidence, bias_state） |
| `GET /api/attention/conviction` | 信念验证（conviction_score, consensus, blind_spots） |
| `GET /api/attention/conviction/timing` | 时机信号（timing_good / timing_hot / timing_wait） |
| `GET /api/attention/conviction/should-add` | 是否加仓（should_add + reason） |

### Attention P1 持仓跟踪（4 个）— 持仓监控

| 端点 | 描述 |
|------|------|
| `GET /api/attention/portfolio/summary` | 持仓汇总（holdings, watchlist, block_alloc） |
| `GET /api/attention/position/metrics` | 持仓指标（return_pct, volatility, max_move） |
| `GET /api/attention/tracking/hotspot` | 热点信号跟踪列表 |
| `GET /api/attention/tracking/stats` | 跟踪统计（avg_return, win_rate） |

### Attention P2 发现融合（4 个）— 发现盲区

| 端点 | 描述 |
|------|------|
| `GET /api/attention/blind-spots` | 盲区发现（root_cause, resolvers） |
| `GET /api/attention/fusion` | 融合信号（共识/分歧/盲区） |
| `GET /api/attention/focus` | 关注焦点（叙事、题材、股票） |
| `GET /api/attention/narrative-block-matrix` | 叙事-题材关联矩阵 |

### Attention P3 状态报告（6 个）— 系统全景

| 端点 | 描述 |
|------|------|
| `GET /api/attention/context` | 注意力上下文（awakening, volatility, contradiction） |
| `GET /api/attention/report` | 完整注意力报告 |
| `GET /api/attention/lab/status` | 实验室状态 |
| `GET /api/attention/liquidity` | 流动性（total_value, cash, daily_pnl） |
| `GET /api/attention/strategy/top-symbols` | 策略权重最高股票 `?n=20` |
| `GET /api/attention/strategy/top-blocks` | 策略权重最高题材 `?n=10` |

### 系统 & 其他（7 个）

| 端点 | 描述 |
|------|------|
| `GET /api/system/status` | 系统状态 |
| `GET /api/system/modules` | 模块状态 |
| `GET /api/radar/events` | 雷达事件 |
| `GET /api/bandit/stats` | Bandit 统计 |
| `GET /api/datasource/list` | 数据源列表 |
| `GET /api/strategy/list` | 策略列表 |
| `GET /api/alaya/status` | 阿那亚觉醒状态 |

---

## 使用案例

### 案例 1：开盘前快速扫描 — "今天关注什么？"

**场景**：每天开盘前，快速了解市场热点和系统决策状态。

```bash
#!/bin/bash
# morning_scan.sh — 开盘前扫描

echo "=== 系统健康 ==="
curl -s http://localhost:8080/api/system/status | jq '.data.overall'

echo ""
echo "=== 美股热点题材 ==="
curl -s http://localhost:8080/api/market/hotspot | jq -r '.us.hot_blocks[:5][] | "\(.block_id): \(.weight)"'

echo ""
echo "=== 美股热门股票 ==="
curl -s http://localhost:8080/api/market/hotspot | jq -r '.us.hot_stocks[:10][] | "\(.symbol) \(.change_pct)% weight=\(.weight)"'

echo ""
echo "=== 注意力和谐度 ==="
curl -s http://localhost:8080/api/attention/harmony | jq '.data'

echo ""
echo "=== 注意力上下文 ==="
curl -s http://localhost:8080/api/attention/context | jq '.data | {awakening_level, volatility: .volatility_surface.regime, contradiction: .contradiction.has_contradiction}'
```

**输出示例**：
```
=== 系统健康 ===
"🟢 正常"

=== 美股热点题材 ===
social_media: 0.76
crypto: 0.72
healthcare: 0.61
cloud_ai: 0.61
streaming: 0.56

=== 美股热门股票 ===
SNOW +9.68% weight=1.52
CRWV +8.65% weight=1.43
JPM +0.92% weight=1.37
TSLA +0.52% weight=1.32
MARA +8.96% weight=1.31

=== 注意力和谐度 ===
{
  "harmony_strength": 0.5,
  "harmony_state": "neutral"
}

=== 注意力上下文 ===
{
  "awakening_level": "dormant",
  "volatility": "normal",
  "contradiction": false
}
```

---

### 案例 2：认知 × 市场 联动分析 — "AI 叙事在驱动哪些股票？"

**场景**：结合认知叙事和市场热点，发现叙事驱动的投资机会。

```bash
#!/bin/bash
# narrative_market_analysis.sh — 叙事-市场联动

echo "=== 认知叙事 Top 5 ==="
curl -s http://localhost:8080/api/cognition/topics | python3 -c "
import sys,json
d=json.load(sys.stdin)
topics = d.get('data',{}).get('topics', d.get('data',{}).get('active_topics',[]))
for t in sorted(topics, key=lambda x: x.get('attention_score',0), reverse=True)[:5]:
    print(f'  {t[\"topic\"]}: attention={t[\"attention_score\"]:.3f} count={t.get(\"recent_count\",\"?\")}')
"

echo ""
echo "=== 美股热点题材 ==="
curl -s http://localhost:8080/api/market/hotspot | python3 -c "
import sys,json
d=json.load(sys.stdin)
for b in d['us']['hot_blocks'][:5]:
    print(f'  {b[\"block_id\"]}: weight={b[\"weight\"]}')
"

echo ""
echo "=== 叙事-题材关联矩阵 ==="
curl -s http://localhost:8080/api/attention/narrative-block-matrix | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('success') and d['data']:
    for narrative, blocks in list(d['data'].items())[:5]:
        top = sorted(blocks.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f'  {narrative}: {dict(top)}')
else:
    print('  (需要完整启动模式)')
"
```

---

### 案例 3：持仓监控面板 — "我的持仓怎么样？"

**场景**：实时监控持仓收益、波动率、最大回撤。

```bash
#!/bin/bash
# position_dashboard.sh — 持仓监控

echo "=== 持仓汇总 ==="
curl -s http://localhost:8080/api/attention/portfolio/summary | python3 -c "
import sys,json
d=json.load(sys.stdin)
s = d.get('data',{})
print(f'  持仓数: {len(s.get(\"holdings\",[]))}')
print(f'  自选数: {len(s.get(\"watchlist\",[]))}')
print(f'  题材分布: {s.get(\"block_alloc\",{})}')
print(f'  行业分布: {s.get(\"industry_alloc\",{})}')
"

echo ""
echo "=== 持仓指标 ==="
curl -s http://localhost:8080/api/attention/position/metrics | python3 -c "
import sys,json
d=json.load(sys.stdin)
metrics = d.get('data',[])
if not metrics:
    print('  (暂无持仓)')
else:
    for m in metrics:
        print(f'  {m[\"symbol\"]}: 收益={m.get(\"return_pct\",0):+.2f}% 波动={m.get(\"volatility\",0):.2f} 速度={m.get(\"price_velocity\",0):.4f}')
"

echo ""
echo "=== 跟踪统计 ==="
curl -s http://localhost:8080/api/attention/tracking/stats | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
print(f'  跟踪中: {d[\"tracking_count\"]}  已关闭: {d[\"closed_count\"]}')
print(f'  平均收益: {d[\"avg_return\"]:+.2f}%  胜率: {d[\"win_rate\"]:.0%}')
"

echo ""
echo "=== 流动性 ==="
curl -s http://localhost:8080/api/attention/liquidity | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
print(f'  总资产: \${d[\"total_value\"]:,.0f}  现金: \${d[\"cash\"]:,.0f}  持仓: \${d[\"position_value\"]:,.0f}')
print(f'  今日盈亏: \${d[\"daily_pnl\"]:+,.0f}')
"
```

---

### 案例 4：决策辅助 — "现在能买吗？"

**场景**：结合信念验证、时机信号和和谐度，辅助交易决策。

```bash
#!/bin/bash
# should_i_buy.sh — 决策辅助

echo "=== 信念验证 ==="
curl -s http://localhost:8080/api/attention/conviction | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('success') and d['data']:
    s = d['data']
    print(f'  信念分数: {s.get(\"conviction_score\",\"N/A\")}')
    print(f'  共识题材: {s.get(\"consensus_blocks\",[])}')
    print(f'  分歧题材: {s.get(\"divergence_blocks\",[])}')
    print(f'  盲区: {s.get(\"blind_spots\",[])}')
    print(f'  信号: {s.get(\"conviction_signal\",\"N/A\")}')
else:
    print('  (需要完整启动模式)')
"

echo ""
echo "=== 时机信号 ==="
curl -s http://localhost:8080/api/attention/conviction/timing | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('success') and d['data']:
    signal = d['data']['signal']
    conf = d['data']['confidence']
    emoji = '🟢' if 'good' in signal else ('🟡' if 'hot' in signal else '🔴')
    print(f'  {emoji} 时机: {signal} (置信度: {conf:.0%})')
else:
    print('  (需要完整启动模式)')
"

echo ""
echo "=== 加仓建议 ==="
curl -s http://localhost:8080/api/attention/conviction/should-add | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('success') and d['data']:
    add = d['data']['should_add']
    reason = d['data']['reason']
    emoji = '✅' if add else '⛔'
    print(f'  {emoji} 加仓: {add}')
    print(f'  原因: {reason}')
else:
    print('  (需要完整启动模式)')
"

echo ""
echo "=== 和谐度 ==="
curl -s http://localhost:8080/api/attention/harmony | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
state = d['harmony_state']
strength = d['harmony_strength']
emoji = '🟢' if state == 'harmonious' else ('🟡' if state == 'neutral' else '🔴')
print(f'  {emoji} {state} (强度: {strength:.2f})')
"
```

---

### 案例 5：系统健康巡检 — "一切正常吗？"

**场景**：定期检查系统各模块健康状态。

```bash
#!/bin/bash
# health_check.sh — 系统健康巡检

echo "=== 系统总览 ==="
curl -s http://localhost:8080/api/system/status | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
print(f'  状态: {d[\"overall\"]}')
print(f'  健康: {d[\"healthy\"]}/{d[\"total\"]}')
if d.get('warning_modules'):
    print(f'  ⚠️ 警告: {d[\"warning_modules\"]}')
if d.get('error_modules'):
    print(f'  ❌ 错误: {d[\"error_modules\"]}')
"

echo ""
echo "=== 各模块延迟 ==="
curl -s http://localhost:8080/api/system/status | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
for m in d['modules']:
    status = '✅' if m['status']=='healthy' else '⚠️'
    print(f'  {status} {m[\"name\"]}: {m[\"delay\"]:.1f}s {m.get(\"info\",\"\")}')
"

echo ""
echo "=== 数据源状态 ==="
curl -s http://localhost:8080/api/datasource/list | python3 -c "
import sys,json
d=json.load(sys.stdin)
sources = d.get('data', d.get('datasources', []))
if isinstance(sources, list):
    for s in sources:
        print(f'  {s.get(\"name\",s)}: {s.get(\"status\",s.get(\"state\",\"?\"))}')
elif isinstance(sources, dict):
    for k,v in sources.items():
        print(f'  {k}: {v}')
"

echo ""
echo "=== 注意力上下文 ==="
curl -s http://localhost:8080/api/attention/context | python3 -c "
import sys,json
d=json.load(sys.stdin)['data']
print(f'  觉醒: {d[\"awakening_level\"]}')
print(f'  波动率: {d[\"volatility_surface\"][\"regime\"]} ({d[\"volatility_surface\"][\"volatility\"]})')
print(f'  矛盾: {\"有\" if d[\"contradiction\"][\"has_contradiction\"] else \"无\"}')
"
```

---

### 案例 6：Python 自动化 — 生成每日报告

**场景**：用 Python 调用 API，生成结构化的每日分析报告。

```python
#!/usr/bin/env python3
"""daily_brief.py — 每日简报生成器"""

import requests
import json
from datetime import datetime

BASE = "http://localhost:8080"

def api(path):
    try:
        return requests.get(f"{BASE}{path}", timeout=15).json()
    except:
        return {"success": False}

def main():
    report = []
    report.append(f"# Naja 每日简报 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")

    # 系统状态
    sys = api("/api/system/status")
    report.append(f"## 系统状态: {sys.get('data',{}).get('overall','?')}")

    # 市场热点
    mkt = api("/api/market/hotspot")
    cn = mkt.get("cn", {})
    us = mkt.get("us", {})
    report.append(f"\n## 市场热点")
    report.append(f"- A股聚焦度: {cn.get('market_hotspot', 0)}")
    report.append(f"- 美股聚焦度: {us.get('market_hotspot', 0)}")
    if us.get("hot_blocks"):
        report.append(f"\n### 美股题材 Top 5")
        for b in us["hot_blocks"][:5]:
            report.append(f"- {b['block_id']}: {b['weight']}")
    if us.get("hot_stocks"):
        report.append(f"\n### 美股股票 Top 5")
        for s in us["hot_stocks"][:5]:
            ch = s.get("change_pct", 0)
            report.append(f"- {s['symbol']}: {ch:+.2f}%")

    # 注意力
    ctx = api("/api/attention/context")
    if ctx.get("success"):
        d = ctx["data"]
        report.append(f"\n## 注意力状态")
        report.append(f"- 觉醒级别: {d.get('awakening_level', '?')}")
        report.append(f"- 波动率: {d.get('volatility_surface',{}).get('regime','?')}")
        report.append(f"- 矛盾: {'有' if d.get('contradiction',{}).get('has_contradiction') else '无'}")

    harm = api("/api/attention/harmony")
    if harm.get("success"):
        d = harm["data"]
        report.append(f"- 和谐度: {d.get('harmony_state','?')} ({d.get('harmony_strength',0):.2f})")

    # 流动性
    liq = api("/api/attention/liquidity")
    if liq.get("success"):
        d = liq["data"]
        report.append(f"\n## 流动性")
        report.append(f"- 总资产: ${d.get('total_value',0):,.0f}")
        report.append(f"- 今日盈亏: ${d.get('daily_pnl',0):+,.0f}")

    text = "\n".join(report)
    print(text)

    # 保存
    with open(f"brief_{datetime.now().strftime('%Y%m%d')}.md", "w") as f:
        f.write(text)
    print(f"\n已保存到 brief_{datetime.now().strftime('%Y%m%d')}.md")

if __name__ == "__main__":
    main()
```

---

## Python 客户端

```bash
# 查看所有命令
python scripts/api_client.py --help

# 常用命令
python scripts/api_client.py system-status
python scripts/api_client.py market-hotspot
python scripts/api_client.py manas-state --output text
python scripts/api_client.py harmony
python scripts/api_client.py conviction
python scripts/api_client.py portfolio-summary
python scripts/api_client.py attention-context
python scripts/api_client.py tracking-stats
python scripts/api_client.py liquidity

# 带参数
python scripts/api_client.py cognition-topics --lookback 100
python scripts/api_client.py strategy-top-symbols --n 10
```

## 响应格式

所有端点返回 JSON：

```json
// 成功
{"success": true, "data": {...}}

// 错误
{"success": false, "error": "模块未初始化"}
```

## 系统要求

- Naja 系统运行在端口 8080
- Python 3.8+（客户端）
- requests 库（客户端）

## 许可证

MIT License
