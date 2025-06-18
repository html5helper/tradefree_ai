from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE `employee` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `user_name` varchar(255) NOT NULL COMMENT '所属用户',
#   `employee_name` varchar(255) NOT NULL COMMENT '员工账号',
#   `employee_cn_name` varchar(255) DEFAULT '--',
#   `employee_token` varchar(255) NOT NULL COMMENT '员工账号token',
#   `is_enable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
#   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `employee_unique` (`employee_name`)
# ) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

class Employee(Base):
    """员工模型
    
    属性说明：
    - user_name: 所属用户
    - employee_name: 员工账号
    - employee_token: 员工账号token
    - is_enable: 是否启用
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False, comment='所属用户')
    employee_name = Column(String(255), nullable=False, unique=True, comment='员工账号')
    employee_cn_name = Column(String(255),insert_default='--', nullable=False, unique=True, comment='员工姓名') 
    employee_token = Column(String(255), nullable=False, comment='员工账号token')
    is_enable = Column(Boolean, nullable=False, default=True, comment='是否启用')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return f"<Employee(id={self.id}, user_name='{self.user_name}', employee_name='{self.employee_name}', is_enable={self.is_enable})>"