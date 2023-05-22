#!/bin/python

import os
import sys
import time
import random
from threading import Thread

from __init__ import __version__
from package_compiler import compile_package

THIS_PATH = os.path.dirname(__file__)

class Progress(Thread):
    def __init__(self, flag: str, timeout: float):
        super().__init__()
        self.flag = flag
        self.cond_var = True
        self.timeout = timeout

    def anim(self):
        t = 0
        while self.cond_var:
            if t > 3:
                t = 0
            print(" " * 10, end="")
            b = f"\r{self.flag} " + ". " * t
            print(b, end="")
            print(" " * 10, end="")
            time.sleep(self.timeout)
            t += 1
        print()

    def stop(self):
        self.cond_var = False

    def run(self):
        self.anim()


def get_response(message: str, exception_fn=None, exception_message: str = None) -> str:
    while True:
        response = input(message)
        if response == "\q":
            exit(0)
        if exception_fn and exception_fn(response):
            if exception_message:
                print(exception_message)
            continue
        return response


MAIN_CPP_SCRIPT = """
#include <filesystem>
#include <unistd.h>
#include "../include/rwlib.hpp"
#include "../include/execlib.hpp"
#include "../include/strlib.hpp"
#include "./py_script.hpp"

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char const *argv[])
{
    fs::path thisPath = argv[0];
    fs::path thisSpace = thisPath.parent_path();
    string tempPyScript;
    int temp_status;
    for (auto &&i : parse_rep(python_script)) tempPyScript += i;
    temp_status = chdir(string(thisSpace).c_str());
    char buffer[1000];
    char* temp_str = getcwd(buffer, sizeof(buffer));
    int status = execScript("python -c", tempPyScript);
    if (status != 0) {
        cout << "Something went wrong !" << endl;
        return 1;
    }
    return 0;
}
"""
if len(sys.argv) >= 2:
    MAIN_PY_PATH = sys.argv[1]
    try:
        OUT_EXE_NAME = sys.argv[2]
    except IndexError:
        OUT_EXE_NAME = ""
    try:
        COMPILE_FULL_PROJECT = sys.argv[3]
    except IndexError:
        COMPILE_FULL_PROJECT = True
else:
    try:
        print(f""" ________________________
| Welcome to PyExe v{__version__}  |
| Developed by: Bari BGF |
| [\q] -> Quit           |
|________________________|
""")

        MAIN_PY_PATH = get_response(
            "> Python main file path: ",
            lambda x: not os.path.exists(x),
            "Error: No file found"
        )

        OUT_EXE_NAME = get_response(
            f"> Out exe name [Return for original]: "
        )

        COMPILE_FULL_PROJECT = True if get_response(
            "> Do you want to compile the full project? [Return for YES]: ",
        ) == '' else False
    except KeyboardInterrupt:
        print("\nGood bye !")
        exit(0)

OUT_EXE_PATH = os.path.dirname(MAIN_PY_PATH) + '/'

if OUT_EXE_NAME == '':
    OUT_EXE_PATH += "".join(os.path.basename(MAIN_PY_PATH).split('.')[:-1])
else:
    OUT_EXE_PATH += OUT_EXE_NAME

print()
progress = Progress("Please wait", 0.5)
progress.start()


def handle_script(script: str):
    py_script_content = ""
    for i in script:
        py_script_content += hex(i).replace('0x', '') + ','
    return py_script_content


def handle_quotes(string: str):
    string = string.replace("\'", "\"\"\"")
    return string


NEW_MAIN_PY_PATH = THIS_PATH + "/" + \
    "".join([random.choice('abcdefgh_') for i in range(8)]) + ".py"

with open(THIS_PATH + "/py_script.hpp", "w") as py_script_header:
    with open(MAIN_PY_PATH, "r") as script_file_r:
        handled_script = handle_quotes(script_file_r.read())
        with open(NEW_MAIN_PY_PATH, "w") as script_file_w:
            script_file_w.write(handled_script)

    with open(NEW_MAIN_PY_PATH, "rb") as script_file_bin:
        py_script_header_content = f'string python_script = "{handle_script(script_file_bin.read())}";'
        py_script_header.write(py_script_header_content)

with open(THIS_PATH + "/main.cpp", "w") as main_cpp_file:
    main_cpp_file.write(MAIN_CPP_SCRIPT)

os.system(f"g++ -O3 {THIS_PATH}/main.cpp {THIS_PATH}/C++/*.cpp -o {OUT_EXE_PATH}")
os.system(f"rm {THIS_PATH}/main.cpp")
os.system(f"rm {THIS_PATH}/py_script.hpp")
os.system(f"rm {NEW_MAIN_PY_PATH}")

if COMPILE_FULL_PROJECT:
    compile_package(os.path.abspath(os.path.dirname(MAIN_PY_PATH)), exclude=[os.path.basename(MAIN_PY_PATH)])
    os.system(f"rm {OUT_EXE_PATH}")

progress.stop()
print("\nDone !")
