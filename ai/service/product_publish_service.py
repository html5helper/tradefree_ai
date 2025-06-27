from sqlalchemy.orm import Session
from ai.dao.db.engine import workflow_engine
from ai.dao.entity.product_publish_history import ProductPublishHistory
from datetime import datetime, timedelta


class ProductPublishService:
    def __init__(self):
        self.session = Session(bind=workflow_engine)

    def save(self, product_publish_history: ProductPublishHistory) -> bool:
        """添加或更新发品历史
        
        Args:
            product_publish_history: 发品历史
            
        Returns:
            bool: 是否操作成功
        """
        try:
            trace_id = product_publish_history.trace_id
            item = self.session.query(ProductPublishHistory).filter_by(trace_id=trace_id).first()
            if item: 
                # 已存在，更新整个对象的值
                item.last_task_id = product_publish_history.last_task_id
                item.last_task_type = product_publish_history.last_task_type
                item.last_task_name = product_publish_history.last_task_name
                item.last_task_status = product_publish_history.last_task_status
                item.updated_at = product_publish_history.updated_at
                self.session.commit()
            else: #add
                self.session.add(product_publish_history)
                self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error saving product publish history: {str(e)}")
            return False
        finally:
            self.session.close()

    def get(self, product_publish_id: int) -> ProductPublishHistory:
        """获取发品历史
        
        Args:
            product_publish_id: 发品历史ID
            
        Returns:
            ProductPublishHistory: 发品历史
        """
        try:
            return self.session.query(ProductPublishHistory).filter_by(id=product_publish_id).first()
        except Exception as e:
            print(f"Error getting product publish history: {str(e)}")
            return None
        finally:
            self.session.close()

    def get_by_trace_id(self, trace_id: str) -> ProductPublishHistory:
        """根据 trace_id 获取发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            
        Returns:
            ProductPublishHistory: 发品历史
        """
        try:
            return self.session.query(ProductPublishHistory).filter_by(trace_id=trace_id).first()
        except Exception as e:
            print(f"Error getting product publish history by trace_id: {str(e)}")
            return None
        finally:
            self.session.close()

    def update(self, trace_id: str, changes: dict) -> ProductPublishHistory:
        """更新发品历史
        
        Args:
            trace_id: 发品workflow trace_id
            changes: 更新内容
            
        Returns:
            ProductPublishHistory: 更新后的发品历史
        """
        try:
            product_publish_history = self.session.query(ProductPublishHistory).filter_by(trace_id=trace_id).first()
            if product_publish_history:
                for key, value in changes.items():
                    if hasattr(product_publish_history, key):
                        setattr(product_publish_history, key, value)
                self.session.commit()
                return product_publish_history
            return None
        except Exception as e:
            self.session.rollback()
            print(f"Error updating product publish history: {str(e)}")
            return None
        finally:
            self.session.close()

    def collect_list(self, employee_id: str, platform: str, product_type: str) -> list[ProductPublishHistory]:
        """根据员工ID和平台和产品类型获取近7天采集列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[ProductPublishHistory]: 发品历史列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            return self.session.query(ProductPublishHistory).filter(
                ProductPublishHistory.employee_id == employee_id,
                ProductPublishHistory.dest_platform == platform,
                ProductPublishHistory.product_type == product_type,
                ProductPublishHistory.collect_status != None,
                ProductPublishHistory.created_at >= start_time
            ).order_by(ProductPublishHistory.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting product publish collect list: {str(e)}")
            return []
        finally:
            self.session.close()

    def generate_list(self, employee_id: str, platform: str, product_type: str) -> list[ProductPublishHistory]:
        """根据员工ID和平台和产品类型获取近7天生成列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[ProductPublishHistory]: 发品历史列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            return self.session.query(ProductPublishHistory).filter(
                ProductPublishHistory.employee_id == employee_id,
                ProductPublishHistory.dest_platform == platform,
                ProductPublishHistory.product_type == product_type,
                ProductPublishHistory.generate_status != None,
                ProductPublishHistory.created_at >= start_time
            ).order_by(ProductPublishHistory.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting product publish generate list: {str(e)}")
            return []
        finally:
            self.session.close()

    def publish_list(self, employee_id: str, platform: str, product_type: str) -> list[ProductPublishHistory]:
        """根据员工ID和平台和产品类型获取发布列表
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
        Returns:
            list[ProductPublishHistory]: 发品历史列表
        """
        try:
            # 获取当前时间
            now = datetime.now()
            # 获取开始时间，减去7天
            start_time = now - timedelta(days=7)

            return self.session.query(ProductPublishHistory).filter(
                ProductPublishHistory.employee_id == employee_id,
                ProductPublishHistory.dest_platform == platform,
                ProductPublishHistory.product_type == product_type,
                ProductPublishHistory.generate_status == 'SUCCESS',
                ProductPublishHistory.publish_status != 'SUCCESS',
                ProductPublishHistory.created_at >= start_time
            ).order_by(ProductPublishHistory.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting product publish publish list: {str(e)}")
            return []
        finally:
            self.session.close()

    def published_list(self, employee_id: str, platform: str, product_type: str,start_time: datetime,end_time: datetime) -> list[ProductPublishHistory]:
        """根据员工ID和平台和产品类型获取已发布列表，并根据开始时间和结束时间过滤
        Args:
            employee_id: 员工ID
            platform: 平台
            product_type: 产品类型
            start_time: 开始时间
            end_time: 结束时间
        Returns:    
            list[ProductPublishHistory]: 发品历史列表
        """
        try:
            return self.session.query(ProductPublishHistory).filter(
                ProductPublishHistory.employee_id == employee_id,
                ProductPublishHistory.dest_platform == platform,
                ProductPublishHistory.product_type == product_type,
                ProductPublishHistory.publish_status == 'SUCCESS',
                ProductPublishHistory.created_at >= start_time,
                ProductPublishHistory.created_at <= end_time
            ).order_by(ProductPublishHistory.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting product publish published list: {str(e)}")
            return []


    def delete_by_trace_id(self, trace_id: str) -> bool:
        """根据 trace_id 删除发品历史
        
        Args:
            trace_id: 发品workflow trace_id
        """
        try:
            self.session.query(ProductPublishHistory).filter_by(trace_id=trace_id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting product publish history by trace_id: {str(e)}")
            return False
        finally:
            self.session.close()

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 