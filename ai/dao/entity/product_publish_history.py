from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE celery_dev.`product_publish_history` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `employee_id` bigint(20) NOT NULL COMMENT '员工编号',
#   `employee_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `dest_platform` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `product_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `shop_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `last_task_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `last_task_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '-',
#   `last_task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
#   `last_task_status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `product` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#   `actionflow` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#   `updated_at` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `trace_id` (`trace_id`),
#   KEY `idx_trace_id` (`trace_id`),
#   KEY `idx_employee_id` (`employee_id`),
#   KEY `idx_platform` (`dest_platform`),
#   KEY `idx_product_status` (`status`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class ProductPublishHistory(Base):
    """产品发布历史模型
    
    发品状态说明：
    - PENDING: 等待执行
    - STARTED: 已开始执行
    - SUCCESS: 执行成功
    - FAILURE: 执行失败
    - RETRY: 重试中
    - REVOKED: 已撤销
    """
    __tablename__ = "product_publish_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    employee_name = Column(String(255), nullable=False)
    dest_platform = Column(String(255), nullable=False)
    product_type = Column(String(255), nullable=False)
    shop_name = Column(String(255), nullable=False)
    status = Column(String(50))
    trace_id = Column(String(255), index=True)
    last_task_id = Column(String(255), nullable=False)
    last_task_type = Column(String(255), nullable=False)
    last_task_name = Column(String(255), nullable=False)
    last_task_status = Column(String(50))
    product = Column(Text)
    action_flow_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<ProductPublishHistory(id={self.id}, employee_name='{self.employee_name}', dest_platform='{self.dest_platform}', status='{self.status}')>"

    def to_dict(self):
        """Convert the object to a dictionary for API responses"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'dest_platform': self.dest_platform,
            'product_type': self.product_type,
            'shop_name': self.shop_name,
            'status': self.status,
            'trace_id': self.trace_id,
            'last_task_id': self.last_task_id,
            'last_task_type': self.last_task_type,
            'last_task_name': self.last_task_name,
            'last_task_status': self.last_task_status,
            'product': self.product,
            'action_flow_id': self.action_flow_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }