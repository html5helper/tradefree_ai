import json
import os
from collections import Counter
import numpy as np
import math

# 读取JSONL文件
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
    return data

# 统计列表字段的分布
def count_list_field(data, field_name):
    counter = Counter()
    for item in data:
        if field_name in item and isinstance(item[field_name], list) and item[field_name]:
            for value in item[field_name]:
                counter[value] += 1
        else:
            # 当字段为空时，计为"OTHERS"
            counter["OTHERS"] += 1
    return dict(counter.most_common())

# 统计数值字段
def analyze_numeric_field(data, field_name):
    values = [item[field_name] for item in data if field_name in item and isinstance(item[field_name], (int, float))]
    if not values:
        return {}
    return {
        'count': len(values),
        'min': min(values),
        'max': max(values),
        'mean': sum(values) / len(values),
        'median': sorted(values)[len(values) // 2],
        'sum': sum(values)
    }

# 按地域统计销量分布
def count_sales_by_place(data):
    place_sales = {}
    place_counts = {}
    total_sales = sum(item.get('buy_cnt', 0) for item in data)
    total_products = len(data)
    
    for item in data:
        if 'buy_cnt' in item:
            place = item.get('place', 'OTHERS')
            buy_cnt = item['buy_cnt']
            
            if place not in place_sales:
                place_sales[place] = 0
                place_counts[place] = 0
            
            place_sales[place] += buy_cnt
            place_counts[place] += 1
    
    # 按销量排序
    sorted_places = sorted(place_sales.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for place, sales in sorted_places:
        count = place_counts[place]
        result.append({
            "name": place,
            "sales": sales,
            "product_count": count,
            "sales_percent": round(sales / total_sales, 4) if total_sales > 0 else 0,
            "count_percent": round(count / total_products, 4) if total_products > 0 else 0
        })
    
    return result

# 按价格带统计销量分布
def count_sales_by_price_range(data):
    # 动态计算价格区间（5个区间）
    prices = [item['price'] for item in data if 'price' in item]
    if not prices:
        return []
    
    min_price = min(prices)
    max_price = max(prices)
    
    # 确保最小价格为0
    min_price = 0
    
    # 计算区间范围
    range_size = (max_price - min_price) / 4  # 分成5个区间需要4个分割点
    
    # 创建价格区间
    price_ranges = []
    for i in range(4):
        start = min_price + i * range_size
        end = min_price + (i + 1) * range_size
        # 四舍五入到整数，除非是小数
        start_rounded = math.floor(start) if start == int(start) else round(start, 1)
        end_rounded = math.ceil(end) if end == int(end) else round(end, 1)
        
        if i == 0:
            range_name = f"{start_rounded}-{end_rounded}元"
        else:
            range_name = f"{start_rounded}-{end_rounded}元"
        
        price_ranges.append((start, end, range_name))
    
    # 添加最后一个区间
    last_start = min_price + 4 * range_size
    last_start_rounded = math.floor(last_start) if last_start == int(last_start) else round(last_start, 1)
    price_ranges.append((last_start, float('inf'), f"{last_start_rounded}元以上"))
    
    # 统计每个价格区间的销量和产品数
    price_range_data = {pr[2]: {'sales': 0, 'count': 0} for pr in price_ranges}
    total_sales = sum(item.get('buy_cnt', 0) for item in data)
    total_products = len(data)
    
    for item in data:
        if 'price' in item and 'buy_cnt' in item:
            price = item['price']
            buy_cnt = item['buy_cnt']
            
            for min_price, max_price, range_name in price_ranges:
                if min_price <= price < max_price:
                    price_range_data[range_name]['sales'] += buy_cnt
                    price_range_data[range_name]['count'] += 1
                    break
    
    # 转换为所需的输出格式
    result = []
    for range_name, stats in price_range_data.items():
        result.append({
            "name": range_name,
            "sales": stats['sales'],
            "product_count": stats['count'],
            "sales_percent": round(stats['sales'] / total_sales, 4) if total_sales > 0 else 0,
            "count_percent": round(stats['count'] / total_products, 4) if total_products > 0 else 0
        })
    
    return result

# 按分类维度统计销量
def count_sales_by_dimension(data, dimension):
    dimension_sales = {}
    dimension_counts = {}
    total_sales = sum(item.get('buy_cnt', 0) for item in data)
    total_products = len(data)
    
    for item in data:
        if 'buy_cnt' in item:
            buy_cnt = item['buy_cnt']
            
            # 处理维度字段
            if dimension in item and isinstance(item[dimension], list) and item[dimension]:
                for value in item[dimension]:
                    if value not in dimension_sales:
                        dimension_sales[value] = 0
                        dimension_counts[value] = 0
                    dimension_sales[value] += buy_cnt
                    dimension_counts[value] += 1
            else:
                # 当字段为空时，计为"OTHERS"
                if "OTHERS" not in dimension_sales:
                    dimension_sales["OTHERS"] = 0
                    dimension_counts["OTHERS"] = 0
                dimension_sales["OTHERS"] += buy_cnt
                dimension_counts["OTHERS"] += 1
    
    # 按销量排序
    sorted_dimensions = sorted(dimension_sales.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for dim_value, sales in sorted_dimensions:
        count = dimension_counts[dim_value]
        result.append({
            "name": dim_value,
            "sales": sales,
            "product_count": count,
            "sales_percent": round(sales / total_sales, 4) if total_sales > 0 else 0,
            "count_percent": round(count / total_products, 4) if total_products > 0 else 0
        })
    
    return result

# 主函数
def main():
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='统计JSONL文件中的商品数据')
    parser.add_argument('--input', '-i', type=str, default='/Users/qinbinbin/PycharmProjects/tradefree_ext/hz_sticker_labeled.jsonl',
                        help='输入的JSONL文件路径')
    parser.add_argument('--output', '-o', type=str, default='/Users/qinbinbin/PycharmProjects/tradefree_ext/stats_output',
                        help='输出目录路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 输入文件路径
    file_path = args.input
    
    # 创建输出目录
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载数据
    data = load_jsonl(file_path)
    
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
    
    # 保存结果为JSON文件
    output_file = os.path.join(output_dir, 'sticker_stats.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"统计结果已保存到: {output_file}")

if __name__ == "__main__":
    main()