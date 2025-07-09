from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.product_history import ProductHistory
from datetime import datetime, timedelta
import json

class ProductHistoryService:
    def __init__(self):
        self.session = Session(bind=workflow_engine)

    def save_or_update(self, product_history: ProductHistory) -> bool:
        """添加或更新发品历史
        
        Args:
            product_history: 发品历史
            
        Returns:
            bool: 是否操作成功
        """
        try:
            trace_id = product_history.trace_id
            item = self.session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if item: 
                # 已存在，更新整个对象的值
                item.last_task_id = product_history.last_task_id
                item.last_task_type = product_history.last_task_type
                item.last_task_name = product_history.last_task_name
                item.last_task_status = product_history.last_task_status
                item.updated_at = product_history.updated_at
                self.session.commit()
            else: #add
                self.session.add(product_history)
                self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error saving product history: {str(e)}")
            return False
        finally:
            self.session.close()

    def get(self, product_history_id: int) -> dict:
        """获取发品历史
        
        Args:
            product_history_id: 发品历史ID
            
        Returns:
            dict: 发品历史数据字典
        """
        try:
            result = self.session.query(ProductHistory).filter_by(id=product_history_id).first()
            if result:
                # 在Session关闭前转换为字典
                return result.to_dict()
            return None
        except Exception as e:
            print(f"Error getting product history: {str(e)}")
            return None
        finally:
            self.session.close()

    def get_by_trace_id(self, trace_id: str) -> dict:
        """根据 trace_id 获取发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            
        Returns:
            dict: 发品历史数据字典
        """
        try:
            result = self.session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if result:
                # 在Session关闭前转换为字典
                return result.to_dict()
            return None
        except Exception as e:
            print(f"Error getting product history by trace_id: {str(e)}")
            return None
        finally:
            self.session.close()

    def update(self, trace_id: str, changes: dict) -> dict:
        """更新发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            changes: 更新内容
            
        Returns:
            dict: 更新后的发品历史数据字典
        """
        try:
            product_history = self.session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if product_history:
                for key, value in changes.items():
                    if hasattr(product_history, key):
                        setattr(product_history, key, value)
                self.session.commit()
                # 在Session关闭前转换为字典
                return product_history.to_dict()
            else:
                return None
        except Exception as e:
            self.session.rollback()
            print(f"Error updating product history: {str(e)}")
            return None
        finally:
            self.session.close()

    def collect_list(self, employee_id: str, platform: str, product_type: str) -> list[dict]:
        """根据员工ID和平台和产品类型获取近7天采集列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[dict]: 发品历史数据字典列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.collect_status != None,
                ProductHistory.created_at >= start_time
            ).order_by(ProductHistory.created_at.desc()).limit(200)
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product publish collect list: {str(e)}")
            return []
        finally:
            self.session.close()

    def generate_list(self, employee_id: str, platform: str, product_type: str) -> list[dict]:
        """根据员工ID和平台和产品类型获取近7天生成列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[dict]: 发品历史数据字典列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.generate_status != None,
                ProductHistory.created_at >= start_time
            ).order_by(ProductHistory.created_at.desc()).limit(200)
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product publish generate list: {str(e)}")
            return []
        finally:
            self.session.close()

    def publish_list(self, employee_id: str, platform: str, product_type: str) -> list[dict]:
        """根据员工ID和平台和产品类型获取发布列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[dict]: 发品历史数据字典列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.generate_status == 'SUCCESS',
                ProductHistory.publish_status != 'SUCCESS',
                ProductHistory.created_at >= start_time
            ).order_by(ProductHistory.created_at.desc()).limit(200)
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product publish publish list: {str(e)}")
            return []
        finally:
            self.session.close()

    def published_list(self, employee_id: str, platform: str, product_type: str,start_date: str,end_date: str) -> list[dict]:
        """根据员工ID和平台和产品类型获取已发布列表，并根据开始时间和结束时间过滤
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
            start_time: 开始时间
            end_time: 结束时间
        Returns:    
            list[dict]: 发品历史数据字典列表
        """
        try:
            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.publish_status == 'SUCCESS',
                ProductHistory.created_at >= start_date + ' 00:00:00',
                ProductHistory.created_at <= end_date + ' 23:59:59'
            ).order_by(ProductHistory.created_at.desc()).limit(300)
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product publish published list: {str(e)}")
            return []
        finally:
            self.session.close()

    def recent_list(self, employee_id: str, platform: str, product_type: str) -> list[dict]:
        """根据员工ID和平台和产品类型获取最近7天接收列表，并根据开始时间和结束时间过滤
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:    
            list[dict]: 发品历史数据字典列表
        """
        try:
            now = datetime.now()
            start_time = now - timedelta(days=7)
            start_time_str = start_time.strftime('%Y-%m-%d 00:00:00')
            
            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.created_at >= start_time_str
            ).order_by(ProductHistory.created_at.desc()).limit(300)
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product publish published list: {str(e)}")
            return []
        finally:
            self.session.close() 

    def delete_by_trace_id(self, trace_id: str) -> bool:
        """根据 trace_id 删除发品历史
        
        Args:
            trace_id: 发品workflow trace_id
        """
        try:
            self.session.query(ProductHistory).filter_by(trace_id=trace_id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting product history by trace_id: {str(e)}")
            return False
        finally:
            self.session.close()

    def publish_success(self, trace_id: str,new_product_id: str) -> bool:
        """根据 trace_id 更新发品历史
        
        Args:
            trace_id: Product History trace_id
            new_product_id: 新产品ID
        """
        try:
            product_history = self.session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            generate_product = product_history.generate_product
            generate_product_json = json.loads(generate_product)
            generate_product_json['new_product_id'] = new_product_id
            generate_product = json.dumps(generate_product_json)
            if product_history:
                product_history.publish_status = 'SUCCESS'
                product_history.publish_product = generate_product
                product_history.updated_at = datetime.now()
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error updating product history publish success: {str(e)}")
            return False
        finally:
            self.session.close()

    def update_generate_product_by_trace_id(self, trace_id: str, generate_product: str) -> bool:
        """根据 trace_id 更新发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            generate_product: 发品历史数据字典
        """
        try:
            product_history = self.session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if product_history:
                # Convert dictionary to JSON string before storing in Text field
                product_history.generate_product = generate_product
                product_history.generate_status = 'SUCCESS'
                product_history.publish_status = 'PENDING'
                product_history.publish_product = None
                product_history.updated_at = datetime.now()
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error updating product history by trace_id: {str(e)}")
            return False
        finally:
            self.session.close()
    
    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 