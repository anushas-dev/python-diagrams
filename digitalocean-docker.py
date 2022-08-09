from diagrams import Diagram
from diagrams.digitalocean.compute import Docker, Containers, K8SCluster, K8SNode, K8SNodePool
from diagrams.digitalocean.network import Vpc

with Diagram("mycloudapp", filename="available_compute", outformat="svg"):
    do_compute = Docker("OnPrem Docker") >> [Containers("Front-End"), Containers("Back-End")]
    live_c = [K8SNode("Function App"),K8SNode("Cronjob"),K8SNode("Batch Processing"),K8SNode("File Delivery System")]
    do_compute >> K8SCluster("MyCloudApp-k8s") << [K8SNodePool("Control Pool, 16 vCPU"), K8SNodePool("Worker Pool, 64 vCPU")] >> Vpc("VPC") << live_c