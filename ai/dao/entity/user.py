from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE `user` (
#   `id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `username` varchar(255) NOT NULL,
#   `user_cn_name` varchar(255) NOT NULL,
#   `password` varchar(255) NOT NULL,
#   `company` varchar(255) DEFAULT NULL,
#   `user_group` varchar(500) DEFAULT NULL,
#   `product_type` varchar(255) DEFAULT NULL,
#   `user_score` int(16) NOT NULL DEFAULT '1',
#   `avatar` varchar(500) DEFAULT NULL,
#   `is_enable` tinyint(4) NOT NULL DEFAULT '1',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#   `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `user_unique` (`username`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class User(Base):
    """用户模型
    
    属性说明：
    - username: 用户名
    - user_cn_name: 用户中文名
    - password: 密码
    - company: 公司
    - user_group: 用户组
    - product_type: 产品类型
    - user_score: 用户积分
    - avatar: 头像
    - is_enable: 是否启用
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True, comment='用户名')
    user_cn_name = Column(String(255), nullable=False, comment='用户中文名')
    password = Column(String(255), nullable=False, comment='密码')
    company = Column(String(255), nullable=True, comment='公司')
    user_group = Column(String(500), nullable=True, comment='用户组')
    product_type = Column(String(255), nullable=True, comment='产品类型')
    user_score = Column(Integer, nullable=False, default=1, comment='用户积分')
    avatar = Column(String(500), nullable=True, comment='头像')
    is_enable = Column(Boolean, nullable=False, default=True, comment='是否启用')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"username='{self.username}', "
            f"user_cn_name='{self.user_cn_name}', "
            f"user_group='{self.user_group}', "
            f"is_enable={self.is_enable})>"
        )