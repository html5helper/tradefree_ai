from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json
Base = declarative_base()

# CREATE TABLE `publish_template` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `platform` varchar(255) NOT NULL COMMENT '电商平台',
#   `shop_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT '店铺ID',
#   `product_type` varchar(255) NOT NULL COMMENT '业务类型',
#   `category_id` varchar(255) NOT NULL DEFAULT '' COMMENT '电商平台类目编号',
#   `category_name` varchar(255) NOT NULL DEFAULT '--' COMMENT '电商平台类目名称',
#   `template` longtext NOT NULL COMMENT '发品模板：toB为API模板，toC为插件发品模板',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`id`),
#   KEY `platform_product_type_category_id_IDX` (`platform`,`product_type`,`category_id`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;

class PublishTemplate(Base):
    """发品模板模型
    
    属性说明：
    - platform: 电商平台
    - shop_id: 店铺ID
    - product_type: 业务类型
    - category_id: 电商平台类目编号
    - category_name: 电商平台类目名称
    - template: 发品模板：toB为API模板，toC为插件发品模板
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "publish_template"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(255), nullable=False, comment='电商平台')
    shop_id = Column(Integer, nullable=False, default=-1, comment='店铺ID')
    product_type = Column(String(255), nullable=False, comment='业务类型')
    category_id = Column(String(255), nullable=False, default='', comment='电商平台类目编号')
    category_name = Column(String(255), nullable=False, default='--', comment='电商平台类目名称')
    template = Column(Text, nullable=False, comment='发品模板：toB为API模板，toC为插件发品模板')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return (
            f"<PublishTemplate(id={self.id}, "
            f"platform='{self.platform}', "
            f"shop_id={self.shop_id}, "
            f"product_type='{self.product_type}', "
            f"category_id='{self.category_id}', "
            f"category_name='{self.category_name}', "
            f"template='{self.template}')>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "platform": self.platform,
            "shop_id": self.shop_id,
            "product_type": self.product_type,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "template": json.loads(self.template),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }