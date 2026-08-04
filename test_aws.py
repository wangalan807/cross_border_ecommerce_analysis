import io
import os
import boto3
import pandas as pd
from dotenv import load_dotenv

# 1. 加载 .env 文件中的环境变量
load_dotenv()


def test_s3_connection():
    print("🚀 开始测试 AWS S3 云端连接...")

    # 获取密钥
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    # 2. 初始化 AWS S3 客户端
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )

    bucket_name = "wangalan-studio-data-2026"
    file_key = "cross_border_orders_100.xlsx"

    try:
        # 3. 从 AWS S3 拉取文件内容
        print(f"📦 正在从存储桶 [{bucket_name}] 读取 [{file_key}]...")
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # 4. 使用 io.BytesIO 将二进制流转化为 Pandas 可读对象
        file_bytes = response['Body'].read()
        df = pd.read_excel(io.BytesIO(file_bytes))

        print("\n✅ 连接成功！数据获取完成。")
        print("=" * 50)
        print("📊 跨境电商测试数据预览（前 5 行）：")
        print(df.head())
        print("=" * 50)
        print(f"📈 表格总行数: {len(df)} 行, 总列数: {len(df.columns)} 列")

        # 5. 模拟 AI 助手的数据分析/处理逻辑（筛选出销售额最高的订单）
        top_sales_df = df[df['Revenue'] > 300]

        # 6. 将处理后的数据转换为 Excel 二进制流
        output_buffer = io.BytesIO()
        with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
            top_sales_df.to_excel(writer, index=False, sheet_name='高销分析')

        output_bytes = output_buffer.getvalue()

        # 7. 将分析结果回传写至 AWS S3
        output_file_key = "reports/top_sales_analysis.xlsx"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_file_key,
            Body=output_bytes
        )

        print(f"\n🎉 成功将 AI 分析报告上传写回至 AWS S3: [{output_file_key}]")

    except Exception as e:
        print(f"\n❌ 测试失败，错误信息: {e}")


if __name__ == "__main__":
    test_s3_connection()