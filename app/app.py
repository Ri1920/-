from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 定义分类函数
def classify_entries(data):
    results = []
    for entry in data:
        entry = entry.strip()
        if not entry:
            continue

        # 提取电话号码
        phone_number = ''.join(filter(str.isdigit, entry.split()[-1]))

        # 判断性别
        if any(keyword in entry for keyword in
               ['小姐', '嫂', '姨', '欣', '美', '玲', '婷', '婉', '芳', '麗', '珊', '雪', '妈妈', '姐', '妹', '珮']):
            gender = '女'
        elif any(keyword in entry for keyword in
                 ['生', '哥', '弟', '叔', '伯', '志', '偉', '俊', '健', '明', '仔', '爸', '傑', '宇', '宏', '淇',
                  '毅']):
            gender = '男'
        else:
            gender = '不明确'

        # 判断地区
        if phone_number.startswith('6') and len(phone_number) == 8:
            region = '澳门'
        elif phone_number.startswith('852') or (phone_number.startswith('9') and len(phone_number) == 8):
            region = '香港'
        elif phone_number.startswith('65') and len(phone_number) == 8:
            region = '新加坡'
        elif phone_number.startswith('86') and len(phone_number) == 11:
            region = '中国'
        else:
            region = '未知地区'

        results.append({"entry": entry, "gender": gender, "phone_number": phone_number, "region": region})

    return results

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 数据处理路由
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # 使用 get_json() 获取 JSON 数据
    entries = data.get('data', [])
    results = classify_entries(entries)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
