
from prefect import flow, task

@task
def say_hello(name: str):
    print(f"Hello, {name}!")
    return name

@flow
def hello_world_flow(name: str = "World"):
    say_hello(name)
    print("Workflow completed!")

if __name__ == "__main__":
    hello_world_flow("MLOps")