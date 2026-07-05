#!/usr/bin/env python3
"""将新版报告统一为 Rocket Lab 旧版大灰皮风格"""

import re
import os

# Rocket Lab 模板的 CSS 和框架
TEMPLATE_CSS = """:root {
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

code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.88em;
  font-family: "SF Mono", "Fira Code", monospace;
}

pre {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 16px 20px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
  font-size: 0.85rem;
  line-height: 1.5;
}
pre code {
  background: none;
  padding: 0;
  color: inherit;
}

strong { color: #1a1a2e; }

ol, ul { padding-left: 24px; margin: 8px 0; }
li { margin: 4px 0; }

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

footer {
  text-align: center;
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 0.85rem;
}
footer a { color: var(--accent); }

@media (max-width: 640px) {
  body { padding: 20px 12px; }
  table { font-size: 0.78rem; }
  th, td { padding: 6px 8px; }
  h1 { font-size: 1.5rem; }
}"""


def convert_report(filepath, company_name, ticker, title_suffix):
    """将一份报告转换为大灰皮风格"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 提取 <body> 到 </body> 之间的内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body_match:
        print(f"  ✗ 无法找到 body: {filepath}")
        return False
    body = body_match.group(1)

    # 2. 移除目录 div (<div class="toc">...</div>)
    body = re.sub(r'<div class="toc">.*?</div>\s*', '', body, flags=re.DOTALL)

    # 3. 移除 .header-meta div
    body = re.sub(r'<div class="header-meta">.*?</div>\s*', '', body, flags=re.DOTALL)

    # 4. 替换 h1 标题（添加大灰皮品牌）
    # 匹配 <h1>...</h1> 或 <h1 id="...">...</h1>
    old_h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    h1_match = re.search(old_h1_pattern, body, re.DOTALL)
    if h1_match:
        old_title = h1_match.group(1).strip()
        # 清理标题中的 "深度分析报告" 后缀，重新拼接
        clean_title = re.sub(r'深度分析报告\s*$', '', old_title).strip()
        new_title = f'{clean_title} — 大灰皮证券研究深度分析报告'
        body = re.sub(old_h1_pattern, f'<h1>{new_title}</h1>', body, count=1)

    # 5. 替换章节格式：第X章：→ 第X章 |
    body = re.sub(r'第(\d+)章：', r'第\1章 | ', body)

    # 6. 移除"分析师：小八"行
    body = re.sub(r'<p[^>]*><strong>分析师：</strong>\s*小八[^<]*</p>\s*', '', body)

    # 7. 移除"结论先行"相关内容（保留结论文字但去掉"结论先行"标签）
    # 将 "结论先行" 的 blockquote 转为普通段落
    body = re.sub(r'<strong>结论先行：</strong>\s*', '<strong>前置结论：</strong> ', body)

    # 8. 移除"小八的观点"章节（h3 或 h2 级别）
    # 匹配 <h3>8.3 小八的观点</h3> 及其后续内容直到下一个 h2/h3
    body = re.sub(r'<h[23][^>]*>\s*8\.3\s*小八的观点\s*</h[23]>.*?(?=<h[23])', '', body, flags=re.DOTALL)
    # 也匹配可能不带编号的
    body = re.sub(r'<h[23][^>]*>小八的观点</h[23]>.*?(?=<h[23])', '', body, flags=re.DOTALL)

    # 9. 移除"四巨头排序"章节
    body = re.sub(r'<h[23][^>]*>\s*四巨头排序\s*</h[23]>.*?(?=<h[23]|<h1|</div>|<footer|$)', '', body, flags=re.DOTALL)

    # 10. 移除"核心逻辑总结"章节（如果是额外的非标准章节）
    # 保留如果它属于第10章的子章节

    # 11. 确保 <h2> 用于第X章，<h3> 用于子章节
    # 新版用 h2 作章节标题，h3 作子章节 — 这与旧版一致

    # 12. 将 <hr> 替换为 <hr />（保持一致）
    body = body.replace('<hr>', '<hr />')
    body = body.replace('<hr/>', '<hr />')

    # 13. 移除尾部的免责声明（如果有），因为模板有自己的 footer
    body = re.sub(r'<p[^>]*><em>本报告[^<]*</em></p>\s*', '', body)

    # 14. 清理多余空行
    body = re.sub(r'\n{3,}', '\n\n', body)

    # 15. 组装最终 HTML
    final_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company_name} ({ticker}) — 大灰皮证券研究深度分析报告 — 大灰皮证券研究</title>
<style>
{TEMPLATE_CSS}
</style>
</head>
<body>
<div class="container">
  <a class="back-link" href="./index.html">&larr; 返回报告列表</a>
{body}
  <footer>
    <p>基于 <a href="https://github.com/abuzhabi/company_report">大灰皮证券研究统一框架</a> &middot; Evidence First &middot; 仅供研究参考，不构成投资建议</p>
  </footer>
</div>
</body>
</html>
"""
    # 清理 body 内容前后的空白
    final_html = re.sub(r'(  <a class="back-link"[^>]*>.*?</a>\n)\s+', r'\1', final_html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"  ✓ 已转换: {os.path.basename(filepath)}")
    return True


def main():
    reports = [
        ("AMD", "AMD", "AMD",
         "reports/AMD/2026-06-30_AMD_深度分析报告.html"),
        ("苹果", "Apple", "AAPL",
         "reports/苹果/2026-06-30_苹果_深度分析报告.html"),
        ("英特尔", "Intel", "INTC",
         "reports/英特尔/2026-06-30_英特尔_深度分析报告.html"),
        ("英伟达", "NVIDIA", "NVDA",
         "reports/英伟达/2026-06-30_英伟达_深度分析报告.html"),
        ("SpaceX", "SpaceX", "-private-",
         "reports/SpaceX/2026-06-30_SpaceX_深度分析报告.html"),
        ("洛克希德马丁", "Lockheed Martin", "LMT",
         "reports/洛克希德马丁/2026-06-30_洛克希德马丁_深度分析报告.html"),
    ]

    os.chdir("/Users/abuzhabi/Workbuddy/Claw/outputs")

    success = 0
    for cn_name, en_name, ticker, rel_path in reports:
        print(f"\n处理: {cn_name} ({en_name})")
        if convert_report(rel_path, en_name, ticker, cn_name):
            success += 1

    print(f"\n完成！成功转换 {success}/{len(reports)} 份报告")


if __name__ == "__main__":
    main()
