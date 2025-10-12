from diagrams import Diagram
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Redshift, Glue
from diagrams.aws.compute import Lambda

"""
数据仓库处理流程架构图（DWGU）
展示从数据采集到分析的完整流程：S3存储原始数据，Glue进行ETL处理，
Redshift作为数据仓库存储，Lambda触发自动化任务。
"""

with Diagram(
    "DWGU Data Warehouse Flow",  # 图表名称
    show=True,                   # 生成后自动显示
    filename="dwgu-diagram",     # 输出文件名（不含扩展名）
    outformat="png"              # 输出格式
):
    # 定义节点
    raw_data = S3("原始数据存储")
    etl_job = Glue("ETL 数据处理")
    data_warehouse = Redshift("数据仓库")
    trigger = Lambda("自动化触发任务")

    # 定义节点关系
    trigger >> raw_data >> etl_job >> data_warehouse