from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Spark
from diagrams.onprem.database import PostgreSQL, MongoDB, Cassandra
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import Flask
from diagrams.onprem.client import Users, Client
from diagrams.custom import Custom
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.onprem.compute import Server

# Configuration for the diagram
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
}

with Diagram(
    "Real-Time Recommendation System ML Pipeline",
    filename="./recommendation-system/recommendation_system_pipeline",
    show=False,
    direction="LR",
    graph_attr=graph_attr
):
    
    # Data Sources
    with Cluster("Data Sources"):
        users = Users("User Events")
        app_logs = Client("Application\nLogs")
        transactions = SQL("Transaction\nData")
    
    # Data Ingestion Layer
    with Cluster("Data Ingestion"):
        kafka_stream = Kafka("Kafka\nStreaming")
        batch_ingestion = Storage("Batch\nIngestion")
    
    # Orchestration
    with Cluster("Orchestration"):
        airflow = Airflow("Apache Airflow\nWorkflow Scheduler")
    
    # Data Processing Layer
    with Cluster("Data Processing"):
        with Cluster("Stream Processing"):
            spark_streaming = Spark("Spark\nStreaming")
            event_processor = Server("Event\nProcessor")
        
        with Cluster("Batch Processing"):
            spark_batch = Spark("Spark\nBatch Jobs")
            feature_eng = Server("Feature\nEngineering")
    
    # Storage Layer
    with Cluster("Data Storage"):
        data_lake = Storage("Data Lake\n(Raw Data)")
        feature_store = PostgreSQL("Feature\nStore")
        user_profiles = MongoDB("User\nProfiles")
    
    # ML Pipeline
    with Cluster("ML Training Pipeline"):
        model_training = Server("Model\nTraining")
        model_eval = Server("Model\nEvaluation")
        model_registry = Storage("Model\nRegistry")
    
    # Serving Layer
    with Cluster("Real-Time Serving"):
        model_serving = Flask("Model\nServing API")
        cache = Redis("Redis\nCache")
        rec_engine = Server("Recommendation\nEngine")
    
    # Recommendation Storage
    with Cluster("Recommendation Storage"):
        rec_db = Cassandra("Pre-computed\nRecommendations")
        online_store = Redis("Online\nFeature Store")
    
    # Application Layer
    with Cluster("Application"):
        api = Flask("REST API")
        web_app = Client("Web/Mobile\nApp")
    
    # Data Flow - Ingestion
    users >> Edge(label="events") >> kafka_stream
    app_logs >> Edge(label="logs") >> kafka_stream
    transactions >> Edge(label="batch") >> batch_ingestion
    
    # Stream Processing Flow
    kafka_stream >> Edge(label="stream") >> spark_streaming
    spark_streaming >> event_processor
    event_processor >> Edge(label="real-time") >> user_profiles
    
    # Batch Processing Flow
    batch_ingestion >> Edge(label="schedule") >> airflow
    airflow >> Edge(label="trigger") >> spark_batch
    spark_batch >> feature_eng
    
    # Data Storage Flow
    spark_streaming >> Edge(label="store") >> data_lake
    spark_batch >> data_lake
    feature_eng >> Edge(label="features") >> feature_store
    event_processor >> user_profiles
    
    # ML Training Flow
    airflow >> Edge(label="trigger") >> model_training
    feature_store >> Edge(label="training data") >> model_training
    user_profiles >> model_training
    
    model_training >> model_eval
    model_eval >> Edge(label="validated") >> model_registry
    
    # Serving Flow
    model_registry >> Edge(label="deploy") >> model_serving
    feature_store >> Edge(label="features") >> online_store
    
    online_store >> rec_engine
    model_serving >> rec_engine
    user_profiles >> Edge(label="context") >> rec_engine
    
    # Pre-computation
    airflow >> Edge(label="schedule") >> rec_engine
    rec_engine >> Edge(label="batch recs") >> rec_db
    rec_engine >> Edge(label="hot cache") >> cache
    
    # API Flow
    rec_engine >> api
    rec_db >> api
    cache >> api
    
    api >> web_app
    web_app >> Edge(label="feedback") >> kafka_stream
    
    # Monitoring feedback loop
    web_app >> Edge(label="user actions", style="dashed") >> users