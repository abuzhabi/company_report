#!/usr/bin/env python3
"""Convert NVIDIA V-2.2 Markdown report to styled HTML for GitHub Pages."""

import re
import html as html_mod

md_path = "/Users/abuzhabi/Documents/Obsidian Vault/寻找艾尔法-证券投资系统/公司/英伟达/2026-07-09_英伟达_深度分析报告_V2.2.md"
html_path = "/Users/abuzhabi/WorkBuddy/Claw/outputs/reports/英伟达/2026-07-09_英伟达_深度分析报告_V2.2.html"

with open(md_path, "r", encoding="utf-8") as f:
    md = f.read()

# Remove YAML frontmatter
md = re.sub(r'^---[\s\S]*?---\n', '', md)

def process_markdown(text):
    """Convert key markdown elements to HTML fragments."""
    lines = text.split('\n')
    result = []
    i = 0
    in_table = False
    in_code = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                result.append('<pre><code>')
            else:
                in_code = False
                result.append('</code></pre>')
            i += 1
            continue
        
        if in_code:
            result.append(html_mod.escape(line))
            i += 1
            continue
        
        # Headers
        h1 = re.match(r'^# (.+)$', line)
        h2 = re.match(r'^## (.+)$', line)
        h3 = re.match(r'^### (.+)$', line)
        h4 = re.match(r'^#### (.+)$', line)
        hr = re.match(r'^---$', line)
        blockquote = re.match(r'^> (.+)$', line)
        ul = re.match(r'^- (.+)$', line)
        ol = re.match(r'^\d+\. (.+)$', line)
        checkbox = re.match(r'^- \[(.)\] (.+)$', line)
        
        if h1:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append(f'<h1>{process_inline(h1.group(1))}</h1>')
        elif h2:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append(f'<h2>{process_inline(h2.group(1))}</h2>')
        elif h3:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append(f'<h3>{process_inline(h3.group(1))}</h3>')
        elif h4:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append(f'<h4>{process_inline(h4.group(1))}</h4>')
        elif hr:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append('<hr>')
        elif blockquote:
            result.append(f'<blockquote>{process_inline(blockquote.group(1))}</blockquote>')
        elif checkbox:
            checked = ' checked' if checkbox.group(1) == 'x' else ''
            result.append(f'<div class="checkbox"><input type="checkbox"{checked} disabled> {process_inline(checkbox.group(2))}</div>')
        elif ul:
            result.append(f'<li>{process_inline(ul.group(1))}</li>')
        elif ol:
            result.append(f'<li>{process_inline(ol.group(1))}</li>')
        elif line.strip().startswith('|') and '|' in line:
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(line)
        elif line.strip() == '':
            if in_table:
                # Check if the last row was a separator row
                if len(table_rows) >= 2 and re.match(r'^\|[\s\-:|]+\|$', table_rows[-1]):
                    # Remove separator, it's markdown formatting
                    table_rows.pop()
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            result.append('')
        else:
            if in_table:
                result.append(flush_table(table_rows))
                table_rows = []
                in_table = False
            if line.strip():
                result.append(f'<p>{process_inline(line)}</p>')
            else:
                result.append('')
        
        i += 1
    
    if in_table:
        result.append(flush_table(table_rows))
    
    return '\n'.join(result)

def flush_table(rows):
    if not rows:
        return ''
    html = ['<table>']
    for idx, row in enumerate(rows):
        cells = [c.strip() for c in row.split('|')[1:-1]]
        tag = 'th' if idx == 0 else 'td'
        html.append('<tr>')
        for cell in cells:
            html.append(f'<{tag}>{process_inline(cell)}</{tag}>')
        html.append('</tr>')
    html.append('</table>')
    return '\n'.join(html)

