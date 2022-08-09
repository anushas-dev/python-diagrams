# python-diagrams
### Diagram as a Code 
Refer official [documentation](https://diagrams.mingrammer.com/)


Commonly noticed error if you didn't have graphviz properly installed:
`graphviz.backend.execute.ExecutableNotFound: failed to execute WindowsPath('dot'), make sure the Graphviz executables are on your systems' PATH`

Install graphviz from [here](https://graphviz.gitlab.io/download/)
Add path to ~/graphviz/bin to ENV PATH

## Examples in this repo
- k8s 2 Replicas : Typcial app deployment exposed with svc,ingress with 2 replicas (./myapp.png)
- my go app: Typcial flowchart for checking new user (./my-go-app.pdf)
- digital ocean compute: on-prem docker communicating to cloudapp as common link that has other services hosted on kubernetes (./digitalocean_compute.svg)