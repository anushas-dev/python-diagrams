"""
Diagram for a Multi-Region Disaster Recovery (DR) Architecture on AWS.
"""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.network import Route53
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3

with Diagram("AWS Multi-Region DR Architecture", 
             filename="./disaster-recovery/aws_disaster_recovery",
             show=False):

    dns = Route53("DNS (Route 53)")

    with Cluster("Region 1 (Primary - us-east-1)"):
        primary_ec2 = EC2("App Server")
        primary_db = RDS("Primary DB")
        primary_s3 = S3("Primary S3 Bucket")

    with Cluster("Region 2 (Standby - us-west-2)"):
        standby_ec2 = EC2("Standby Server")
        standby_db = RDS("Read Replica DB")
        standby_s3 = S3("Replicated S3 Bucket")

    # Traffic Flow
    dns >> primary_ec2
    primary_ec2 >> primary_db
    primary_ec2 >> primary_s3

    # Replication Links (Data Sync)
    primary_db >> Edge(label="Replication", style="dotted") >> standby_db
    primary_s3 >> Edge(label="CRR", style="dotted") >> standby_s3

    # Standby Flow (if primary fails, DNS points here)
    dns >> Edge(label="Failover", style="dashed", color="red") >> standby_ec2
    standby_ec2 >> standby_db
    standby_ec2 >> standby_s3