def process_inline(text):
    """Process inline markdown: bold, italic, code, links."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Bold with __
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Arrow → 
    text = text.replace('→', '&rarr;')
    text = text.replace('←', '&larr;')
    text = text.replace('↓', '&darr;')
    text = text.replace('↑', '&uarr;')
    # Emojis and symbols
    text = text.replace('✅', '<span class="check">✅</span>')
    text = text.replace('⚠️', '<span class="warn">⚠️</span>')
    
    return text

body = process_markdown(md)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>英伟达（NVIDIA）深度分析报告 V-2.2 | 2026-07-09</title>
<style>
:root {{
  --bg: #faf9f7;
  --card-bg: #ffffff;
  --text: #1a1a1a;
  --text-secondary: #555;
  --border: #e8e5e0;
  --accent: #76b900;
  --accent-text: #fff;
  --green-bg: #e8f5e9;
  --green-text: #2e7d32;
  --yellow-bg: #fff8e1;
  --yellow-text: #f57f17;
  --red-bg: #ffebee;
  --red-text: #c62828;
  --table-stripe: #faf9f7;
  --header-bg: #f5f3ef;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.75;
  font-size: 15px;
}}
.container {{
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}}
.report-header {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 36px 40px;
  margin-bottom: 32px;
}}
.report-header h1 {{
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1a1a1a;
}}
.report-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 16px;
  font-size: 13px;
  color: var(--text-secondary);
}}
.report-meta span {{
  background: var(--header-bg);
  padding: 4px 12px;
  border-radius: 6px;
}}
h1 {{ font-size: 24px; font-weight: 700; margin: 48px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--accent); }}
h2 {{ font-size: 20px; font-weight: 700; margin: 36px 0 12px; color: #333; }}
h3 {{ font-size: 17px; font-weight: 600; margin: 28px 0 10px; color: #444; }}
h4 {{ font-size: 15px; font-weight: 600; margin: 20px 0 8px; color: #555; }}
p {{ margin: 12px 0; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0 24px;
  font-size: 14px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}}
th, td {{
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}}
th {{
  background: var(--header-bg);
  font-weight: 600;
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
tr:nth-child(even) td {{ background: var(--table-stripe); }}
tr:hover td {{ background: #f0ede7; }}
blockquote {{
  background: #f8f9fa;
  border-left: 4px solid var(--accent);
  padding: 12px 20px;
  margin: 16px 0;
  border-radius: 0 8px 8px 0;
  color: #444;
  font-style: italic;
}}
blockquote p {{ margin: 4px 0; }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 32px 0; }}
code {{
  background: #f0ede7;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: "SF Mono", "Fira Code", monospace;
}}
pre {{
  background: #1a1a1a;
  color: #e0e0e0;
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
  font-size: 13px;
}}
pre code {{ background: none; padding: 0; }}
li {{ margin: 6px 0 6px 24px; }}
.checkbox {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0 4px 24px;
  font-size: 14px;
}}
.checkbox input[type="checkbox"] {{ margin-right: 4px; }}
strong {{ color: #1a1a1a; }}
em {{ color: #666; }}
.green {{ color: #2e7d32; background: #e8f5e9; padding: 2px 6px; border-radius: 4px; }}
.yellow {{ color: #f57f17; background: #fff8e1; padding: 2px 6px; border-radius: 4px; }}
.red {{ color: #c62828; background: #ffebee; padding: 2px 6px; border-radius: 4px; }}
.footnote {{
  font-size: 12px;
  color: #999;
  margin-top: 60px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}}
@media (max-width: 640px) {{
  .container {{ padding: 16px 12px 60px; }}
  .report-header {{ padding: 24px 20px; }}
  table {{ font-size: 12px; }}
  th, td {{ padding: 6px 8px; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="report-header">
  <h1>🔬 英伟达（NVIDIA）深度分析报告</h1>
  <p style="color: #555; font-size: 16px;">框架版本 V-2.2 | 完整版（第0-10章 + 投资决策价格体系 + Value Drivers）</p>
  <div class="report-meta">
    <span>📅 分析日期：2026-07-09</span>
    <span>📊 数据截止：2026-07-08（股价）/ 2026-04-26（FY2027 Q1）</span>
    <span>🏷️ NVDA · NASDAQ</span>
    <span>💰 市值：$4.94T</span>
    <span>⭐ Fisher：91/100</span>
    <span>🎯 投资建议：观察</span>
  </div>
</div>

{body}

<div class="footnote">
  <p>报告生成于 2026-07-09 | 框架版本：Research Constitution V-2.2 | 分析工具：WorkBuddy + WebSearch</p>
  <p>下一重要更新节点：FY2027 Q2 财报（预计 2026-08-26）</p>
  <p style="margin-top: 12px; color: #aaa;">免责声明：本报告仅用于个人投资研究参考，不构成任何投资建议。投资有风险，入市须谨慎。</p>
</div>

</div>
</body>
</html>'''

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML written to: {html_path}")
print(f"Size: {len(html)} bytes")
