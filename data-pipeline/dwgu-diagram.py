from diagrams import Diagram, Edge
from diagrams.aws.storage import S3  # AWS S3: Object storage for raw/processed data
from diagrams.aws.analytics import (
    Glue,         # ETL Step 1: Crawl raw data to infer schema
    Redshift      # ETL Step 2: Load processed data to data warehouse
)
from diagrams.aws.compute import Lambda  # Trigger ETL pipeline automatically

"""
DWGU Data Warehouse ETL Architecture Diagram
============================================
Purpose: Visualizes the end-to-end ETL (Extract-Transform-Load) workflow for a data warehouse,
         suitable for small-to-medium business analytics scenarios.

Legends (Component Descriptions):
---------------------------------
1. Lambda: Serverless function that triggers ETL when data is uploaded to S3
2. S3:
   - "Raw Data Bucket": Stores unprocessed source data (e.g., CSV/JSON logs)
   - "Processed Data Bucket": Temporarily stores cleaned data
3. Glue: AWS Glue service (used here for crawling raw data, inferring schemas, and transforming data)
4. Redshift: Columnar data warehouse for analytical queries
"""

with Diagram(
    "DWGU Data Warehouse ETL Flow",
    show=True,
    filename="dwgu-diagram",
    outformat="png",
    direction="LR"
):
    etl_trigger = Lambda("ETL Trigger\n(On S3 Upload)")
    raw_data_bucket = S3("Raw Data Bucket\n(Source: CSV/JSON)")
    processed_data_bucket = S3("Processed Data Bucket\n(Cleaned Data)")
    glue_crawler = Glue("Glue Crawler\n(Infer Schema)")  # Implements crawling functionality using the Glue component
    glue_job = Glue("Glue Job\n(Transform Data)")  # Different instances of the same component; distinguished by labels
    data_warehouse = Redshift("Redshift\n(Data Warehouse)")

    # Maintains the original ETL workflow
    etl_trigger >> Edge(label="1. Trigger ETL") >> raw_data_bucket
    raw_data_bucket >> Edge(label="2. Crawl Raw Data") >> glue_crawler
    glue_crawler >> Edge(label="3. Update Data Catalog") >> glue_job
    glue_job >> Edge(label="4. Transform & Save") >> processed_data_bucket
    processed_data_bucket >> Edge(label="5. Load to DW") >> data_warehouse