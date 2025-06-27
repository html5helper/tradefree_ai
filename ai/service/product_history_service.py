from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.product_history import ProductHistory

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

    # 使用关键字参数，避免位置参数问题
    def list_by_employee_and_platform_and_product_type(self, employee_id: str, platform: str, product_type: str, status_list: list[str]) -> list[dict]:
        """根据员工ID和平台和产品类型获取发品历史
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
            status_list: 状态列表，用于过滤
        Returns:
            list[dict]: 发品历史数据字典列表
        """
        try:
            # ProductHistory 没有 status 字段，需要根据具体的状态字段进行过滤
            # 这里暂时返回所有匹配的记录，后续可以根据需要添加状态过滤逻辑
            results = self.session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type
            ).order_by(ProductHistory.created_at.desc()).all()
            
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting product history: {str(e)}")
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

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 