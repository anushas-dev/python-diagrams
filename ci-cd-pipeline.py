"""
CI/CD pipeline diagram using the Diagrams library.

This module generates a CI/CD pipeline diagram and saves it to
'ci-cd-pipeline.png' in the repository root.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.devtools import Codebuild, Codepipeline, Codecommit, Codeartifact, Codedeploy
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3
from diagrams.aws.compute import ECS, ECR
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import APIGateway
from diagrams.aws.general import Users


def create_ci_cd_pipeline() -> None:
    """
    Create and render a CI/CD pipeline diagram using the Diagrams library.

    Outputs:
        ci-cd-pipeline.png in the repository root.
    """
    with Diagram(
        "CI/CD Pipeline",
        filename="ci-cd-pipeline",
        outformat="png",
        show=False,
        direction="LR",
    ):
        # Define nodes
        developers = Users("Developers")
        code_repo = Codecommit("Code Repository")
        build = Codebuild("Build")
        test = Codebuild("Test")
        package = Codeartifact("Package")
        deploy_dev = Codedeploy("Deploy to Dev")
        deploy_prod = Codedeploy("Deploy to Prod")
        container_registry = ECR("Container Registry")
        dev_env = ECS("Dev Environment")
        prod_env = ECS("Prod Environment")
        monitoring = Cloudwatch("Monitoring")
        artifacts = S3("Artifact Store")
        iam = IAM("IAM")
        cdn = CloudFront("CDN")
        api_gateway = APIGateway("API Gateway")

        # Define clusters
        with Cluster("Source"):
            _ = [developers, code_repo]

        with Cluster("CI/CD Pipeline"):
            pipeline = Codepipeline("CI/CD Pipeline")
            _ = [build, test, package, deploy_dev, deploy_prod]

        with Cluster("Infrastructure"):
            _ = [container_registry, artifacts, iam]

        with Cluster("Environments"):
            _ = [dev_env, prod_env]

        # Define connections
        developers >> code_repo
        code_repo >> Edge(label="On push to main") >> pipeline
        pipeline >> build >> test >> package
        package >> Edge(label="On success") >> deploy_dev
        package >> Edge(label="Store artifacts") >> artifacts
        deploy_dev >> dev_env
        deploy_dev >> Edge(label="Manual approval") >> deploy_prod
        deploy_prod >> prod_env
        container_registry << build
        container_registry >> [dev_env, prod_env]
        iam - Edge(style="dashed") - [build, test, package, deploy_dev, deploy_prod]
        [dev_env, prod_env] >> monitoring
        api_gateway >> [dev_env, prod_env]
        cdn >> api_gateway
        users = Users("End Users")
        users >> cdn
        users >> api_gateway


if __name__ == "__main__":
    create_ci_cd_pipeline()
