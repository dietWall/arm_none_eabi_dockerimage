import pytest
import docker

default_tag = "stm32"

def pytest_addoption(parser):
    parser.addoption("--tag",action="store",help="defines a container id to use", default=default_tag)

def get_repo_root() -> str:
    import subprocess    
    git_result = subprocess.run(["git", "rev-parse", "--show-toplevel"],capture_output=True)
    repo_root = git_result.stdout.strip().decode("utf-8")
    return repo_root

def run_container(img):
    from docker.types import Mount
    client = docker.from_env()
    repo_mount = Mount(target=f"/home/developer/code", source=get_repo_root(), type='bind')
    result = client.containers.run(image=default_tag, 
                                   detach=True, stdout=True, stdin_open=True, 
                                   mounts=[repo_mount],
                                   remove=True)
    print(f"Started container with id: {result.id}")
    return result

@pytest.fixture(scope="module")
def container(request):
    img = request.config.getoption("--tag")
    container = run_container(img=img)
    yield container

    container.stop()