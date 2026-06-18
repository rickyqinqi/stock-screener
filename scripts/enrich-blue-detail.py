#!/usr/bin/env python3
"""为13只蓝标股票生成详细分析卡片数据"""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST = os.path.join(ROOT, "docs", "data", "latest.json")
BLUE_DETAIL = os.path.join(ROOT, "docs", "data", "blue-detail.json")

# 13只蓝标详细分析（综合6位专家+最新基本面数据）
details = {
    "sz002916": {
        "name": "深南电路",
        "summary": "AI算力PCB龙头，净利暴增74%+现金流极佳，是13只中最确定的成长标的",
        "industry": {"stars": 5, "pos": "高端PCB/封装基板，AI服务器核心供应商，国内唯一量产ABF载板", "driver": "AI算力扩产→封装基板需求爆发→量价齐升"},
        "fundamental": {"speed": "加速", "rev_growth": "+32%", "profit_growth": "+74%", "roe": "20.8%", "cash_quality": "经营现金流38亿>净利33亿", "verdict": "营收净利双高增，逐季加速，盈利质量极高"},
        "valuation": {"pe_ttm": 82, "peg": 1.34, "peg_fwd": 0.90, "verdict": "PEG合理偏高但Forward PE 55倍+PEG 0.9，盈利趋势向上可消化"},
        "capital": {"today": "-4.99亿", "signal": "大单流出+机构折价大宗，短线获利了结", "verdict": "机构边打边撤，但换手仅1.88%说明主力未大规模出逃"},
        "shortTerm": {"ma5": 413, "deviation": "+5.9%", "signal": "PCB总龙头昨日涨停后回调洗盘，等重新站稳MA5", "verdict": "短线回调中，MA5≈413是关键支撑"},
        "experts": {"bull": 2, "bear": 4, "note": "财报+短线偏多，估值+信号+逆向偏空——同标的最大分歧"},
    },
    "sz002353": {
        "name": "杰瑞股份",
        "summary": "油服压裂设备龙头，Q4营收创历史新高但增收不增利，需等毛利率回升",
        "industry": {"stars": 4, "pos": "油田压裂/固井设备国内市占率第一，中东非洲快速拓展", "driver": "全球油气资本支出上行周期→设备需求增长"},
        "fundamental": {"speed": "减速", "rev_growth": "+21%", "profit_growth": "+2%", "roe": "12.2%", "cash_quality": "经营现金流54亿>净利28亿(回收历史应收)", "verdict": "营收高增但费用侵蚀严重致净利停滞，增收不增利"},
        "valuation": {"pe_ttm": 61, "peg": 1.50, "peg_fwd": 1.11, "verdict": "PEG偏高但不离谱，需等毛利率回升确认"},
        "capital": {"today": "未单独查询", "signal": "无明确信号", "verdict": "千亿大市值，机构持仓稳定"},
        "shortTerm": {"ma60": 128, "deviation": "+30%", "signal": "MA60偏离30%，距MA120还需跌23%才到逆向买点", "verdict": "趋势仍在但偏离过大，等回调"},
        "experts": {"bull": 2, "bear": 4, "note": "逆向+估值偏空(等跌)，财报偏多(持有不卖)"},
    },
    "sz300054": {
        "name": "鼎龙股份",
        "summary": "CMP抛光垫国内唯一，毛利率51%+净利+38%，但PEG 2.31偏贵+主力持续流出",
        "industry": {"stars": 5, "pos": "CMP抛光垫+PI浆料国内垄断，深度受益存储扩产", "driver": "长鑫IPO催化+存储扩产→CMP耗材需求爆发"},
        "fundamental": {"speed": "加速", "rev_growth": "+10%", "profit_growth": "+38%", "roe": "12.8%", "cash_quality": "毛利率51%，经营现金流11.6亿>净利7.2亿", "verdict": "半导体材料放量+利润率双击，国产替代兑现最漂亮的标的"},
        "valuation": {"pe_ttm": 105, "peg": 2.31, "peg_fwd": 1.80, "verdict": "PEG偏贵，涨幅101%远超增速45%，需等估值消化"},
        "capital": {"today": "-1.05亿", "signal": "持续流出+折价大宗", "verdict": "机构获利了结，等回调后的"黄金坑""},
        "shortTerm": {"ma5": 83, "deviation": "+10%", "signal": "非本周主线核心标的", "verdict": "中线逻辑硬但短线无催化剂"},
        "experts": {"bull": 2, "bear": 4, "note": "产业+财报看好赛道，估值+逆向嫌贵，信号看资金流出"},
    },
    "sz300223": {
        "name": "北京君正",
        "summary": "车载存储芯片龙头，存储涨价周期受益但ROE仅3%+机构20笔折价大宗减持",
        "industry": {"stars": 4, "pos": "全球车规级DRAM隐形冠军，AI存储3D DRAM布局中", "driver": "存储涨价周期+车规芯片国产替代+AI存储远期预期"},
        "fundamental": {"speed": "减速", "rev_growth": "+13%", "profit_growth": "+3%", "roe": "3.1%", "cash_quality": "经营现金流6.2亿>净利3.8亿，但7.1亿研发吃掉毛利", "verdict": "营收恢复增长但净利几乎不增，ROE极低，大量研发投入短期压制利润"},
        "valuation": {"pe_ttm": 144, "peg": 0.71, "peg_fwd": 0.39, "verdict": "PEG便宜(Forward PEG 0.39)，但盈利可持续性是核心风险"},
        "capital": {"today": "+1033万", "signal": "20笔机构折价大宗(5%折价)", "verdict": "机构急售，极度危险信号——即使看好存储逻辑也不能忽视"},
        "shortTerm": {"ma5": 166, "deviation": "+11.4%", "signal": "今日+7.45%，趋势稳健", "verdict": "趋势健康，MA5≈166止损"},
        "experts": {"bull": 3, "bear": 3, "note": "最分裂标的——估值+财报+短线偏多 vs 信号+产业+逆向偏空"},
    },
    "sz002409": {
        "name": "雅克科技",
        "summary": "半导体前驱体平台，营收+25%但PEG 1.89偏贵，增速与估值赛跑中",
        "industry": {"stars": 4, "pos": "前驱体+SOD+电子特气三种半导体材料产品线，国产唯一/唯二", "driver": "AI芯片扩产→前驱体需求增长+国产替代加速"},
        "fundamental": {"speed": "稳定", "rev_growth": "+25%", "profit_growth": "+15%", "roe": "12.6%", "cash_quality": "经营现金流10.3亿≈净利10.3亿，盈利质量好", "verdict": "营收高增但费用增速快于营收，净利增速落后于收入"},
        "valuation": {"pe_ttm": 70, "peg": 1.89, "peg_fwd": 1.39, "verdict": "PEG偏贵，但Forward PEG 1.39尚可接受"},
        "capital": {"today": "未查", "signal": "无明确信号", "verdict": "721亿中大盘，机构持仓相对稳定"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线核心标的", "verdict": "中线好标的但短线无催化剂"},
        "experts": {"bull": 2, "bear": 4, "note": "产业看好但估值+逆向偏空"},
    },
    "sz300373": {
        "name": "扬杰科技",
        "summary": "功率半导体SiC龙头，唯一主力净流入+2亿的标的，PE 48倍PEG 1.60合理偏高",
        "industry": {"stars": 4, "pos": "MOSFET/IGBT/SiC布局完整，新能源车/光储/充电桩三大主力应用", "driver": "碳化硅供需两旺至少看到2027年，AI算力带动功率需求"},
        "fundamental": {"speed": "加速", "rev_growth": "+18%", "profit_growth": "+26%", "roe": "13.7%", "cash_quality": "经营现金流17亿>净利12.5亿，现金牛", "verdict": "净利增速跑赢营收，毛利率34%稳定，现金流扎实"},
        "valuation": {"pe_ttm": 49, "peg": 1.60, "peg_fwd": 1.33, "verdict": "PEG偏高但可接受，SiC放量逻辑确定"},
        "capital": {"today": "+2.01亿", "signal": "唯一逆势大幅流入", "verdict": "资金在用脚投票，功率半导体有独立逻辑"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "今日+7.57%突破，量比1.89", "verdict": "放量突破，短线强势"},
        "experts": {"bull": 4, "bear": 2, "note": "13只中最受认可的标的——产业+信号+财报+短线均偏多"},
    },
    "sz300037": {
        "name": "新宙邦",
        "summary": "电解液二哥+氟化工双轮驱动，PEG 0.45最便宜，Forward PE仅28倍",
        "industry": {"stars": 3, "pos": "锂电电解液+电子信息化学品+有机氟化学品三线并进", "driver": "电解液价格触底反弹+氟化工放量带来第二增长曲线"},
        "fundamental": {"speed": "稳定", "rev_growth": "+23%", "profit_growth": "+16%", "roe": "10.7%", "cash_quality": "经营现金流11.7亿>净利11亿，现金流健康", "verdict": "营收恢复双位数增长但毛利率仅24%偏低，净利距2022年峰值还有差距"},
        "valuation": {"pe_ttm": 46, "peg": 0.45, "peg_fwd": 0.27, "verdict": "PEG最便宜标的，Forward PE仅28倍，估值有明显安全边际"},
        "capital": {"today": "-1.65亿", "signal": "今日流出短期偏弱", "verdict": "季节性波动，整体中性"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线标的", "verdict": "中线估值便宜，短线无催化"},
        "experts": {"bull": 3, "bear": 3, "note": "估值最看好(PEG 0.45)，产业和财报中性"},
    },
    "sz002850": {
        "name": "科达利",
        "summary": "锂电结构件隐形冠军，PE 32倍PEG 0.93最'正常'的估值，营收+26%稳健增长",
        "industry": {"stars": 4, "pos": "全球锂电池结构件龙头市占率超30%，宁德时代核心供应商", "driver": "动力电池高景气+4680大圆柱/刀片电池结构件升级"},
        "fundamental": {"speed": "加速", "rev_growth": "+26%", "profit_growth": "+20%", "roe": "14.1%", "cash_quality": "经营现金流19亿>净利17.5亿，3年净利CAGR 25%", "verdict": "营收净利双高增，现金流强劲，隐形冠军稳健成长"},
        "valuation": {"pe_ttm": 32, "peg": 0.93, "peg_fwd": 0.69, "verdict": "13只中估值最'正常'的标的，PEG接近1，可作为组合压舱石"},
        "capital": {"today": "-2984万", "signal": "今日流出但近20日+6亿", "verdict": "短线偏弱，中期资金仍偏正向"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线标的", "verdict": "慢牛标的，不适合短线博弈"},
        "experts": {"bull": 4, "bear": 2, "note": "估值+财报+产业均认可，PE合理+龙头地位清晰"},
    },
    "sz002138": {
        "name": "顺络电子",
        "summary": "电感龙头，毛利率37%+ROE 16%现金流极好，但PEG 2.25偏贵+涨幅93%已透支",
        "industry": {"stars": 3, "pos": "电感/磁珠国内龙头，受益AI服务器+汽车电子双驱动", "driver": "被动元件供需紧平衡，AI服务器电感用量大幅增加"},
        "fundamental": {"speed": "加速", "rev_growth": "+14%", "profit_growth": "+23%", "roe": "16.1%", "cash_quality": "经营现金流17亿>净利11.4亿，现金流极好", "verdict": "净利增23%跑赢营收14%，毛利率37%优异，盈利质量全面向上"},
        "valuation": {"pe_ttm": 57, "peg": 2.25, "peg_fwd": 1.65, "verdict": "PEG偏贵，93%涨幅对应25%增速，估值已超额反映乐观预期"},
        "capital": {"today": "+6765万", "signal": "今日主力净流入", "verdict": "短线资金偏正向"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "被动元件板块强势但非本周最热", "verdict": "趋势仍在但短线性价比不高"},
        "experts": {"bull": 2, "bear": 4, "note": "基本面优秀但估值太贵，产业+逆向偏空"},
    },
    "sz300346": {
        "name": "南大光电",
        "summary": "光刻胶+前驱体双赛道，毛利率40%+扣非+31%，但主力20日流出28.75亿是最大隐忧",
        "industry": {"stars": 3, "pos": "ArF光刻胶+前驱体国产替代核心标的", "driver": "日本光刻胶酝酿三季度提价+国产Fab扩产→材料需求"},
        "fundamental": {"speed": "稳定", "rev_growth": "+10%", "profit_growth": "+18%", "roe": "9.2%", "cash_quality": "经营现金流7.3亿>净利4亿(扣非+31%)，盈利质量出色", "verdict": "营收个位数但扣非+31%，核心业务在加速，ROE偏低是短板"},
        "valuation": {"pe_ttm": 127, "peg": "-", "peg_fwd": "-", "verdict": "PE 127倍贵，但扣非+31%对应PEG约4，依然偏贵"},
        "capital": {"today": "-3.73亿", "signal": "20日流出-28.75亿，全市场最严重", "verdict": "机构持续大幅减持，是最大风险信号——逻辑再好资金不跟也白搭"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线标的", "verdict": "中线逻辑好但短线资金面极差"},
        "experts": {"bull": 1, "bear": 5, "note": "资金面红旗飘飘，仅产业策略师看好赛道"},
    },
    "sz300811": {
        "name": "铂科新材",
        "summary": "金属磁材受益AI电感需求，毛利率42%但营收增速降至8%+经营现金流低于净利",
        "industry": {"stars": 3, "pos": "金属粉末/电感磁芯，AI服务器芯片电感核心供应商", "driver": "AI算力→芯片电感需求爆发+金属磁材国产替代"},
        "fundamental": {"speed": "稳定", "rev_growth": "+8%", "profit_growth": "+11%", "roe": "15.1%", "cash_quality": "经营现金流3.5亿<净利4.3亿⚠️，营收增速降至个位数", "verdict": "高毛利(42%)+高ROE(15%)，但成长在放缓+现金流质量下降"},
        "valuation": {"pe_ttm": 96, "peg": "-", "peg_fwd": "-", "verdict": "PE 96倍贵，营收增速仅8%难以消化"},
        "capital": {"today": "待查", "signal": "无明确信号", "verdict": "233亿中小盘，筹码相对分散"},
        "shortTerm": {"ma5": 94, "deviation": "+9%", "signal": "今日+5.07%突破后健康", "verdict": "突破后趋势健康，MA5≈94止损"},
        "experts": {"bull": 2, "bear": 4, "note": "短线偏多(趋势好)，产业中性，估值偏空"},
    },
    "sz002831": {
        "name": "裕同科技",
        "summary": "高端包装龙头，PE 25倍+ROE 14%+高分红，防御配置首选但增长天花板已现",
        "industry": {"stars": 3, "pos": "消费电子/白酒/化妆品高端包装，苹果/茅台核心供应商", "driver": "消费电子包装升级+客户结构多元化"},
        "fundamental": {"speed": "减速", "rev_growth": "+0.5%", "profit_growth": "+13%", "roe": "13.6%", "cash_quality": "经营现金流27亿>净利15.8亿，10转4派8元高分红", "verdict": "营收停滞，靠控费挤出13%净利增速，增长天花板明显"},
        "valuation": {"pe_ttm": 25, "peg": "-", "peg_fwd": "-", "verdict": "PE 25倍在蓝标中最低档，ROE 13.6%支撑得住"},
        "capital": {"today": "未查", "signal": "无明确信号", "verdict": "成熟行业龙头，机构稳定持仓"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线标的", "verdict": "不适合短线，适合作为熊市调仓的防御标的"},
        "experts": {"bull": 3, "bear": 3, "note": "财报+估值看好防御价值，产业看天花板"},
    },
    "sz002668": {
        "name": "TCL智家",
        "summary": "冰箱出海龙头，PE仅9.6倍13只中最便宜，但营收停滞+ROE虚高(靠杠杆)",
        "industry": {"stars": 2, "pos": "冰箱/洗衣机出口制造，海外市场占比高", "driver": "家电出海+汇率贬值利好出口"},
        "fundamental": {"speed": "减速", "rev_growth": "+1%", "profit_growth": "+10%", "roe": "37.7%(靠69%负债率)", "cash_quality": "经营现金流25.5亿>净利21.4亿，现金奶牛", "verdict": "营收几乎零增长，ROE虚高靠杠杆(ROA仅14%)，增长动力不足"},
        "valuation": {"pe_ttm": 10, "peg": "-", "peg_fwd": "-", "verdict": "PE 9.6倍蓝标最低，纯防御配置，不适合作为成长标的"},
        "capital": {"today": "未查", "signal": "无明确信号", "verdict": "成熟行业龙头，低波动"},
        "shortTerm": {"ma5": "-", "deviation": "-", "signal": "非本周主线标的", "verdict": "完全不适用于短线"},
        "experts": {"bull": 2, "bear": 4, "note": "仅估值(PE低)和财报(现金牛)偏多，其余偏空"},
    },
}

# 汇总排名：按综合质量分
ranking = []
for code, detail in details.items():
    ind_stars = detail["industry"]["stars"]
    fund_speed = {"加速": 5, "加速(增速待验证)": 4, "稳定": 3, "减速": 1}[detail["fundamental"]["speed"]]
    score = ind_stars * 2 + fund_speed + (6 - detail["experts"]["bear"])
    ranking.append((score, code, detail["name"], detail["experts"]["bull"], detail["experts"]["bear"]))

ranking.sort(key=lambda x: -x[0])

output = {
    "date": "2026-06-18",
    "total": len(details),
    "details": details,
    "ranking": [{"code": r[1], "name": r[2], "score": r[0], "bull": r[3], "bear": r[4]} for r in ranking],
}

with open(BLUE_DETAIL, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"[OK] Generated blue-detail.json with {len(details)} stocks")
for r in ranking:
    print(f"  {r[1]} {r[2]}: score={r[0]} bull={r[3]} bear={r[4]}")
