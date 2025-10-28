"""
AWS Web Application Architecture diagram using Diagrams.

Outputs: aws-web-app-architecture.png in the repository root.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, PublicSubnet, PrivateSubnet, InternetGateway, NATGateway, Route53
from diagrams.aws.network import ALB, CloudFront
from diagrams.aws.security import WAF, IAM
from diagrams.aws.compute import ECS, EC2AutoScaling
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS  # optional
from diagrams.aws.compute import ECR      # optional

def create_architecture() -> None:
    """
    Render an AWS web application reference architecture.
    """
    with Diagram(
        "AWS Web Application Architecture",
        filename="./aws-web-app/aws-web-app-architecture",
        outformat="png",
        show=False,
        direction="LR",
    ):
        users = Route53("Route 53")
        cdn = CloudFront("CloudFront")
        waf = WAF("WAF")
        alb = ALB("ALB")

        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")
            nat = NATGateway("NAT")

            with Cluster("Public Subnets"):
                pub_a = PublicSubnet("Public A")
                pub_b = PublicSubnet("Public B")

            with Cluster("Private Subnets"):
                priv_a = PrivateSubnet("Private A")
                priv_b = PrivateSubnet("Private B")

            # App tier (choose one: ECS or EC2 AutoScaling)
            app = ECS("App Service")
            db = RDS("RDS (Multi-AZ)")
            cache = ElastiCache("Redis")
            assets = S3("Static Assets")
            metrics = Cloudwatch("CloudWatch")

            # Optional CI/CD artifacts
            ecr = ECR("ECR")

            # Traffic flow
            users >> cdn >> waf >> alb
            alb >> [app]
            app >> [db, cache]
            app >> assets

            # Observability
            [app, db] >> metrics

            # Routing hints (not full wiring, just for visual)
            igw - Edge(style="dashed") - [pub_a, pub_b]
            nat - Edge(style="dashed") - [priv_a, priv_b]

if __name__ == "__main__":
    create_architecture()
