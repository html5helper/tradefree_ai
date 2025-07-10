from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# CREATE TABLE `product_history` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `trace_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '工作流编号',
#   `employee_id` bigint(20) NOT NULL COMMENT '员工编号',
#   `employee_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '员工名称',
#   `product_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '--' COMMENT '产品类型（业务类目）',
#   `collect_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '采集状态：PENDING-任务已创建，等待执行,STARTED-任务已开始执行,SUCCESS-任务执行成功,FAILURE-任务执行失败',
#   `collect_product` text COLLATE utf8mb4_unicode_ci COMMENT '源商品信息',
#   `generate_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '生成状态：PENDING-任务已创建，等待执行,STARTED-任务已开始执行,SUCCESS-任务执行成功,FAILURE-任务执行失败',
#   `generate_product` text COLLATE utf8mb4_unicode_ci COMMENT '生成商品信息',
#   `publish_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发布状态：PENDING-任务已创建，等待执行,STARTED-任务已开始执行,SUCCESS-任务执行成功,FAILURE-任务执行失败',
#   `publish_product` text COLLATE utf8mb4_unicode_ci COMMENT '发布商品信息',
#   `template_id` bigint(20) DEFAULT NULL COMMENT '发品模板编号',
#   `src_platform` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '来源平台',
#   `dest_platform` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发品平台',
#   `shop_id` bigint(20) NOT NULL COMMENT '店铺ID',
#   `dest_shop_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发品店铺名称',
#   `last_task_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '最后执行的任务task_id',
#   `last_task_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '-' COMMENT '最后执行的任务类型',
#   `last_task_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '最后执行的任务名',
#   `last_task_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后执行的任务状态',
#   `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#   `updated_at` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `trace_id` (`trace_id`),
#   KEY `idx_trace_id` (`trace_id`),
#   KEY `idx_employee_id` (`employee_id`),
#   KEY `idx_platform` (`dest_platform`),
#   KEY `idx_product_type` (`product_type`),
#   KEY `idx_collect_status` (`collect_status`),
#   KEY `idx_generate_status` (`generate_status`),
#   KEY `idx_publish_status` (`publish_status`)
# ) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

class ProductHistory(Base):
    """产品历史模型
    
    发品状态说明：
    - PENDING: 等待执行
    - STARTED: 已开始执行
    - SUCCESS: 执行成功
    - FAILURE: 执行失败
    """
    __tablename__ = "product_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String(255), index=True)
    employee_id = Column(Integer, nullable=False)
    employee_name = Column(String(255), nullable=False)
    product_type = Column(String(255), nullable=False)
    collect_status = Column(String(50))
    collect_product = Column(Text)
    generate_status = Column(String(50))
    generate_product = Column(Text)
    publish_status = Column(String(50))
    publish_product = Column(Text)
    src_platform = Column(String(255), nullable=False)
    dest_platform = Column(String(255), nullable=False)
    shop_id = Column(Integer, nullable=False)
    dest_shop_name = Column(String(255), nullable=False)
    last_task_id = Column(String(255), nullable=False)
    last_task_type = Column(String(255), nullable=False)
    last_task_name = Column(String(255), nullable=False)
    last_task_status = Column(String(50))
    template_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<ProductHistory(id={self.id}, employee_id='{self.employee_id}', dest_platform='{self.dest_platform}', dest_shop_name='{self.dest_shop_name}')>"

    def to_dict(self):
        """Convert the object to a dictionary for API responses"""
        return {
            'id': self.id,
            'trace_id': self.trace_id,
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'product_type': self.product_type,
            'collect_status': self.collect_status,
            'collect_product': self.collect_product,
            'generate_status': self.generate_status,
            'generate_product': self.generate_product,
            'publish_status': self.publish_status,
            'publish_product': self.publish_product,
            'src_platform': self.src_platform,
            'dest_platform': self.dest_platform,
            'shop_id': self.shop_id,
            'dest_shop_name': self.dest_shop_name,
            'last_task_id': self.last_task_id,
            'last_task_type': self.last_task_type,
            'last_task_name': self.last_task_name,
            'last_task_status': self.last_task_status,
            'template_id': self.template_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }