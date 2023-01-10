#!/bin/python
import os
import time
import random
from threading import Thread

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

MAIN_CPP_SCRIPT = """
#include "../libs/rwlib.hpp"
#include "../libs/exec.hpp"
#include "../libs/strlib.hpp"
#include "./py_script.hpp"
#ifndef string
    #include <iostream>
#endif

using namespace std;

int main(int argc, char const *argv[])
{

    string temp_py_script;
    for (auto &&i : parse_rep(python_script))
    {
        temp_py_script += i;
    }
    
    int status = execScript("python -c", temp_py_script);
    if (status != 0)
        cout << "Something went wrong !" << endl;
    return 0;
}
"""

print(f""" ________________________
| Welcome to PyExe v1.0  |
| Developed by: Bari BGF |
| [\q] -> Quit           |
|________________________|
""")

MAIN_PY_PATH = "."
while not os.path.exists(MAIN_PY_PATH := input("> Python main file path: ")):
    if MAIN_PY_PATH == "\q": exit(0)
    print("Error: No file found")

OUT_EXE_PATH = "."
while not os.path.exists(os.path.dirname(OUT_EXE_PATH := input("> Out exe file path: "))):
    if OUT_EXE_PATH == "\q": exit(0)
    print("Error: No path found, Please specify a valid path")

print()
progress = Progress("Please wait", 0.5)
progress.start()

with open("../bins/py", 'rb') as bf:
    with open("./py_bin.hpp", 'w') as py_bin_header:
        py_bin_header_content = ""
        py_bin_header_content += "#ifndef string\n\t#include <iostream>\n#endif\n"
        py_bin_header_content += 'string py_bin_rep = \"'
        for i in bf.read():
            py_bin_header_content += hex(i).replace('0x', '') + ','
        py_bin_header_content += '\";'
        py_bin_header.write(py_bin_header_content)

def handle_script(script):
    py_script_content = ""
    for i in script:
        py_script_content += hex(i).replace('0x', '') + ','
    return py_script_content

def handle_quotes(string: str):
    string = string.replace("\'", "\"\"\"")
    return string

NEW_MAIN_PY_PATH = "./" + "".join([random.choice('abcdefgh') for i in range(8)]) + ".py"
with open("./py_script.hpp", "w") as py_script_header:
    with open(MAIN_PY_PATH, "r") as script_file_r:
        handled_script = handle_quotes(script_file_r.read())
        with open(NEW_MAIN_PY_PATH, "w") as script_file_w:
            script_file_w.write(handled_script)

    with open(NEW_MAIN_PY_PATH, "rb") as script_file_bin:
        py_script_header_content = f'string python_script = "{handle_script(script_file_bin.read())}";'
        py_script_header.write(py_script_header_content)

with open("./main.cpp", "w") as main_cpp_file:
    main_cpp_file.write(MAIN_CPP_SCRIPT)

os.system(f"g++ -O3 ./main.cpp -o {OUT_EXE_PATH}")
os.system("rm ./main.cpp")
os.system("rm ./py_bin.hpp")
os.system("rm ./py_script.hpp")
os.system(f"rm {NEW_MAIN_PY_PATH}")

progress.stop()
print("\nDone !")
