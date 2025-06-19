from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json
Base = declarative_base()

# CREATE TABLE `action_flow` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `name` varchar(100) NOT NULL COMMENT 'actionflow名称',
#   `platform` varchar(800) NOT NULL COMMENT '发品平台',
#   `product_type` varchar(255) NOT NULL COMMENT '产品类型',
#   `category_id` varchar(255) NOT NULL COMMENT '发品品类编号',
#   `action_flow` text NOT NULL COMMENT '发品事件流模板',
#   `is_enable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class ActionFlow(Base):
    """发品事件流模板模型
    
    属性说明：
    - name: actionflow名称
    - platform: 发品平台
    - product_type: 产品类型
    - category_id: 发品品类编号
    - action_flow: 发品事件流模板
    - is_enable: 是否启用
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "action_flow"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment='actionflow名称')
    platform = Column(String(800), nullable=False, comment='发品平台')
    product_type = Column(String(255), nullable=False, comment='产品类型')
    category_id = Column(String(255), nullable=False, comment='发品品类编号')
    action_flow = Column(Text, nullable=False, comment='发品事件流模板')
    is_enable = Column(Boolean, nullable=False, default=True, comment='是否启用')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return (
            f"<ActionFlow(id={self.id}, "
            f"name='{self.name}', "
            f"platform='{self.platform}', "
            f"product_type='{self.product_type}', "
            f"category_id='{self.category_id}', "
            f"is_enable={self.is_enable})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "platform": self.platform,
            "product_type": self.product_type,
            "category_id": self.category_id,
            "action_flow": json.loads(self.action_flow),
            "is_enable": self.is_enable,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }