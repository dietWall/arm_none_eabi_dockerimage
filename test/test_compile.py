import pytest


def print_container_output(output):
    for l in output.output.decode("utf-8").splitlines():
        print(l)

@pytest.mark.parametrize("tool", ["gdb-multiarch", "cmake", "arm-none-eabi-gcc"])
def test_tools_available(container, tool):
    print("")   #newline for readability

    gdb_output = container.exec_run(cmd=f"{tool} --version")
    print_container_output(gdb_output)
    assert gdb_output.exit_code == 0, f"gdb exit code: {gdb_output.exit_code}, output: {gdb_output.output.decode("utf-8").splitlines()}"


def test_compile(container, 
                 source_path="/home/developer/code/test/lib/",
                 build_path="/home/developer/build/"):
    print("")   #newline for readability
    print(f"testing in container {container.id}")
    
    #make sure build directory is clean
    container.exec_run(cmd=f"rm -rf {build_path}")
    #make sure build directory exists
    print_container_output(container.exec_run(cmd=f"mkdir -p {build_path}"))
    
    # output = container.exec_run(cmd="pwd")
    # print_container_output(output)
    # output = container.exec_run(cmd="ls -la")
    # print_container_output(output)
    # output = container.exec_run(cmd="ls -lRa build/")
    # print_container_output(output)

    compile_result = container.exec_run(cmd=f"cmake -S {source_path} -B {build_path} -DCMAKE_TOOLCHAIN_FILE=/home/developer/toolchain/arm-none-eabi-gcc.cmake")
    assert compile_result.exit_code == 0, f"cmake failed with output: {compile_result.output.decode('utf-8')}"
    print("cmake succeeded")
    make_result = container.exec_run(cmd=f"make -C {build_path}")
    assert make_result.exit_code == 0, f"make failed with output: {make_result.output.decode('utf-8')}"
    print("make succeeded")
    print("Test passed")



