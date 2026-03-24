import pytest

import docker

def test_compile(container_id, source_path="/home/developer/code/test/lib"):
    print("")   #newline for readability
    print(f"testing in container {container_id}, source path: {source_path}")
    
    client = docker.from_env()
    container = client.containers.get(container_id)
    dir_contents = container.exec_run(cmd="ls -la", workdir=source_path)
    print(f"Contents of {source_path} in container:")
    print(dir_contents.output.decode('utf-8'))
    
    copied_source_path = f"/home/developer/workspace"
    build_dir = "/home/developer/build"
    mkdir_result = container.exec_run(cmd=f"mkdir -p {copied_source_path}")
    
    dir_contents = container.exec_run(cmd="ls -la", workdir=copied_source_path)
    print(f"Contents of {copied_source_path} in container:")
    print(dir_contents.output.decode('utf-8'))

    # github actions run with a different uid, we make a copy with changed ownership
    cp_result = container.exec_run(cmd=f"cp -r {source_path} {copied_source_path}", workdir=copied_source_path)
    print(f"cp: {cp_result.exit_code}")
    print(cp_result.output.decode('utf-8'))


    dir_contents = container.exec_run(cmd="ls -la", workdir=copied_source_path)
    print(f"Contents of {copied_source_path} in container:")
    print(dir_contents.output.decode('utf-8'))

    container.exec_run(cmd=f"chown -R developer:developer {copied_source_path}", workdir=copied_source_path)

    #make sure build directory is clean
    container.exec_run(cmd=f"rm -rf {build_dir}/*", workdir=copied_source_path)
    #make sure build directory exists
    container.exec_run(cmd=f"mkdir -p {build_dir}", workdir=source_path)

    compile_result = container.exec_run(cmd=f"cmake -S {copied_source_path}/lib -B {build_dir} -DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake", workdir=source_path)
    assert compile_result.exit_code == 0, f"cmake failed with output: {compile_result.output.decode('utf-8')}"
    print("cmake succeeded")
    make_result = container.exec_run(cmd=f"make -C {build_dir}", workdir=copied_source_path)
    assert make_result.exit_code == 0, f"make failed with output: {make_result.output.decode('utf-8')}"
    print("make succeeded")
    print("Test passed")