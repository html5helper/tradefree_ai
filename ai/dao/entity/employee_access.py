from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE `employee_access` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `user_id` bigint(20) NOT NULL COMMENT '所属用户',
#   `employee_id` bigint(20) NOT NULL COMMENT '员工账号',
#   `workflow` varchar(800) NOT NULL COMMENT '工作流',
#   `workflow_name` varchar(255) NOT NULL DEFAULT '--' COMMENT '发品商店',
#   `src_platform` varchar(100) DEFAULT NULL COMMENT '来源平台',
#   `dest_platform` varchar(100) DEFAULT NULL,
#   `product_type` varchar(255) NOT NULL COMMENT '产品类型',
#   `shop_id` bigint(20) DEFAULT NULL COMMENT '店铺编号',
#   `shop_name` varchar(255) NOT NULL COMMENT '发品商店',
#   `category_id` varchar(100) NOT NULL DEFAULT '-' COMMENT '商品类目编号',
#   `template_id` bigint(20) NOT NULL COMMENT '发品模板',
#   `is_enable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`id`),
#   KEY `employer_access_user_name_IDX` (`user_id`,`employee_id`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;

class EmployeeAccess(Base):
    """员工访问权限模型
    
    属性说明：
    - user_id: 所属用户
    - employee_id: 员工账号ID
    - workflow: 工作流
    - workflow_name: 工作流名称
    - src_platform: 来源平台
    - dest_platform: 目标平台
    - product_type: 产品类型
    - shop_id: 店铺编号
    - shop_name: 发品商店
    - category_id: 商品类目编号
    - template_id: 发品模板ID
    - is_enable: 是否启用
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "employee_access"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment='所属用户')
    employee_id = Column(Integer, nullable=False, comment='员工账号')
    workflow = Column(String(800), nullable=False, comment='工作流')
    workflow_name = Column(String(255), nullable=False, comment='工作流名称')
    src_platform = Column(String(100), nullable=True, comment='来源平台')
    dest_platform = Column(String(100), nullable=True, comment='目标平台')
    product_type = Column(String(255), nullable=False, comment='产品类型')
    shop_id = Column(Integer, nullable=True, comment='店铺编号')
    shop_name = Column(String(255), nullable=False, comment='发品商店')
    category_id = Column(String(100), nullable=False, default='-', comment='商品类目编号')
    template_id = Column(Integer, nullable=False, comment='发品模板')
    is_enable = Column(Boolean, nullable=False, default=True, comment='是否启用')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return (
            f"<EmployeeAccess(id={self.id}, "
            f"user_id={self.user_id}, "
            f"employee_id={self.employee_id}, "
            f"workflow='{self.workflow}', "
            f"workflow_name='{self.workflow_name}', "
            f"src_platform='{self.src_platform}', "
            f"dest_platform='{self.dest_platform}', "
            f"product_type='{self.product_type}', "
            f"shop_id={self.shop_id}, "
            f"shop_name='{self.shop_name}', "
            f"category_id='{self.category_id}', "
            f"template_id={self.template_id}, "
            f"is_enable={self.is_enable})>"
        )