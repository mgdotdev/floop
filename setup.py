from setuptools import setup, find_packages, Extension
from os.path import join


c_extensions = [
    Extension(
        "floop.tools.extensions",
        [join("src", "floop", "tools", "extensions.c")]
    ),
]

setup(
    name="floop",
    version="0.0.1",
    python_requires=">=3.9",
    description="fast loops in python",
    url="https://github.com/1mikegrn/floop",
    author="Michael Green",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    tests_require=["pytest"],
    ext_modules=c_extensions
)
