from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataFirehose, AmazonOpensearchService, Athena
from diagrams.aws.storage import S3
from diagrams.aws.analytics import AmazonOpensearchService as OpenSearch
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm
from diagrams.aws.integration import SNS
from diagrams.aws.database import DDB
from diagrams.aws.analytics import Athena


with Diagram("Logging & Monitoring Stack", show=True, 
             filename="./logging-monitoring/logging-monitoring-stack", direction="LR"):
    # Ingestion layer
    with Cluster("Ingestion"):
        api_gateway = APIGateway("API Gateway")
        ingest_lambda = Lambda("Ingest Lambda\n(validation/enrich)")
        kinesis = KinesisDataStreams("Kinesis Data Streams")

        api_gateway >> Edge(label="HTTP logs/events") >> ingest_lambda >> kinesis

    # Processing & buffering
    with Cluster("Processing"):
        firehose = KinesisDataFirehose("Kinesis Firehose")
        processor_lambda = Lambda("Processor Lambda\n(aggregation/metrics)")

        kinesis >> Edge(label="stream") >> processor_lambda
        processor_lambda >> Edge(label="to firehose") >> firehose

    # Storage & search
    with Cluster("Storage & Indexing"):
        logs_bucket = S3("S3 Logs Bucket")
        es = OpenSearch("OpenSearch / Elasticsearch")
        metadata_db = DDB("DynamoDB (metadata)")

        firehose >> Edge(label="deliver") >> logs_bucket
        firehose >> Edge(label="index") >> es

    # Analytics
    with Cluster("Analytics"):
        athena = Athena("Athena")
        logs_bucket >> athena

    # Monitoring & Alerts
    with Cluster("Monitoring"):
        cw = Cloudwatch("CloudWatch")
        alarm = CloudwatchAlarm("CW Alarm")
        alerts = SNS("Alert Topic")

        processor_lambda >> cw
        es >> cw
        metadata_db >> cw

        cw >> alarm >> alerts

    # Connect metadata and retention
    processor_lambda >> metadata_db
    logs_bucket >> metadata_db