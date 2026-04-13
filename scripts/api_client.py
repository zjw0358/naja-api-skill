#!/usr/bin/env python3
"""
Naja API 客户端脚本

用于调用 naja 系统的各种 API 端点，方便用户获取系统数据和状态。
支持 34 个 API 端点。
"""

import requests
import json
import argparse
import time

BASE_URL = "http://localhost:8080"


def call_api(endpoint, params=None):
    """调用 API 端点"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 认知系统
# ============================================================

def get_cognition_memory():
    return call_api("/api/cognition/memory")

def get_cognition_topics(lookback=50):
    return call_api("/api/cognition/topics", params={"lookback": lookback})

def get_cognition_attention(lookback=200):
    return call_api("/api/cognition/attention", params={"lookback": lookback})

def get_cognition_thought():
    return call_api("/api/cognition/thought")

# ============================================================
# 市场热点
# ============================================================

def get_market_state():
    return call_api("/api/market/state")

def get_market_hotspot():
    return call_api("/api/market/hotspot")

def get_market_hotspot_details():
    return call_api("/api/market/hotspot/details")

# ============================================================
# Attention - P0 核心决策
# ============================================================

def get_manas_state():
    return call_api("/api/attention/manas/state")

def get_harmony():
    return call_api("/api/attention/harmony")

def get_decision():
    return call_api("/api/attention/decision")

def get_conviction():
    return call_api("/api/attention/conviction")

def get_conviction_timing():
    return call_api("/api/attention/conviction/timing")

def get_conviction_should_add():
    return call_api("/api/attention/conviction/should-add")

# ============================================================
# Attention - P1 持仓与跟踪
# ============================================================

def get_portfolio_summary():
    return call_api("/api/attention/portfolio/summary")

def get_position_metrics():
    return call_api("/api/attention/position/metrics")

def get_tracking_hotspot():
    return call_api("/api/attention/tracking/hotspot")

def get_tracking_stats():
    return call_api("/api/attention/tracking/stats")

# ============================================================
# Attention - P2 发现与融合
# ============================================================

def get_blind_spots():
    return call_api("/api/attention/blind-spots")

def get_fusion():
    return call_api("/api/attention/fusion")

def get_focus():
    return call_api("/api/attention/focus")

def get_narrative_block_matrix():
    return call_api("/api/attention/narrative-block-matrix")

# ============================================================
# Attention - P3 状态与报告
# ============================================================

def get_attention_report():
    return call_api("/api/attention/report")

def get_lab_status():
    return call_api("/api/attention/lab/status")

def get_liquidity():
    return call_api("/api/attention/liquidity")

def get_strategy_top_symbols(n=20):
    return call_api("/api/attention/strategy/top-symbols", params={"n": n})

def get_strategy_top_blocks(n=10):
    return call_api("/api/attention/strategy/top-blocks", params={"n": n})

def get_attention_context():
    return call_api("/api/attention/context")

# ============================================================
# 系统监控
# ============================================================

def get_system_status():
    return call_api("/api/system/status")

def get_system_modules():
    return call_api("/api/system/modules")

# ============================================================
# 其他
# ============================================================

def get_radar_events():
    return call_api("/api/radar/events")

def get_bandit_stats():
    return call_api("/api/bandit/stats")

def get_datasource_list():
    return call_api("/api/datasource/list")

def get_strategy_list():
    return call_api("/api/strategy/list")

def get_alaya_status():
    return call_api("/api/alaya/status")


# ============================================================
# 命令映射
# ============================================================

COMMANDS = {
    # 认知系统
    "cognition-memory": get_cognition_memory,
    "cognition-topics": lambda: get_cognition_topics(args.lookback or 50),
    "cognition-attention": lambda: get_cognition_attention(args.lookback or 200),
    "cognition-thought": get_cognition_thought,
    # 市场
    "market-state": get_market_state,
    "market-hotspot": get_market_hotspot,
    "market-hotspot-details": get_market_hotspot_details,
    # Attention P0
    "manas-state": get_manas_state,
    "harmony": get_harmony,
    "decision": get_decision,
    "conviction": get_conviction,
    "conviction-timing": get_conviction_timing,
    "conviction-should-add": get_conviction_should_add,
    # Attention P1
    "portfolio-summary": get_portfolio_summary,
    "position-metrics": get_position_metrics,
    "tracking-hotspot": get_tracking_hotspot,
    "tracking-stats": get_tracking_stats,
    # Attention P2
    "blind-spots": get_blind_spots,
    "fusion": get_fusion,
    "focus": get_focus,
    "narrative-block-matrix": get_narrative_block_matrix,
    # Attention P3
    "attention-report": get_attention_report,
    "lab-status": get_lab_status,
    "liquidity": get_liquidity,
    "strategy-top-symbols": lambda: get_strategy_top_symbols(args.n or 20),
    "strategy-top-blocks": lambda: get_strategy_top_blocks(args.n or 10),
    "attention-context": get_attention_context,
    # 系统
    "system-status": get_system_status,
    "system-modules": get_system_modules,
    # 其他
    "radar-events": get_radar_events,
    "bandit-stats": get_bandit_stats,
    "datasource-list": get_datasource_list,
    "strategy-list": get_strategy_list,
    "alaya-status": get_alaya_status,
}


def main():
    """主函数"""
    global BASE_URL, args

    parser = argparse.ArgumentParser(
        description="Naja API 客户端（34 个端点）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python api_client.py system-status
  python api_client.py market-hotspot
  python api_client.py manas-state
  python api_client.py conviction --output text
  python api_client.py strategy-top-symbols --n 10
        """
    )
    parser.add_argument("command", choices=list(COMMANDS.keys()), help="API 命令")
    parser.add_argument("--lookback", type=int, help="回溯数量（cognition-topics/attention）")
    parser.add_argument("--n", type=int, help="数量限制（strategy-top-symbols/blocks）")
    parser.add_argument("--base-url", default=BASE_URL, help="API 基础 URL")
    parser.add_argument("--output", choices=["json", "text"], default="json", help="输出格式")

    args = parser.parse_args()
    BASE_URL = args.base_url

    result = COMMANDS[args.command]()

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("success"):
            print(f"✓ 调用成功: {args.command}")
            data = result.get("data", result)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        val_str = json.dumps(value, ensure_ascii=False)
                        if len(val_str) > 150:
                            val_str = val_str[:150] + "..."
                        print(f"  {key}: {val_str}")
                    else:
                        print(f"  {key}: {value}")
            elif isinstance(data, list):
                print(f"  共 {len(data)} 条记录")
                for item in data[:10]:
                    print(f"  - {json.dumps(item, ensure_ascii=False)[:120]}")
            else:
                print(f"  {data}")
        else:
            print(f"✗ 调用失败: {result.get('error')}")


if __name__ == "__main__":
    main()
