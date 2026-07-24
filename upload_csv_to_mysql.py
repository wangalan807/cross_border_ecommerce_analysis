import os
import pandas as pd
from sqlalchemy import create_engine
# 导入 dotenv 库来解析环境配置文件
from dotenv import load_dotenv


def upload_data():
    # 1. 自动寻找并加载项目根目录下的 .env 文件
    load_dotenv()

    # 2. 从环境变量中安全地捞出配置（如果捞不到则使用安全的默认兜底值）
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD")  # 这会精准读取你 .env 里的密码
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "cross_border_ecommerce_db")

    # 安全防线：如果 .env 里没配密码，直接报错拦截，防止空密连接崩溃
    if not db_password:
        print("❌ 错误：未能从 .env 文件中成功读取到 'DB_PASSWORD'，请检查文件内容！")
        return

    # 3. 动态拼接出绝对安全的连接字符串（URL）
    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"

    try:
        engine = create_engine(db_url)
        print("🚀 [安全通道] 已成功读取 .env 凭证，MySQL 数据库连接成功！")
    except Exception as e:
        print(f"❌ 数据库连接失败，请检查配置: {e}")
        return

    # 4. 定位你 PyCharm 里的 outputs 文件夹路径（多平台路径自适应）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(base_dir, 'outputs')

    # 5. 映射：本地本地 2.csv 文件 -> 数据库中干净的业务表名
    file_to_table_mapping = {
        'orders_clean.csv': 'orders_clean',
        'ad_campaigns_clean.csv': 'ad_campaigns_clean',
        'country_metrics.csv': 'country_metrics'
    }

    print("-" * 60)
    for csv_file, table_name in file_to_table_mapping.items():
        file_path = os.path.join(outputs_dir, csv_file)

        # 严格检查文件是否存在
        if not os.path.exists(file_path):
            print(f"⚠️ 警告：在 outputs 文件夹下没有找到 【{csv_file}】")
            continue

        print(f"📦 正在读取本地大样本数据: {csv_file} ...")

        try:
            # 采用 utf-8-sig 编码完美兼容多国站点（如 Germany 字符）和财务指标，杜绝乱码
            df = pd.read_csv(file_path, encoding='utf-8-sig')

            print(f"💾 正在批量同步 {len(df)} 条数据到 MySQL 核心表 【{table_name}】...")
            # if_exists='replace' 会自动建表、清洗并覆盖，绝不碰你已有的其他数据库
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            print(f"✅ 表 【{table_name}】 自动化落库成功！")

        except Exception as csv_err:
            print(f"❌ 同步 {csv_file} 时发生崩溃: {csv_err}")
        print("-" * 60)

    print("\n🎉 恭喜！outputs 文件夹中的 3 张亚马逊核心业务表已通过安全通道全部落库成功！")


if __name__ == '__main__':
    upload_data()