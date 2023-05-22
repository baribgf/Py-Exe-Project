
from typing import Iterable

from glob import glob
from os.path import dirname, basename
from os import system, remove
from re import fullmatch, search
from shutil import copytree, rmtree, move


def compile_module(module_path: str) -> None:
    module_name = "".join(module_path.split('/')[-1].split('.')[:-1])
    module_pardir_name = dirname(module_path)

    setup_script = f"from setuptools import setup\nfrom Cython.Build import cythonize\nsetup(ext_modules=cythonize([\'{module_path}\']))"

    system(f"python -c \"{setup_script}\" build_ext --inplace >> /dev/null")

    remove("".join(module_path.split('.')[:-1]) + '.c')
    rmtree("./build")

    cmodule_path = tuple(filter(
        lambda path: fullmatch(fr"\./{module_name}\..+\.(so|pyc)", path),
        glob("./*")
    ))[0]

    dest_path = module_pardir_name + '/' + module_name + \
        search(r"\.(so|pyc)$", cmodule_path).group(0)

    move(cmodule_path, dest_path)


def compile_package(package_path: str, exclude: Iterable[str] = []) -> None:
    new_package_path = package_path + '-compiled'

    try:
        copytree(package_path, new_package_path)
    except FileExistsError:
        rmtree(new_package_path)
        return compile_package(package_path, exclude)

    modules_paths = [path for path in glob(
        new_package_path + "/**/*.py", recursive=True)]

    for module_path in modules_paths:
        if not basename(module_path) in exclude:
            compile_module(module_path)
        remove(module_path)
