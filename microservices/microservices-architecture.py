from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DDB

with Diagram("Microservices Architecture", show=False,
             filename="./microservices/microservices-architecture", direction="LR"):
    # This is the entry point for users
    api_gateway = APIGateway("API Gateway")

    # This is a group of services
    with Cluster("Services"):
        user_service = Lambda("User Service")
        order_service = Lambda("Order Service")

    # This is a group of databases
    with Cluster("Databases"):
        user_db = DDB("User DB")
        order_db = DDB("Order DB")

    # This is how you connect them
    api_gateway >> user_service >> user_db
    api_gateway >> order_service >> order_db