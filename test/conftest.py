import pytest


def pytest_addoption(parser):
    parser.addoption("--container_id",action="store",default="default_value",help="defines a container id to use",)


@pytest.fixture
def container_id(request):
    return request.config.getoption("--container_id")