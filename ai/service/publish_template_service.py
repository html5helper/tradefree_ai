from sqlalchemy.orm import Session
from ai.dao.db.engine import manager_engine
from ai.dao.entity.publish_template import PublishTemplate

class PublishTemplateService:
    def __init__(self):
        self.session = Session(bind=manager_engine)

    def add(self, publish_template: PublishTemplate) -> bool:
        """添加发品模板
        
        Args:
            publish_template: 发品模板
            
        Returns:
            bool: 是否添加成功
        """
        try:
            self.session.add(publish_template)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding task event: {str(e)}")
            return False
        finally:
            self.session.close()

    def get(self, publish_template_id: int) -> PublishTemplate:
        """获取发品模板
        
        Args:
            publish_template_id: 发品模板ID
            
        Returns:
            PublishTemplate: 发品模板
        """
        try:
            return self.session.query(PublishTemplate).filter_by(id=publish_template_id).first()
        except Exception as e:
            print(f"Error getting publish template: {str(e)}")
            return None
        finally:
            self.session.close()

    def get_by_ids(self, ids: list) -> list:
        """获取发品模板
        
        Args:
            ids: 发品模板ID列表
            
        Returns:
            list: 发品模板字典列表
        """
        try:
            results = self.session.query(PublishTemplate).filter(PublishTemplate.id.in_(ids)).all()
            # 在Session关闭前转换为字典列表
            return [result.to_dict() for result in results]
        except Exception as e:
            print(f"Error getting publish template: {str(e)}")
            return []
        finally:
            self.session.close()

    def update(self, publish_template_id: int, changes: dict) -> PublishTemplate:
        """更新发品模板
        
        Args:
            publish_template_id: 发品模板ID
            changes: 更新内容
            
        Returns:
            bool: 是否更新成功
        """
        try:
            publish_template = self.session.query(PublishTemplate).filter_by(id=publish_template_id).first()
            if publish_template:
                for key, value in changes.items():
                    setattr(publish_template, key, value)
                self.session.commit()
                return publish_template
            return None
        except Exception as e:
            self.session.rollback()
            print(f"Error updating publish template: {str(e)}")
        finally:
            self.session.close()

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 