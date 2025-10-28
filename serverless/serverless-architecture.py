from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.management import Cloudwatch


with Diagram("Serverless Architecture", show=True, filename="./serverless/serverless-architecture", outformat="png"):
    # Public API + Auth
    api_gateway = APIGateway("API Gateway")
    user_auth = Cognito("Cognito User Pool")

    # Core compute and storage
    lambda_function = Lambda("API Lambda")
    dynamodb = Dynamodb("DynamoDB")
    s3 = S3("S3")

    # Async messaging and worker
    sns = SNS("SNS Topic")
    sqs = SQS("SQS Queue")
    worker = Lambda("Worker Lambda")

    # Monitoring
    cw = Cloudwatch("CloudWatch")

    # Group the serverless backend for clarity
    with Cluster("Serverless Backend"):
        lambda_function >> dynamodb
        lambda_function >> s3
        lambda_function >> sns

    # Async delivery to worker via SQS subscription
    sns >> sqs
    sqs >> worker

    # API and auth flow
    api_gateway >> user_auth
    api_gateway >> lambda_function

    # Monitoring connections (informational)
    lambda_function >> cw
    worker >> cw
    dynamodb >> cw
