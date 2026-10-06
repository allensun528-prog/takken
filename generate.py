from openpyxl import load_workbook
from html import escape
from pathlib import Path


# =========================
# 文件设置
# =========================

BASE_DIR = Path(__file__).resolve().parent

EXCEL_FILE = BASE_DIR / "answer.xlsx"
OUTPUT_FILE = BASE_DIR / "index.html"


# =========================
# 读取 Excel
# =========================

wb = load_workbook(EXCEL_FILE, data_only=True)
ws = wb["知識点"]


items = []

for row in ws.iter_rows(min_row=2, values_only=True):

    # Excel 五列：
    # ID / 答案 / 前半段 / 后半段 / 分类
    item_id, answer, front, back, category = row

    # 空行跳过
    if item_id is None:
        continue

    item_id = str(item_id)
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

    <span>{front}</span>

    <span
        class="answer"
        tabindex="0"
        role="button"
    >{answer}</span>

    <span>{back}</span>

</li>
''')

    content.append('</ul>')


knowledge_html = "\n".join(content)


# =========================
# HTML 模板
# =========================

html = f'''<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>宅建知識</title>

<link rel="stylesheet" href="style.css">

</head>


<body>

<main>

<h1>宅建知識</h1>

{knowledge_html}

</main>


<script src="app.js"></script>

</body>

</html>
'''


# =========================
# 输出 HTML
# =========================

OUTPUT_FILE.write_text(
    html,
    encoding="utf-8"
)

print("HTML生成完成！")
print(f"输出文件：{OUTPUT_FILE}")
print(f"知识点数量：{len(items)}")
