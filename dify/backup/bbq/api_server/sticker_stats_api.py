import json
import requests
import io
from flask import request, jsonify
from sticker_stats_json import analyze_numeric_field, count_sales_by_place, count_sales_by_price_range, count_sales_by_dimension

# 直接从文件流读取JSONL数据
def load_jsonl_from_stream(stream):
    data = []
    for line in stream:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        line = line.strip()
        if line:  # 跳过空行
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
    return data

def analyze_sticker_data_route():
    """处理JSONL文件或URL，返回统计分析结果"""
    if 'file' not in request.files and 'file_url' not in request.form:
        return jsonify({'error': '请提供JSONL文件或文件URL'}), 400
    
    try:
        # 处理上传的文件
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': '未选择文件'}), 400
            
            # 直接从文件流读取数据
            data = load_jsonl_from_stream(file)
        
        # 处理文件URL
        elif 'file_url' in request.form:
            file_url = request.form['file_url']
            try:
                response = requests.get(file_url)
                response.raise_for_status()
                
                # 直接从响应内容读取数据
                content = response.content
                data = load_jsonl_from_stream(io.BytesIO(content))
            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'下载文件失败: {str(e)}'}), 400
        if not data:
            return jsonify({'error': '无法解析JSONL文件或文件为空'}), 400
        
        # 统计结果
        result = {}
        
        # 1. 商品总数
        result['total_products'] = len(data)
        
        # 2. 总销量 & 均价
        buy_cnt_stats = analyze_numeric_field(data, 'buy_cnt')
        price_stats = analyze_numeric_field(data, 'price')
        
        result['total_sales'] = buy_cnt_stats.get('sum', 0)
        result['average_price'] = price_stats.get('mean', 0)
        
        # 3. 按地域的销量分布
        result['summary_by_place'] = count_sales_by_place(data)
        
        # 4. 按价格带的销量分布
        result['sales_by_price_range'] = count_sales_by_price_range(data)
        
        # 5. 按各维度的销量统计
        dimensions = ['category', 'scence', 'group', 'function', 'feature', 'color', 'others']
        for dimension in dimensions:
            result[f'summary_by_{dimension}'] = count_sales_by_dimension(data, dimension)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'处理数据时出错: {str(e)}'}), 500
    
    finally:
        # 不需要清理临时文件，因为我们直接使用文件流
        pass