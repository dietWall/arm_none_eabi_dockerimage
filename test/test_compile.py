import pytest

import docker

def test_compile(container_id, source_path="/home/developer/code/test/lib"):
    print("")   #newline for readability
    print(f"testing in container {container_id}")
    client = docker.from_env()
    container = client.containers.get(container_id)
    #make sure build directory is clean
    container.exec_run(cmd="rm -rf build/*")
    #make sure build directory exists
    container.exec_run(cmd="mkdir -p build")

    compile_result = container.exec_run(cmd=f"cmake -S {source_path} -B build -DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake")
    assert compile_result.exit_code == 0, f"cmake failed with output: {compile_result.output.decode('utf-8')}"
    print("cmake succeeded")
    make_result = container.exec_run(cmd="make -C build")
    assert make_result.exit_code == 0, f"make failed with output: {make_result.output.decode('utf-8')}"
    print("make succeeded")
    print("Test passed")