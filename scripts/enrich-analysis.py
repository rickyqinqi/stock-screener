#!/usr/bin/env python3
"""
为筛选结果增加五维度投研分析标签
基于6位专家报告，为每只股票标注：产业方向 / 估值水位 / 资金信号 / 基本面 / 短线盘面
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST = os.path.join(ROOT, "docs", "data", "latest.json")
OUTPUT = os.path.join(ROOT, "docs", "data", "latest.json")  # 覆盖原文件，增加dimensions字段


# ============================================================
# 维度1：产业方向
# ============================================================
INDUSTRY_MAP = {
    # 高端PCB/封装基板 (第1梯队 ⭐⭐⭐⭐⭐)
    "sz002916": {"label": "高端PCB/封装基板", "tier": 1},
    # PCB下游/模组/检测
    "sz300657": {"label": "PCB-FPC柔性板", "tier": 2},
    "sz002913": {"label": "PCB制造", "tier": 3},
    "sz002815": {"label": "PCB制造", "tier": 3},
    "sz000823": {"label": "PCB制造", "tier": 3},
    "sz300852": {"label": "PCB制造", "tier": 3},
    "sz301132": {"label": "PCB制造", "tier": 3},
    "sz301366": {"label": "PCB设计", "tier": 3},
    "sz300410": {"label": "PCB检测设备", "tier": 3},
    "sz300802": {"label": "PCB-AOI检测", "tier": 3},
    # 半导体材料
    "sz002409": {"label": "半导体前驱体/特气", "tier": 1},
    "sz300054": {"label": "半导体CMP抛光垫", "tier": 1},
    "sz300346": {"label": "半导体光刻胶/前驱体", "tier": 2},
    "sz300576": {"label": "半导体光刻胶", "tier": 2},
    "sz300398": {"label": "半导体电子化学品", "tier": 3},
    "sz300481": {"label": "半导体电子树脂", "tier": 3},
    # 功率半导体
    "sz300373": {"label": "功率半导体SiC", "tier": 2},
    "sz300671": {"label": "模拟芯片设计", "tier": 3},
    # 存储/MCU
    "sz300223": {"label": "车载存储芯片", "tier": 2},
    # 硅材料
    "sz300821": {"label": "有机硅材料", "tier": 3},
    "sz003026": {"label": "半导体硅片", "tier": 3},
    # 被动元件
    "sz002138": {"label": "被动元件电感/磁珠", "tier": 2},
    "sz300811": {"label": "被动元件磁材", "tier": 2},
    "sz301566": {"label": "被动元件MLCC", "tier": 3},
    # 显示/触控/光学
    "sz300566": {"label": "光学膜/显示材料", "tier": 3},
    "sz300088": {"label": "触控显示模组", "tier": 4},
    "sz002106": {"label": "触控显示", "tier": 4},
    # 锂电
    "sz300037": {"label": "锂电电解液", "tier": 3},
    "sz002850": {"label": "锂电结构件龙头", "tier": 3},
    "sz300568": {"label": "锂电隔膜", "tier": 5},
    "sz002192": {"label": "锂矿采选", "tier": 4},
    # 新材料/化工
    "sz002254": {"label": "特种纤维芳纶", "tier": 3},
    "sz002768": {"label": "改性塑料", "tier": 4},
    "sz300586": {"label": "精细化工色母粒", "tier": 4},
    "sz301069": {"label": "特种化工材料", "tier": 4},
    "sz003022": {"label": "光伏EVA材料", "tier": 3},
    "sz300174": {"label": "木质活性炭/硅材料", "tier": 4},
    "sz300196": {"label": "玻纤制品", "tier": 3},
    "sz001359": {"label": "云母绝缘材料", "tier": 4},
    # 工业自动化/设备
    "sz301029": {"label": "FA零部件自动化", "tier": 3},
    "sz300607": {"label": "工业机器人", "tier": 4},
    "sz002851": {"label": "电源/电控/自动化", "tier": 5},
    "sz300820": {"label": "特种电源设备", "tier": 4},
    "sz300488": {"label": "精密工具", "tier": 4},
    "sz301418": {"label": "运动控制器", "tier": 4},
    "sz300720": {"label": "智能计量设备", "tier": 4},
    "sz002931": {"label": "园林机械/零部件", "tier": 5},
    # 半导体设备/零部件
    "sz300260": {"label": "洁净管件/半导体零部件", "tier": 3},
    "sz300480": {"label": "半导体划片机", "tier": 3},
    "sz301611": {"label": "半导体陶瓷零部件", "tier": 3},
    # 电子分销
    "sz300475": {"label": "电子元器件分销", "tier": 4},
    "sz301099": {"label": "电子元器件分销", "tier": 4},
    # 油服
    "sz002353": {"label": "油服压裂设备龙头", "tier": 2},
    # 消费/包装
    "sz002668": {"label": "冰箱出海制造", "tier": 4},
    "sz002831": {"label": "高端包装", "tier": 4},
    "sz002515": {"label": "食品加工", "tier": 5},
    "sz002674": {"label": "皮革加工", "tier": 5},
    # 汽车零部件
    "sz300304": {"label": "汽车电子调节器", "tier": 3},
    "sz002937": {"label": "精密连接器", "tier": 3},
    "sz002993": {"label": "充电器/电源适配器", "tier": 4},
    "sz301252": {"label": "汽车换热器", "tier": 4},
    "sz300733": {"label": "汽车发动机零部件", "tier": 4},
    "sz301161": {"label": "密封件", "tier": 4},
    "sz301303": {"label": "燃气表/计量", "tier": 4},
    # 军工/航空
    "sz003009": {"label": "小型固体火箭", "tier": 4},
    "sz001696": {"label": "摩托车发动机/航空", "tier": 4},
    # 其他
    "sz300031": {"label": "工业互联网/游戏", "tier": 4},
    "sz300292": {"label": "通信射频器件", "tier": 4},
    "sz002213": {"label": "汽车缓速器/存储", "tier": 5},
    "sz300401": {"label": "维生素/原料药", "tier": 4},
    "sz300497": {"label": "原料药/中间体", "tier": 5},
    "sz301178": {"label": "智慧城市/政务IT", "tier": 5},
    "sz301617": {"label": "特种陶瓷材料", "tier": 4},
    "sz301305": {"label": "生物柴油/环保", "tier": 5},
    "sz301580": {"label": "口腔修复材料", "tier": 4},
    "sz300873": {"label": "供应链物流服务", "tier": 4},
    "sz300120": {"label": "电磁线/铜加工", "tier": 4},
    "sz002171": {"label": "铜加工/新材料", "tier": 4},
    "sz002700": {"label": "天然气管道", "tier": 5},
    "sz002263": {"label": "塑料薄膜", "tier": 5},
    "sz002141": {"label": "漆包线/微特电机", "tier": 5},
    "sz000920": {"label": "膜分离/水处理", "tier": 4},
    "sz000722": {"label": "水电/清洁能源", "tier": 4},
    "sz000055": {"label": "幕墙/轨道交通屏蔽门", "tier": 5},
    "sz000691": {"label": "房地产/物业管理", "tier": 5},
    "sz000593": {"label": "城市燃气供应", "tier": 5},
    "sz002972": {"label": "轨道交通信号", "tier": 4},
    "sz300606": {"label": "精密研磨抛光", "tier": 4},
    "sz300700": {"label": "金刚线/光伏辅材", "tier": 4},
    "sz300221": {"label": "改性塑料", "tier": 4},
    "sz300263": {"label": "节能换热/环保", "tier": 5},
    "sz301310": {"label": "光伏线缆", "tier": 4},
    "sz301168": {"label": "光伏接线盒", "tier": 4},
}


# ============================================================
# 维度2：估值水位 (基于估值分析师PEG分析)
# ============================================================
VALUATION_MAP = {
    "sz300475": {"label": "✅ PEG 0.20 极低", "tier": 1},   # 香农芯创
    "sz300037": {"label": "✅ PEG 0.45 便宜", "tier": 1},   # 新宙邦
    "sz300223": {"label": "✅ PEG 0.71 合理", "tier": 2},   # 北京君正
    "sz002850": {"label": "✅ PEG 0.93 合理", "tier": 2},   # 科达利
    "sz002916": {"label": "⚠️ PEG 1.34 偏高", "tier": 3},  # 深南电路
    "sz002851": {"label": "⚠️ Forward PEG特殊", "tier": 4}, # 麦格米特
    "sz002353": {"label": "⚠️ PEG 1.50 偏高", "tier": 3},  # 杰瑞股份
    "sz300373": {"label": "⚠️ PEG 1.60 偏高", "tier": 3},  # 扬杰科技
    "sz002409": {"label": "🔴 PEG 1.89 偏贵", "tier": 4},  # 雅克科技
    "sz002138": {"label": "🔴 PEG 2.25 偏贵", "tier": 4},  # 顺络电子
    "sz300054": {"label": "🔴 PEG 2.31 偏贵", "tier": 4},  # 鼎龙股份
    "sz300260": {"label": "🔴 PEG 5.10 很贵", "tier": 5},  # 新莱应材
}

# For others, derive from PE ranges
def get_valuation_label(code, pe):
    if code in VALUATION_MAP:
        return VALUATION_MAP[code]
    if pe < 0:
        return {"label": "⚠️ 亏损不可估值", "tier": 5}
    if pe < 20:
        return {"label": "✅ PE<20 低估", "tier": 1}
    if pe < 35:
        return {"label": "✅ PE 20-35 合理", "tier": 2}
    if pe < 60:
        return {"label": "⚠️ PE 35-60 偏高", "tier": 3}
    if pe < 150:
        return {"label": "🔴 PE 60-150 贵", "tier": 4}
    return {"label": "🔴 PE>150 极贵", "tier": 5}


# ============================================================
# 维度3：资金信号 (基于信号派首席资金流分析)
# ============================================================
CAPITAL_MAP = {
    "sz300373": {"label": "🟢 主力净流入+2亿", "tier": 1},
    "sz002138": {"label": "🟢 主力净流入+6765万", "tier": 1},
    "sz301099": {"label": "🟡 短线回流转正", "tier": 2},
    "sz002916": {"label": "🔴 主力流出-5亿+大宗", "tier": 5},
    "sz300346": {"label": "🔴 20日流出-28.75亿", "tier": 5},
    "sz300223": {"label": "🔴 20笔折价大宗减持", "tier": 4},
    "sz300054": {"label": "🔴 持续流出+折价大宗", "tier": 4},
    "sz300657": {"label": "🔴 20日流出-20.27亿", "tier": 5},
    "sz300037": {"label": "🟡 今日流出-1.65亿", "tier": 2},
    "sz002850": {"label": "🟡 今日流出-2984万", "tier": 2},
    "sz300568": {"label": "🟡 20日-2.72亿", "tier": 3},
    "sz301029": {"label": "🟡 资金平衡", "tier": 3},
    "sz300401": {"label": "🔴 主力持续流出", "tier": 4},
    "sz300811": {"label": "待查", "tier": 3},
}


# ============================================================
# 维度4：基本面
# ============================================================
FUNDAMENTAL_MAP = {
    # 🟢 业绩驱动
    "sz002916": {"label": "🟢 业绩驱动 净利+74%", "tier": 1},
    "sz002353": {"label": "🟢 业绩驱动 Q4历史新高", "tier": 1},
    "sz002850": {"label": "🟢 业绩驱动 营收+26%", "tier": 1},
    "sz300373": {"label": "🟢 业绩驱动 现金牛", "tier": 1},
    "sz002409": {"label": "🟢 业绩驱动 净利+15%", "tier": 1},
    "sz300037": {"label": "🟢 业绩驱动 重回增长", "tier": 1},
    "sz300054": {"label": "🟢 业绩驱动 现金流极佳", "tier": 1},
    "sz300398": {"label": "🟢 业绩加速 净利+58%", "tier": 1},
    "sz300346": {"label": "🟢 业绩驱动 扣非+31%", "tier": 1},
    "sz002668": {"label": "🟢 稳健现金牛 PE9.6", "tier": 2},
    "sz002831": {"label": "🟢 稳健 ROE13.6%高分红", "tier": 2},
    # 🟡 待验证
    "sz300223": {"label": "🟡 待验证 PE233倍靠AI预期", "tier": 3},
    "sz300475": {"label": "🟡 待验证 净利率仅1.55%", "tier": 3},
    "sz003022": {"label": "🟡 待验证 PE124倍 营收停滞", "tier": 3},
    "sz002192": {"label": "🟡 待验证 锂价弹性标的", "tier": 3},
    # 🔴 恶化
    "sz002851": {"label": "🔴 恶化 Q4亏损现金外流", "tier": 5},
    "sz300568": {"label": "🔴 恶化 净利崩盘90%扣非亏", "tier": 5},
    "sz300260": {"label": "🔴 恶化 净利-23% PE300倍", "tier": 5},
}


# ============================================================
# 维度5：短线盘面
# ============================================================
SHORTTERM_MAP = {
    "sz002916": {"label": "PCB总龙头 回调洗盘 MA5≈413", "tier": 2},
    "sz300223": {"label": "存储龙头 +7.45% 趋势稳健", "tier": 1},
    "sz300373": {"label": "功率突破 +7.57% 量比1.89", "tier": 1},
    "sz300671": {"label": "放量突破 +8.96% 量比2.64", "tier": 1},
    "sz300031": {"label": "放量涨停 +10.72% 量比2.85", "tier": 1},
    "sz300088": {"label": "⚠️ 放量滞涨 量比3.07出货", "tier": 5},
    "sz300811": {"label": "突破后健康 +5.07%", "tier": 2},
    "sz300657": {"label": "高换手滞涨 警惕", "tier": 4},
    "sz301366": {"label": "高换手下跌 警惕", "tier": 4},
}


def main():
    with open(LATEST, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    for market_name, market in data.get("markets", {}).items():
        for stock in market.get("stocks", []):
            code = stock["code"]
            pe = stock.get("pe", 999)

            # 产业方向
            ind = INDUSTRY_MAP.get(code, {"label": "其他/待分类", "tier": 5})

            # 估值水位
            val = get_valuation_label(code, pe)

            # 资金信号
            cap = CAPITAL_MAP.get(code, {"label": "未单独分析", "tier": 3})

            # 基本面
            fund = FUNDAMENTAL_MAP.get(code, {"label": "未深入分析", "tier": 3})

            # 短线盘面
            short = SHORTTERM_MAP.get(code, {"label": "非本周主线标的", "tier": 3})

            stock["dimensions"] = {
                "industry": ind,
                "valuation": val,
                "capital": cap,
                "fundamental": fund,
                "shortTerm": short,
            }

            total += 1

    # 投票 — 圆桌层面，非单只股票层面；这里传整组
    data["roundtableVotes"] = {
        "date": "2026-06-18",
        "summary": "方向对、时机偏晚、资金面背离",
        "votes": {
            "偏空/观望": 4,
            "选择性偏多": 2,
        },
        "experts": [
            {"name": "产业策略师 · 星望远", "stance": "偏空", "reason": "过半仓等回调"},
            {"name": "信号派首席 · 洲四方", "stance": "偏空", "reason": "资金面红灯"},
            {"name": "估值分析师 · 文衡价", "stance": "偏空", "reason": "涨的是PE不是EPS"},
            {"name": "逆向投资人 · 坤候底", "stance": "偏空", "reason": "无一满足买入框架"},
            {"name": "财报研究员 · 钊审财", "stance": "选择性偏多", "reason": "业绩好的可持有"},
            {"name": "短线冲浪手 · 磊追浪", "stance": "选择性偏多", "reason": "主升浪中期鱼尾行情"},
        ],
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Enriched {total} stocks with 5-dimension analysis labels")
    ind_count = len([s for _, m in data['markets'].items() for s in m['stocks'] if s['dimensions']['industry']['tier'] < 5])
    val_count = len([s for _, m in data['markets'].items() for s in m['stocks'] if s['dimensions']['valuation']['tier'] != 3])
    cap_count = len([s for _, m in data['markets'].items() for s in m['stocks'] if s['dimensions']['capital']['label'] != '未单独分析'])
    fund_count = len([s for _, m in data['markets'].items() for s in m['stocks'] if s['dimensions']['fundamental']['label'] != '未深入分析'])
    print(f"   Industry: {ind_count} classified, Valuation: {val_count}, Capital: {cap_count}, Fundamental: {fund_count}")


if __name__ == "__main__":
    main()
