import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from diagrams import Diagram, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis, KinesisDataStreams, KinesisDataFirehose
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift, DynamodbTable
from diagrams.aws.ml import SagemakerModel
from diagrams.generic.database import SQL
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Users

"""
Real-time Streaming Data Pipeline Architecture
==============================================
Purpose: Modern streaming data pipeline for real-time analytics and ML inference,
         handling high-volume event data with both batch and stream processing.

Components:
-----------
1. Users: Data sources generating events (web apps, mobile apps, IoT devices)
2. Kinesis Data Streams: Real-time data ingestion and streaming
3. Lambda: Stream processing for real-time transformations
4. Kinesis Data Firehose: Reliable data delivery to storage
5. S3: Data lake for raw and processed data storage
6. Spark: Batch processing for complex analytics
7. Redshift: Data warehouse for business intelligence
8. DynamoDB: Real-time feature store for ML models
9. SageMaker: ML model serving for real-time predictions
"""

with Diagram(
    "Real-time Streaming Data Pipeline",
    show=False,
    filename="./data-pipeline/data-pipeline-streaming",
    outformat="png",
    direction="TB"
):
    # Data Sources
    data_sources = Users("Event Sources\n(Web/Mobile/IoT)")
    
    # Streaming Layer
    kinesis_streams = KinesisDataStreams("Kinesis Streams\n(Real-time Ingestion)")
    
    # Real-time Processing
    stream_processor = Lambda("Stream Processor\n(Real-time Transform)")
    
    # Data Delivery
    firehose = KinesisDataFirehose("Kinesis Firehose\n(Data Delivery)")
    
    # Storage Layer
    data_lake = S3("Data Lake\n(Raw & Processed)")
    feature_store = DynamodbTable("Feature Store\n(Real-time Features)")
    
    # Batch Processing
    batch_processor = Spark("Spark Jobs\n(Batch Analytics)")
    
    # Analytics & ML
    data_warehouse = Redshift("Redshift\n(Data Warehouse)")
    ml_model = SagemakerModel("ML Models\n(Real-time Inference)")
    
    # Data Flow
    data_sources >> Edge(label="events") >> kinesis_streams
    kinesis_streams >> Edge(label="stream") >> stream_processor
    stream_processor >> Edge(label="features") >> feature_store
    stream_processor >> Edge(label="processed") >> firehose
    firehose >> Edge(label="store") >> data_lake
    data_lake >> Edge(label="batch") >> batch_processor
    batch_processor >> Edge(label="aggregated") >> data_warehouse
    feature_store >> Edge(label="features") >> ml_model