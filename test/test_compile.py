import pytest


@pytest.mark.parametrize("tool", ["gdb-multiarch", "cmake", "arm-none-eabi-gcc"])
def test_tools_available(container, tool):
    print("")   #newline for readability
    
    gdb_output = container.exec_run(cmd=f"{tool} --version")
    for l in gdb_output.output.decode("utf-8").splitlines():
        print(l)
    assert gdb_output.exit_code == 0, f"gdb exit code: {gdb_output.exit_code}, output: {gdb_output.output.decode("utf-8").splitlines()}"


def test_compile(container, 
                 source_path="/home/developer/test/lib/"):
    print("")   #newline for readability
    print(f"testing in container {container.id}")
    
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



