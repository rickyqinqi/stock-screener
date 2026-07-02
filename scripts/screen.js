/**
 * 深证A股均线多头排列筛选脚本
 * 
 * 筛选条件：
 * 1. 均线多头排列（MA多头发散策略）
 * 2. 归属于母公司所有者的净利润 > 0
 * 3. 最近3个月涨跌幅 0% ~ 100%
 * 4. 市场类型：深证A股
 * 
 * 用法：node scripts/screen.js [--date YYYY-MM-DD]
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TOOLS = path.join(ROOT, 'tools');
const DATA_DIR = path.join(ROOT, 'docs', 'data');
const HISTORY_DIR = path.join(DATA_DIR, 'history');

// 工具路径
const WESTOOL_TOOL = path.join(TOOLS, 'westock-tool.js');
const WESTOOL_DATA = path.join(TOOLS, 'westock-data.js');

// 市场分类规则
function classifyMarket(code) {
  const num = parseInt(code.substring(2));
  if (code.startsWith('sz')) {
    if (num >= 300000 && num < 302000) return { type: '创业板', subType: 'sz_cyb' };
    if (num >= 0 && num < 10000) return { type: '深圳主板', subType: 'sz_main' };
    return { type: '深圳其他', subType: 'sz_other' };
  }
  if (code.startsWith('sh')) {
    if (num >= 688000) return { type: '科创板', subType: 'sh_kcb' };
    if (num >= 600000) return { type: '上海主板', subType: 'sh_main' };
    return { type: '上海其他', subType: 'sh_other' };
  }
  return { type: '其他', subType: 'other' };
}

// 解析markdown表格
function parseMarkdownTable(text) {
  const lines = text.split('\n');
  const result = [];
  let inTable = false;
  let headers = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (trimmed.includes('---')) continue;
      if (!inTable) {
        headers = trimmed.split('|').map(h => h.trim()).filter(Boolean);
        inTable = true;
        continue;
      }
      const values = trimmed.split('|').map(v => v.trim()).filter(Boolean);
      const row = {};
      headers.forEach((h, i) => {
        if (values[i] !== undefined) row[h] = values[i];
      });
      result.push(row);
    } else if (inTable && !trimmed.startsWith('|')) {
      inTable = false;
    }
  }
  return result;
}

// 运行命令并返回标准输出
function runCommand(cmd, options = {}) {
  try {
    const result = execSync(cmd, {
      encoding: 'utf-8',
      timeout: options.timeout || 120000,
      maxBuffer: options.maxBuffer || 50 * 1024 * 1024,
      ...options
    });
    return { success: true, output: result, error: null };
  } catch (err) {
    return { success: false, output: err.stdout || '', error: err.message };
  }
}

// 获取均线多头排列股票（第1步）
function getMaLongStocks(date) {
  console.log(`[1/4] 获取均线多头排列股票 (${date})...`);
  const cmd = `node "${WESTOOL_TOOL}" strategy ma_long --date ${date} --limit 1000`;
  const result = runCommand(cmd);

  if (!result.success) {
    console.error('  策略查询失败:', result.error);
    return [];
  }

  const stocks = parseMarkdownTable(result.output);
  // 只保留深证A股（sz开头）
  const szStocks = stocks.filter(s => s.code && s.code.startsWith('sz'));
  console.log(`  找到 ${stocks.length} 只均线多头股票，其中 ${szStocks.length} 只深证A股`);
  return szStocks;
}

// 获取符合财务条件的股票（第2步）
function getFinancialFilterStocks() {
  console.log('[2/4] 筛选财务条件（归母净利润>0, 3月涨幅0%~100%）...');
  const cmd = `node "${WESTOOL_TOOL}" filter "intersect([NPParentCompanyOwners > 0, Chg60D > 0, Chg60D < 100])" --limit 5000`;
  const result = runCommand(cmd, { timeout: 180000 });

  if (!result.success) {
    console.error('  财务筛选失败:', result.error);
    return [];
  }

  const stocks = parseMarkdownTable(result.output);
  // 只保留深证A股
  const szStocks = stocks.filter(s => s.code && s.code.startsWith('sz'));
  console.log(`  找到 ${stocks.length} 只符合财务条件的股票，其中 ${szStocks.length} 只深证A股`);
  return szStocks;
}

// 获取交集（第3步）
function getIntersection(maStocks, finStocks) {
  const finCodes = new Set(finStocks.map(s => s.code));
  return maStocks.filter(s => finCodes.has(s.code));
}

// 批量获取股票详细数据（第4步）
async function getStockDetails(codes) {
  console.log(`[3/4] 获取 ${codes.length} 只股票详细数据...`);

  const BATCH_SIZE = 30;
  const allResults = [];

  for (let i = 0; i < codes.length; i += BATCH_SIZE) {
    const batch = codes.slice(i, i + BATCH_SIZE);
    const codeStr = batch.join(',');
    const cmd = `node "${WESTOOL_DATA}" quote ${codeStr}`;
    const result = runCommand(cmd, { timeout: 60000 });

    if (result.success) {
      const details = parseMarkdownTable(result.output);
      allResults.push(...details);
    } else {
      console.error(`  批量查询失败 (${i}-${i + BATCH_SIZE}):`, result.error);
    }

    if (i + BATCH_SIZE < codes.length) {
      console.log(`  进度: ${Math.min(i + BATCH_SIZE, codes.length)}/${codes.length}`);
    }
  }

  console.log(`  成功获取 ${allResults.length} 只股票详情`);
  return allResults;
}

// 主函数
async function main() {
  // 解析参数
  const args = process.argv.slice(2);
  let targetDate = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && args[i + 1]) {
      targetDate = args[i + 1];
      i++;
    }
  }

  // 默认使用昨天日期
  if (!targetDate) {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    targetDate = yesterday.toISOString().split('T')[0];
  }

  console.log(`\n========================================`);
  console.log(`  深证A股均线多头排列筛选`);
  console.log(`  目标日期: ${targetDate}`);
  console.log(`  运行时间: ${new Date().toISOString()}`);
  console.log(`========================================\n`);

  // 第1步：获取均线多头排列股票
  const maStocks = getMaLongStocks(targetDate);
  if (maStocks.length === 0) {
    console.error('未找到任何均线多头排列的深证A股，退出。');
    process.exit(1);
  }

  // 第2步：获取符合财务条件的股票
  const finStocks = getFinancialFilterStocks();
  if (finStocks.length === 0) {
    console.error('未找到任何符合财务条件的深证A股，退出。');
    process.exit(1);
  }

  // 第3步：取交集
  const candidates = getIntersection(maStocks, finStocks);
  console.log(`\n[交集结果] 同时满足均线多头+财务条件: ${candidates.length} 只`);

  if (candidates.length === 0) {
    console.log('没有股票同时满足所有条件。');
    const emptyResult = {
      date: targetDate,
      generatedAt: new Date().toISOString(),
      totalCount: 0,
      markets: {},
      stocks: []
    };
    saveResults(emptyResult, targetDate);
    return;
  }

  // 第4步：获取详细数据
  const codes = candidates.map(s => s.code);
  const details = await getStockDetails(codes);

  // 数据合并与分组
  console.log('[4/4] 数据分组与保存...');
  const nameMap = {};
  candidates.forEach(s => { nameMap[s.code] = s.name; });

  const enriched = details.map(d => {
    const code = d.code || d.symbol || '';
    const marketInfo = classifyMarket(code);

    return {
      code: code,
      name: nameMap[code] || d.name || '',
      market: marketInfo.type,
      marketSubType: marketInfo.subType,
      price: parseFloat(d.price) || 0,
      changePct: parseFloat(d.change_percent) || 0,
      chg60d: parseFloat(d.chg_60d) || 0,
      pe: parseFloat(d.pe_ratio) || 0,
      pb: parseFloat(d.pb_ratio) || 0,
      totalMv: parseFloat(d.total_market_cap) || 0,
      turnoverRate: parseFloat(d.turnover_rate) || 0,
      volumeRatio: parseFloat(d.volume_ratio) || 0,
      high52w: parseFloat(d.high_52week) || 0,
      low52w: parseFloat(d.low_52week) || 0,
    };
  });

  // 按市场分组
  const markets = {};
  enriched.forEach(s => {
    const key = s.market;
    if (!markets[key]) {
      markets[key] = { type: s.marketSubType, stocks: [] };
    }
    markets[key].stocks.push(s);
  });

  // 每个市场内按Chg60D降序排序
  Object.values(markets).forEach(m => {
    m.stocks.sort((a, b) => b.chg60d - a.chg60d);
    m.count = m.stocks.length;
  });

  const result = {
    date: targetDate,
    generatedAt: new Date().toISOString(),
    totalCount: enriched.length,
    markets: markets,
    stocks: enriched
  };

  saveResults(result, targetDate);

  // 自动运行五维度标签增强
  const enrichScript = path.join(ROOT, 'scripts', 'enrich-analysis.py');
  if (fs.existsSync(enrichScript)) {
    console.log('\n[5/5] 运行五维度投研标签增强...');
    try {
      execSync(`python3 "${enrichScript}"`, { stdio: 'inherit', cwd: ROOT });
      console.log('  五维度标签已添加');
    } catch (e) {
      console.log('  五维度标签增强跳过（Python未安装或脚本错误）');
    }
  }

  // 打印摘要
  console.log('\n========================================');
  console.log('  筛选结果摘要');
  console.log('========================================');
  console.log(`  日期: ${targetDate}`);
  console.log(`  总计: ${result.totalCount} 只`);
  Object.entries(markets).forEach(([name, m]) => {
    console.log(`  ${name}: ${m.count} 只`);
  });
  console.log('========================================\n');
}

function saveResults(result, date) {
  // 确保目录存在
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(HISTORY_DIR)) fs.mkdirSync(HISTORY_DIR, { recursive: true });

  // 保存 latest.json
  const latestPath = path.join(DATA_DIR, 'latest.json');
  fs.writeFileSync(latestPath, JSON.stringify(result, null, 2), 'utf-8');
  console.log(`  已保存: ${latestPath}`);

  // 保存历史记录
  const historyPath = path.join(HISTORY_DIR, `${date}.json`);
  fs.writeFileSync(historyPath, JSON.stringify(result, null, 2), 'utf-8');
  console.log(`  已保存: ${historyPath}`);

  // 更新历史索引
  updateHistoryIndex();
}

function updateHistoryIndex() {
  const indexPath = path.join(DATA_DIR, 'history-index.json');
  let index = [];

  if (fs.existsSync(indexPath)) {
    try {
      index = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
    } catch (e) {
      index = [];
    }
  }

  // 扫描历史目录获取所有日期
  const files = fs.readdirSync(HISTORY_DIR)
    .filter(f => f.endsWith('.json') && f !== 'history-index.json')
    .map(f => {
      const date = f.replace('.json', '');
      const filePath = path.join(HISTORY_DIR, f);
      try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        return { date, totalCount: data.totalCount || 0, markets: Object.keys(data.markets || {}) };
      } catch (e) {
        return { date, totalCount: 0, markets: [] };
      }
    })
    .sort((a, b) => b.date.localeCompare(a.date));

  fs.writeFileSync(indexPath, JSON.stringify(files, null, 2), 'utf-8');
  console.log(`  历史索引已更新: ${files.length} 条记录`);
}

main().catch(err => {
  console.error('执行失败:', err);
  process.exit(1);
});
