from diagrams import Diagram
from diagrams.programming.language import Go
from diagrams.programming.flowchart import Action, Decision, Delay, InputOutput

with Diagram("MyGoApp", show=True, filename="my-go-app", outformat="pdf"):
    net = Go("MyGoApp") >> Action("Fetch User Data")
    decide = Decision("Is this new user?")
    action_y = Action("Yes")
    action_n = Action("No")
    net >> decide >> action_y >> InputOutput("Proceed to Login")
    net >> decide >> action_n >> InputOutput("Register/Sign Up")
