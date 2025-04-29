#!/bin/bash

# 创建数据库
mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS tradefree_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tradefree_ai;

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    input_data JSON,
    output_data JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 任务日志表
CREATE TABLE IF NOT EXISTS task_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_task_id (task_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建用户并授权
CREATE USER IF NOT EXISTS 'tradefree'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON tradefree_ai.* TO 'tradefree'@'localhost';
FLUSH PRIVILEGES;
EOF 