"""Convert markdown analysis reports to styled HTML."""
import re
import sys

CSS = """
:root {
  --bg: #ffffff;
  --text: #1a1a1a;
  --text-secondary: #555555;
  --border: #e5e5e5;
  --accent: #2563eb;
  --green: #16a34a;
  --yellow: #ca8a04;
  --red: #dc2626;
  --surface: #f8f9fa;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: var(--font);
  color: var(--text);
  background: var(--bg);
  line-height: 1.7;
  padding: 2rem;
  max-width: 820px;
  margin: 0 auto;
}
h1 { font-size: 1.8rem; font-weight: 600; margin: 2rem 0 0.5rem; border-bottom: 2px solid var(--border); padding-bottom: 0.4rem; }
h2 { font-size: 1.35rem; font-weight: 600; margin: 2rem 0 0.6rem; color: #111; }
h3 { font-size: 1.1rem; font-weight: 600; margin: 1.2rem 0 0.4rem; }
h4 { font-size: 1rem; font-weight: 600; margin: 1rem 0 0.3rem; }
p { margin: 0.6rem 0; }
ul, ol { margin: 0.4rem 0 0.4rem 1.5rem; }
li { margin: 0.2rem 0; }
blockquote {
  border-left: 3px solid var(--accent);
  padding: 0.5rem 1rem;
  margin: 0.8rem 0;
  background: var(--surface);
  border-radius: 0 4px 4px 0;
  font-style: italic;
  color: var(--text-secondary);
}
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
strong { font-weight: 600; }
code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--surface);
  padding: 0.15em 0.4em;
  border-radius: 3px;
  border: 0.5px solid var(--border);
}
pre { display: none; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
th, td {
  border: 0.5px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}
th { background: var(--surface); font-weight: 600; }
tr:nth-child(even) td { background: #fafbfc; }

.green-badge { color: var(--green); font-weight: 600; }
.yellow-badge { color: var(--yellow); font-weight: 600; }
.red-badge { color: var(--red); font-weight: 600; }

.header-meta {
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}
.header-meta strong { color: var(--text); }

.toc {
  background: var(--surface);
  border: 0.5px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  margin: 1.5rem 0;
}
.toc h3 { margin-top: 0; }
.toc ol { margin-left: 1.2rem; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }

.rating-green { color: var(--green); }
.rating-yellow { color: var(--yellow); }
.rating-red { color: var(--red); }

@media (max-width: 600px) {
  body { padding: 1rem; }
  h1 { font-size: 1.4rem; }
  table { font-size: 0.8rem; }
  th, td { padding: 0.35rem 0.5rem; }
}

@media print {
  body { padding: 0; max-width: 100%; }
  .header-meta { break-inside: avoid; }
}
"""

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    in_table = False
    in_blockquote = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines in some contexts
        if not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_table:
                html_lines.append('</table>')
                in_table = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('')
            i += 1
            continue
        
        # Horizontal rules
        if line.strip() == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_table:
                html_lines.append('</table>')
                in_table = False
            html_lines.append('<hr>')
            i += 1
            continue
        
        # Blockquotes
        if line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            content = line[2:]
            content = process_inline(content)
            html_lines.append(f'<p>{content}</p>')
            i += 1
            continue
        
        if in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False
        
        # Tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                # Check if first line is header
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html_lines.append('<thead><tr>')
                for cell in cells:
                    html_lines.append(f'<th>{process_inline(cell)}</th>')
                html_lines.append('</tr></thead><tbody>')
                # Check if next line is separator
                if i + 1 < len(lines) and '---' in lines[i+1] and '|' in lines[i+1]:
                    i += 2
                    continue
            else:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html_lines.append('<tr>')
                for cell in cells:
                    tag = 'th' if line.strip().startswith('|---') else 'td'
                    html_lines.append(f'<td>{process_inline(cell)}</td>')
                html_lines.append('</tr>')
            i += 1
            continue
        
        if in_table and not ('|' in line and line.strip().startswith('|')):
            html_lines.append('</tbody></table>')
            in_table = False
        
        # Headings
        if line.startswith('# '):
            html_lines.append(f'<h1>{process_inline(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{process_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{process_inline(line[4:])}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{process_inline(line[5:])}</h4>')
        # Unordered lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_lines.append(f'<li>{process_inline(content)}</li>')
        # Ordered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            content = re.sub(r'^\d+\.\s', '', line.strip())
            html_lines.append(f'<li>{process_inline(content)}</li>')
        else:
            html_lines.append(f'<p>{process_inline(line)}</p>')
        
        i += 1
    
    # Close any open structures
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</tbody></table>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)


def process_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    text = text.replace('🟢', '<span class="green-badge">🟢</span>')
    text = text.replace('🟡', '<span class="yellow-badge">🟡</span>')
    text = text.replace('🔴', '<span class="red-badge">🔴</span>')
    
    return text


def generate_toc(md_text):
    """Generate table of contents from headings."""
    headings = re.findall(r'^(#{1,3})\s+(.+)$', md_text, re.MULTILINE)
    toc_lines = ['<div class="toc"><h3>目录</h3><ol>']
    for level, title in headings:
        if level == '#':
            continue  # Skip main title
        indent = '  ' * (len(level) - 2)
        anchor = re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '-')
        toc_lines.append(f'<li style="margin-left:{1.5 * (len(level)-2)}rem"><a href="#{anchor}">{title}</a></li>')
    toc_lines.append('</ol></div>')
    return '\n'.join(toc_lines)


def add_anchors(html):
    """Add id anchors to headings."""
    def replacer(match):
        tag = match.group(1)
        title = match.group(2)
        anchor = re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '-')
        return f'<{tag} id="{anchor}">{title}</{tag}>'
    return re.sub(r'<(h[1-3])>(.+?)</h\1>', replacer, html)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert.py <input.md>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    toc = generate_toc(md_text)
    body_html = md_to_html(md_text)
    body_html = add_anchors(body_html)
    
    # Extract title for HTML title
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Analysis Report'
    
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
{toc}
{body_html}
</body>
</html>"""
    
    out_path = sys.argv[1].replace('.md', '.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated: {out_path}")
