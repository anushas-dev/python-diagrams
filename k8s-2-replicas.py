from diagrams import Diagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

with Diagram("MyApp", show=True, filename="myapp", outformat="png"):
    net = Ingress("myapp.com:80,443") >> Service("myapp-svc:80")
    net >> [Pod("myapp-1"),
            Pod("myapp-2")] << ReplicaSet("rs") << Deployment("myapp") << HPA("hpa")