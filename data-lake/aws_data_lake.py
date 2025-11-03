"""
Diagram for a basic Data Lake Architecture on AWS.
"""
from diagrams import Cluster, Diagram
from diagrams.aws.analytics import Glue, Redshift, Quicksight
from diagrams.aws.storage import S3
from diagrams.aws.database import DatabaseMigrationService as DMS

with Diagram("AWS Data Lake Architecture", 
             filename="./data-lake/aws_data_lake",
             show=False, direction="LR"):
    
    source = DMS("Data Source (e.g., DB)")

    with Cluster("Data Lake"):
        s3_raw = S3("Raw Zone (S3)")
        
        with Cluster("ETL & Warehouse"):
            glue_etl = Glue("ETL (Glue)")
            redshift_dw = Redshift("Warehouse (Redshift)")
        
        s3_raw >> glue_etl >> redshift_dw

    bi_tool = Quicksight("BI (QuickSight)")
    
    source >> s3_raw
    redshift_dw >> bi_tool
