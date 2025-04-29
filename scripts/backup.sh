#!/bin/bash

# 设置备份目录
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
echo "备份数据库..."
mysqldump -u tradefree -ppassword tradefree_ai > $BACKUP_DIR/tradefree_ai_$DATE.sql

# 备份日志
echo "备份日志..."
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# 备份配置文件
echo "备份配置文件..."
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/

# 保留最近7天的备份
find $BACKUP_DIR -type f -mtime +7 -delete

echo "备份完成！"
echo "备份文件保存在: $BACKUP_DIR" 