import redis
import json
from typing import Dict, Any, Optional
from ai.config.celeryconfig_dev import employee_catch

class EmployeeCacheService:
    """员工信息缓存服务"""
    
    def __init__(self):
        self.redis_client = redis.from_url(employee_catch, decode_responses=True)
        self.cache_prefix = "employee_access:"
        self.cache_expire = 3600*24*365  # 1年过期

    def _get_cache_key(self, token: str) -> str:
        """生成缓存键
        
        Args:
            token: 员工token
            
        Returns:
            str: 缓存键
        """
        return f"{self.cache_prefix}{token}"

    def get_from_cache(self, token: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据
        
        Args:
            token: 员工token
            
        Returns:
            Optional[Dict[str, Any]]: 缓存的数据，如果不存在则返回None
        """
        try:
            cached_data = self.redis_client.get(self._get_cache_key(token))
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Error getting from cache: {str(e)}")
        return None

    def set_to_cache(self, token: str, data: Dict[str, Any]) -> None:
        """将数据存入缓存
        
        Args:
            token: 员工token
            data: 要缓存的数据
        """
        try:
            self.redis_client.setex(
                self._get_cache_key(token),
                self.cache_expire,
                json.dumps(data)
            )
        except Exception as e:
            print(f"Error setting cache: {str(e)}")

    def delete_from_cache(self, token: str) -> None:
        """从缓存中删除数据
        
        Args:
            token: 员工token
        """
        try:
            self.redis_client.delete(self._get_cache_key(token))
        except Exception as e:
            print(f"Error deleting from cache: {str(e)}")

    def clear_all_cache(self) -> None:
        """清除所有员工相关的缓存"""
        try:
            pattern = f"{self.cache_prefix}*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Error clearing cache: {str(e)}")

    def get_employee_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """通过token从缓存中获取员工信息
        
        Args:
            token: 员工token
            
        Returns:
            Optional[Dict[str, Any]]: 员工信息，格式如下：
            {
                "user_name": str,
                "user_group": str,
                "employee_token": str,
                "user_info": {
                    "user_name": str,
                    "user_group": str,
                },
                "employee_info": {
                    "employee_id": str,
                    "employee_name": str,
                    "employee_cn_name": str
                },
                "employee_accesses": [
                    {
                        "employee_id": str,
                        "workflow": str,
                        "workflow_name": str,
                        "product_type": str,
                        "platform": str,
                        "category_id": str,
                        "shop_name": str,
                        "template_id": str
                    }
                ]
            }
            如果缓存中不存在，则返回None
        """
        return self.get_from_cache(token) 