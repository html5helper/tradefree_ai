from sqlalchemy import create_engine
from ai.config.celeryconfig import MYSQL_CONFIG

workflow_mysql_url = (
    f"mysql+pymysql://{MYSQL_CONFIG['workflow_db']['user']}:{MYSQL_CONFIG['workflow_db']['password']}"
    f"@{MYSQL_CONFIG['workflow_db']['host']}:{MYSQL_CONFIG['workflow_db']['port']}/{MYSQL_CONFIG['workflow_db']['database']}"
    f"?charset={MYSQL_CONFIG['workflow_db']['charset']}"
)

manager_mysql_url = (
    f"mysql+pymysql://{MYSQL_CONFIG['manager_db']['user']}:{MYSQL_CONFIG['manager_db']['password']}"
    f"@{MYSQL_CONFIG['manager_db']['host']}:{MYSQL_CONFIG['manager_db']['port']}/{MYSQL_CONFIG['manager_db']['database']}"
    f"?charset={MYSQL_CONFIG['manager_db']['charset']}"
)

workflow_engine = create_engine(
    workflow_mysql_url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    pool_timeout=30,
    echo=False
)

manager_engine = create_engine(
    manager_mysql_url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    pool_timeout=30,
    echo=False
) 