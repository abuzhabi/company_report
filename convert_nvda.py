import re
import html as html_escape

with open("/Users/abuzhabi/Documents/Obsidian Vault/寻找艾尔法-证券投资系统/公司/英伟达/2026-07-09_英伟达_深度分析报告.md", "r", encoding="utf-8") as f:
    content = f.read()

# Remove YAML frontmatter
content = re.sub(r'^---\n.*?\n---\n\n', '', content, flags=re.DOTALL)

css = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>英伟达（NVDA）— 大灰皮证券研究深度分析报告</title>
<style>
:root {
  --bg: #f8f9fa;
  --text: #1a1a2e;
  --text-secondary: #555;
  --accent: #e74c3c;
  --accent-green: #27ae60;
  --border: #e0e0e0;
  --card-bg: #ffffff;
  --code-bg: #f5f5f5;
  --table-stripe: #fafafa;
  --warning: #fef3c7;
  --danger: #fee2e2;
  --success: #d1fae5;
  --rating-green: #27ae60;
  --rating-red: #e74c3c;
  --rating-yellow: #f39c12;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "PingFang SC", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.85;
  padding: 40px 20px;
}
.container { max-width: 900px; margin: 0 auto; }
.back-link {
  display: inline-block;
  margin-bottom: 24px;
  color: var(--accent);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
}
.back-link:hover { text-decoration: underline; }
h1 {
  font-size: 1.85rem;
  font-weight: 800;
  margin: 16px 0 8px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--accent);
  line-height: 1.3;
}
h2 {
  font-size: 1.35rem;
  font-weight: 700;
  margin: 36px 0 16px;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 24px 0 12px;
  color: #2c3e50;
}
h4 {
  font-size: 1rem;
  font-weight: 700;
  margin: 16px 0 8px;
  color: #444;
}
blockquote {
  background: #f0f7ff;
  border-left: 4px solid #3b82f6;
  margin: 12px 0;
  padding: 12px 18px;
  border-radius: 0 8px 8px 0;
  color: #1e40af;
  font-size: 0.94rem;
}
p { margin: 8px 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 0.88rem;
  overflow-x: auto;
}
th {
  background: #2c3e50;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
}
td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}
tr:nth-child(even) td { background: var(--table-stripe); }
tr:hover td { background: #eef1ff; }
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 28px 0;
}
strong { color: #1a1a2e; }
ol, ul { padding-left: 24px; margin: 8px 0; }
li { margin: 4px 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.meta {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 24px;
}
.meta span { margin-right: 16px; }
.rating-green { color: #27ae60; font-weight: 700; }
.rating-yellow { color: #f39c12; font-weight: 700; }
.rating-red { color: #e74c3c; font-weight: 700; }
.verdict-box {
  background: #f8f9fa;
  border: 2px solid #2c3e50;
  border-radius: 12px;
  padding: 24px;
  margin: 28px 0;
}
.verdict-box h3 { margin-top: 0; }
.score-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px 24px;
  margin: 12px 0;
}
.score-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dotted var(--border);
}
.checklist { list-style: none; padding-left: 0; }
.checklist li { padding: 4px 0; }
.green-dot { color: #27ae60; }
.red-dot { color: #e74c3c; }
.yellow-dot { color: #f39c12; }
.stars { color: #f39c12; letter-spacing: 2px; }
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-right: 6px;
}
.tag-bull { background: #d1fae5; color: #065f46; }
.tag-base { background: #e0e7ff; color: #3730a3; }
.tag-bear { background: #fee2e2; color: #991b1b; }
@media (max-width: 768px) {
  body { padding: 20px 12px; }
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.2rem; }
  table { font-size: 0.78rem; }
  .score-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div class="container">
<p class="back-link"><a href="index.html">&larr; 返回报告列表</a></p>
'''

# Convert markdown to HTML inline
lines = content.split('\n')
html_parts = []
i = 0
in_table = False
in_code = False
in_list = False
in_ol = False

while i < len(lines):
    line = lines[i]

    # Skip empty lines
    if not line.strip():
        if in_table:
            html_parts.append('</tbody></table>\n')
            in_table = False
        if in_list:
            html_parts.append('</ul>\n')
            in_list = False
        if in_ol:
            html_parts.append('</ol>\n')
            in_ol = False
        i += 1
        continue

    # H1 heading
    if line.startswith('# ') and not line.startswith('## '):
        text = line[2:].strip()
        html_parts.append(f'<h1>{text}</h1>\n')
        i += 1
        continue

    # H2 heading
    if line.startswith('## '):
        text = line[3:].strip()
        # Handle ### for h3, ### for h4
        html_parts.append(f'<h2>{text}</h2>\n')
        i += 1
        continue

    # H3 heading
    if line.startswith('### '):
        text = line[4:].strip()
        html_parts.append(f'<h3>{text}</h3>\n')
        i += 1
        continue

    # H4 heading
    if line.startswith('#### '):
        text = line[5:].strip()
        html_parts.append(f'<h4>{text}</h4>\n')
        i += 1
        continue

    # Horizontal rule
    if line.strip() == '---':
        if in_table:
            html_parts.append('</tbody></table>\n')
            in_table = False
        if in_list:
            html_parts.append('</ul>\n')
            in_list = False
        html_parts.append('<hr>\n')
        i += 1
        continue

    # Blockquote
    if line.startswith('> '):
        if in_table:
            html_parts.append('</tbody></table>\n')
            in_table = False
        block_lines = []
        while i < len(lines) and lines[i].startswith('> '):
            block_lines.append(lines[i][2:])
            i += 1
        html_parts.append('<blockquote>' + '<br>'.join(block_lines) + '</blockquote>\n')
        continue

    # Table
    if '|' in line and line.strip().startswith('|'):
        if in_table:
            # Check if it's a separator row
            if re.match(r'^\|[\s\-:|]+\|$', line):
                html_parts.append('</thead><tbody>\n')
                i += 1
                continue
            # Data row
            cells = [c.strip() for c in line.split('|')[1:-1]]
            html_parts.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n')
        else:
            # Check if next line is a separator (header detection)
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1]):
                if in_list:
                    html_parts.append('</ul>\n')
                    in_list = False
                in_table = True
                header_cells = [c.strip() for c in line.split('|')[1:-1]]
                html_parts.append('<table><thead><tr>' + ''.join(f'<th>{c}</th>' for c in header_cells) + '</tr></thead>\n')
        i += 1
        continue

    # Not in table - close it if was open
    if in_table:
        html_parts.append('</tbody></table>\n')
        in_table = False

    # Unordered list
    if line.strip().startswith('- ') or line.strip().startswith('* '):
        if not in_list:
            if in_ol:
                html_parts.append('</ol>\n')
                in_ol = False
            html_parts.append('<ul>\n')
            in_list = True
        text = line.strip()[2:]
        # Handle bold in list items
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        html_parts.append(f'<li>{text}</li>\n')
        i += 1
        continue

    # Ordered list
    if re.match(r'^\d+\.\s', line.strip()):
        if not in_ol:
            if in_list:
                html_parts.append('</ul>\n')
                in_list = False
            html_parts.append('<ol>\n')
            in_ol = True
        text = re.sub(r'^\d+\.\s', '', line.strip())
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        html_parts.append(f'<li>{text}</li>\n')
        i += 1
        continue

    # Checkbox-style list
    if line.strip().startswith('□') or line.strip().startswith('✅') or line.strip().startswith('⚠️'):
        if not in_list:
            html_parts.append('<ul class="checklist">\n')
            in_list = True
        text = line.strip()
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        html_parts.append(f'<li>{text}</li>\n')
        i += 1
        continue

    # Close open lists
    if in_list:
        html_parts.append('</ul>\n')
        in_list = False
    if in_ol:
        html_parts.append('</ol>\n')
        in_ol = False

    # Regular paragraph
    text = line.strip()
    # Convert bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Convert stars
    text = re.sub(r'★★★★★', r'<span class="stars">★★★★★</span>', text)
    text = re.sub(r'★★★★☆', r'<span class="stars">★★★★☆</span>', text)
    text = re.sub(r'★★★☆☆', r'<span class="stars">★★★☆☆</span>', text)
    text = re.sub(r'★★☆☆☆', r'<span class="stars">★★☆☆☆</span>', text)
    text = re.sub(r'★☆☆☆☆', r'<span class="stars">★☆☆☆☆</span>', text)
    # Convert emoji indicators
    text = text.replace('🟢', '<span class="green-dot">●</span>')
    text = text.replace('🟡', '<span class="yellow-dot">●</span>')
    text = text.replace('🔴', '<span class="red-dot">●</span>')
    html_parts.append(f'<p>{text}</p>\n')
    i += 1

# Close any remaining open tags
if in_table:
    html_parts.append('</tbody></table>\n')
if in_list:
    html_parts.append('</ul>\n')
if in_ol:
    html_parts.append('</ol>\n')

footer = '''
</div>
</body>
</html>
'''

full_html = css + '\n'.join(html_parts) + footer

# Write to file
output_path = "/Users/abuzhabi/WorkBuddy/Claw/outputs/reports/英伟达/2026-07-09_英伟达_深度分析报告.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML report written to: {output_path}")
print(f"Length: {len(full_html)} chars")
