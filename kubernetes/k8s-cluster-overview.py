from diagrams import Diagram, Edge, Cluster
from diagrams.azure.network import ApplicationGateway, LoadBalancers
from diagrams.azure.compute import AKS, KubernetesServices, ContainerRegistries
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.monitor import Monitor

with Diagram("Kubernetes Cluster Overview (Azure)", 
             filename="./kubernetes/k8s-cluster-overview-azure", show=False, direction="LR"):
    # External traffic
    app_gw = ApplicationGateway("App Gateway / ALB")

    # Kubernetes cluster (AKS)
    with Cluster("AKS Cluster"):
        aks = AKS("AKS")
        pod1 = KubernetesServices("Pod: app-1")
        pod2 = KubernetesServices("Pod: app-2")

    # Supporting services
    acr = ContainerRegistries("ACR")
    blob = StorageAccounts("Blob Storage (PV)")
    db = DatabaseForPostgresqlServers("Azure DB for PostgreSQL")
    monitor = Monitor("Azure Monitor")

    # Interactions
    app_gw >> Edge(label="Ingress") >> aks
    aks >> Edge(label="Schedules/Routes") >> pod1
    aks >> Edge(label="Schedules/Routes") >> pod2

    pod1 >> Edge(label="Store PVC") >> blob
    pod2 >> Edge(label="Store PVC") >> blob

    pod1 >> Edge(label="Query") >> db
    pod2 >> Edge(label="Query") >> db

    acr >> Edge(label="Images") >> aks

    # Monitoring
    aks >> monitor
    db >> monitor
    blob >> monitor
