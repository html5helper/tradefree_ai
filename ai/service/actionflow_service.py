from sqlalchemy.orm import Session
from ai.dao.db.engine import manager_engine
from ai.dao.entity.action_flow import ActionFlow

class ActionFlowService:
    def __init__(self):
        self.session = Session(bind=manager_engine)

    def add(self, action_flow: ActionFlow) -> bool:
        """添加发品事件流
        
        Args:
            action_flow: 发品事件流
            
        Returns:
            bool: 是否添加成功
        """
        try:
            self.session.add(action_flow)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding task event: {str(e)}")
            return False
        finally:
            self.session.close()

    def get(self, action_flow_id: int) -> ActionFlow:
        """获取发品事件流
        
        Args:
            action_flow_id: 发品事件流ID
            
        Returns:
            ActionFlow: 发品事件流
        """
        try:
            return self.session.query(ActionFlow).filter_by(id=action_flow_id).first()
        except Exception as e:
            print(f"Error getting action flow: {str(e)}")
            return None
        finally:
            self.session.close()

    def get_by_ids(self, ids: list) -> list:
        """获取发品事件流
        
        Args:
            ids: 发品事件流ID列表
            
        Returns:
            list: 发品事件流字典列表
        """
        try:
            results = self.session.query(ActionFlow).filter(ActionFlow.id.in_(ids)).all()
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting action flow: {str(e)}")
            return []
        finally:
            self.session.close()

    def update(self, action_flow_id: int, changes: dict) -> ActionFlow:
        """更新发品事件流
        
        Args:
            action_flow_id: 发品事件流ID
            changes: 更新内容
            
        Returns:
            bool: 是否更新成功
        """
        try:
            action_flow = self.session.query(ActionFlow).filter_by(id=action_flow_id).first()
            if action_flow:
                for key, value in changes.items():
                    setattr(action_flow, key, value)
                self.session.commit()
                return action_flow
            return None
        except Exception as e:
            self.session.rollback()
            print(f"Error updating action flow: {str(e)}")
        finally:
            self.session.close()

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 