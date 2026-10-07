from openpyxl import load_workbook
from html import escape
from pathlib import Path


# =========================
# 文件位置
# =========================

BASE_DIR = Path(__file__).resolve().parent

EXCEL_FILE = BASE_DIR / "answer.xlsx"
OUTPUT_FILE = BASE_DIR / "index.html"


# =========================
# 读取 Excel
# =========================

wb = load_workbook(EXCEL_FILE, data_only=True)
ws = wb.active

items = []

for row in ws.iter_rows(min_row=2, values_only=True):

    item_id, answer, front, back, category = row[:5]

    # ID 为空则跳过
    if item_id is None:
        continue

    item_id = str(item_id).strip()
    answer = "" if answer is None else str(answer)
    front = "" if front is None else str(front)
    back = "" if back is None else str(back)
    category = "" if category is None else str(category)

    items.append({
        "id": item_id,
        "answer": answer,
        "front": front,
        "back": back,
        "category": category
    })


# =========================
# 按分类整理
# =========================

categories = {}

for item in items:

    category = item["category"]

    if category not in categories:
        categories[category] = []

    categories[category].append(item)


# =========================
# 生成知识点 HTML
# =========================

content = []

for category, category_items in categories.items():

    if category:
        content.append(
            f'<h2>{escape(category)}</h2>'
        )

    content.append(
        '<ul class="knowledge-list">'
    )

    for item in category_items:

        item_id = escape(item["id"])
        answer = escape(item["answer"])
        front = escape(item["front"])
        back = escape(item["back"])

        content.append(f'''
<li class="item" data-id="{item_id}">

    <input
        class="item-check"
        type="checkbox"
    >

    <span class="front">
        {front}
    </span>

    <span
        class="answer"
        tabindex="0"
        role="button"
    >
        {answer}
    </span>

    <span class="back">
        {back}
    </span>

</li>
''')

    content.append('</ul>')


knowledge_html = "\n".join(content)


# =========================
# 生成完整 HTML
# =========================

html = f'''<!DOCTYPE html>
<html lang="ja">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>宅建知識</title>


<style>

/* =========================
   答案隐藏 / 显示
   ========================= */

.answer {{
    color: transparent;
    background: #ddd;
    cursor: pointer;
    border-radius: 3px;
    padding: 0 8px;
}}

.answer.show {{
    color: inherit;
    background: transparent;
}}


/* =========================
   基本样式
   ========================= */

body {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    line-height: 1.6;
}}

.knowledge-list {{
    padding-left: 0;
}}

.item {{
    list-style: none;
    margin: 8px 0;
}}

.item-check {{
    margin-right: 8px;
}}

.front {{
    margin-right: 4px;
}}

.back {{
    margin-left: 4px;
}}

h2 {{
    margin-top: 30px;
}}

</style>

</head>


<body>

<main>

<h1>宅建知識</h1>

{knowledge_html}

</main>


<!-- Firebase / app.js -->

<script
    type="module"
    src="app.js"
></script>

</body>

</html>
'''


# =========================
# 写入 index.html
# =========================

OUTPUT_FILE.write_text(
    html,
    encoding="utf-8"
)


# =========================
# 完成提示
# =========================

print("================================")
print("HTML生成完成！")
print("================================")
print(f"Excel：{EXCEL_FILE.name}")
print(f"HTML ：{OUTPUT_FILE.name}")
print(f"知识点数量：{len(items)}")
print("================================")
