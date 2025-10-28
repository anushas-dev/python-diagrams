from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.ml import Sagemaker, Bedrock
from diagrams.aws.security import Cognito, SecretsManager
from diagrams.aws.integration import Eventbridge, SQS, SNS, StepFunctions
from diagrams.aws.analytics import KinesisDataAnalytics
from diagrams.onprem.client import Users

# Configuration for the diagram
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
}

with Diagram(
    "AWS GenAI LLM Chatbot Architecture",
    filename="./chatbot/aws_genai_chatbot_architecture",
    show=False,
    direction="TB",
    graph_attr=graph_attr
):
    
    # Users
    user = Users("Users")
    
    with Cluster("Frontend Layer"):
        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")
        webapp = S3("Web App\n(S3 Static Site)")
    
    with Cluster("API Layer"):
        apigw = APIGateway("API Gateway")
        websocket_apigw = APIGateway("WebSocket API")
    
    with Cluster("Authentication"):
        auth = Cognito("Cognito\nUser Pool")
    
    with Cluster("Application Logic"):
        with Cluster("Lambda Functions"):
            api_lambda = Lambda("API Handler")
            websocket_lambda = Lambda("WebSocket\nHandler")
            chat_lambda = Lambda("Chat Processing")
            orchestrator = Lambda("Orchestrator")
    
    with Cluster("AI/ML Services"):
        bedrock = Bedrock("Amazon Bedrock\n(LLM Models)")
        sagemaker = Sagemaker("SageMaker\n(Custom Models)")
    
    with Cluster("Data Storage"):
        dynamodb = Dynamodb("DynamoDB\n(Chat History)")
        s3_data = S3("S3\n(Documents)")
        secrets = SecretsManager("Secrets Manager")
    
    with Cluster("Message Processing"):
        queue = SQS("SQS Queue")
        eventbus = Eventbridge("EventBridge")
        step_func = StepFunctions("Step Functions\n(Workflow)")
    
    with Cluster("Monitoring & Analytics"):
        analytics = KinesisDataAnalytics("Kinesis\nAnalytics")
        notifications = SNS("SNS\nNotifications")
    
    # Flow connections
    user >> Edge(label="HTTPS") >> dns >> cdn >> webapp
    
    webapp >> Edge(label="REST API") >> apigw
    webapp >> Edge(label="WebSocket") >> websocket_apigw
    
    apigw >> auth
    websocket_apigw >> auth
    
    auth >> api_lambda
    auth >> websocket_lambda
    
    api_lambda >> chat_lambda
    websocket_lambda >> chat_lambda
    
    chat_lambda >> orchestrator
    orchestrator >> queue
    queue >> step_func
    
    step_func >> bedrock
    step_func >> sagemaker
    step_func >> s3_data
    
    chat_lambda >> dynamodb
    orchestrator >> dynamodb
    
    bedrock >> Edge(label="Response") >> orchestrator
    sagemaker >> Edge(label="Response") >> orchestrator
    
    orchestrator >> Edge(label="Store") >> dynamodb
    s3_data >> Edge(label="RAG Context") >> orchestrator
    
    secrets >> api_lambda
    secrets >> chat_lambda
    
    eventbus >> analytics
    chat_lambda >> eventbus
    
    analytics >> notifications