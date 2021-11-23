#!/bin/bash
DATE=$(date +%Y%m%d%H%M)
BACKUP_DIR=/home/lab21/project/db_backup/
mysqldump --login-path=local Covid > $BACKUP_DIR"backup_"$DATE.sql

# 3일이 지난 백업 파일삭제
find $BACKUP_DIR -ctime +3 -exec rm -f {} \;

echo "DB Backup --- $(date +%Y:%m:%d) $(date +%H:%M:%s)"
