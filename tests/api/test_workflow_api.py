import requests
import time
import json
import os
from datetime import datetime

class TestWorkflowAPI:
    """工作流 API 测试类"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.test_data = {
            "message": "Hello World",
            "timestamp": datetime.now().isoformat()
        }
    
    def test_trigger_workflow(self):
        """测试触发工作流"""
        print("\n=== 测试触发工作流 ===")
        
        # 发送请求
        response = requests.post(
            f"{self.base_url}/trigger-workflow",
            json=self.test_data
        )
        
        # 打印请求和响应信息
        print(f"请求 URL: {response.url}")
        print(f"请求数据: {json.dumps(self.test_data, indent=2)}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(response.json(), indent=2)}")
        
        # 验证响应
        assert response.status_code == 200
        assert "event_id" in response.json()
        assert response.json()["status"] == "success"
        
        return response.json()["event_id"]
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始 API 测试...")
        
        try:
            # 测试触发工作流
            event_id = self.test_trigger_workflow()
            print(f"测试通过！事件 ID: {event_id}")
            
        except Exception as e:
            print(f"测试失败: {str(e)}")
            raise e

if __name__ == "__main__":
    # 确保服务已启动
    print("请确保服务已在运行 (python src/main.py)")
    input("按回车键开始测试...")
    
    # 运行测试
    tester = TestWorkflowAPI()
    tester.run_all_tests() 