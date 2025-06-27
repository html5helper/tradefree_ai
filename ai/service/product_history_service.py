from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.product_history import ProductHistory

class ProductHistoryService:
    def __init__(self):
        self.session = None

    def _get_session(self):
        """获取数据库会话"""
        if self.session is None:
            self.session = Session(bind=workflow_engine)
        return self.session

    def save_or_update(self, product_history: ProductHistory) -> bool:
        """添加或更新发品历史
        
        Args:
            product_history: 发品历史
            
        Returns:
            bool: 是否操作成功
        """
        session = self._get_session()
        try:
            trace_id = product_history.trace_id
            item = session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if item: 
                # 已存在，更新整个对象的值
                item.last_task_id = product_history.last_task_id
                item.last_task_type = product_history.last_task_type
                item.last_task_name = product_history.last_task_name
                item.last_task_status = product_history.last_task_status
                item.updated_at = product_history.updated_at
                session.commit()
            else: #add
                session.add(product_history)
                session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error saving product history: {str(e)}")
            return False

    def get(self, product_history_id: int) -> ProductHistory:
        """获取发品历史
        
        Args:
            product_history_id: 发品历史ID
            
        Returns:
            ProductPublishHistory: 发品历史
        """
        session = self._get_session()
        try:
            return session.query(ProductHistory).filter_by(id=product_history_id).first()
        except Exception as e:
            print(f"Error getting product history: {str(e)}")
            return None

    def get_by_trace_id(self, trace_id: str) -> ProductHistory:
        """根据 trace_id 获取发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            
        Returns:
            ProductHistory: 发品历史
        """
        session = self._get_session()
        try:
            return session.query(ProductHistory).filter_by(trace_id=trace_id).first()
        except Exception as e:
            print(f"Error getting product history by trace_id: {str(e)}")
            return None

    def update(self, trace_id: str, changes: dict) -> ProductHistory:
        """更新发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            changes: 更新内容
            
        Returns:
            ProductHistory: 更新后的发品历史
        """
        session = self._get_session()
        try:
            product_history = session.query(ProductHistory).filter_by(trace_id=trace_id).first()
            if product_history:
                for key, value in changes.items():
                    if hasattr(product_history, key):
                        setattr(product_history, key, value)
                session.commit()
                return product_history
            else:
                return None
        except Exception as e:
            session.rollback()
            print(f"Error updating product history: {str(e)}")
            return None

    # 使用关键字参数，避免位置参数问题
    def list_by_employee_and_platform_and_product_type(self, employee_id: str, platform: str, product_type: str, status_list: list[str]) -> list[ProductHistory]:
        """根据员工ID和平台和产品类型获取发品历史
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
            status_list: 状态列表，用于过滤
        Returns:
            list[ProductHistory]: 发品历史列表
        """
        session = self._get_session()
        try:
            return session.query(ProductHistory).filter(
                ProductHistory.employee_id == employee_id,
                ProductHistory.dest_platform == platform,
                ProductHistory.product_type == product_type,
                ProductHistory.status.in_(status_list)
            ).order_by(ProductHistory.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting product history: {str(e)}")
            return []

    def delete_by_trace_id(self, trace_id: str) -> bool:
        """根据 trace_id 删除发品历史
        
        Args:
            trace_id: 发品workflow trace_id
        """
        session = self._get_session()
        try:
            session.query(ProductHistory).filter_by(trace_id=trace_id).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting product history by trace_id: {str(e)}")
            return False

    def close_session(self):
        """关闭数据库会话"""
        if self.session:
            self.session.close()
            self.session = None

    def __del__(self):
        """确保session被正确关闭"""
        self.close_session() 