import os
import subprocess
import sys
from packaging.version import Version

import numpy
import setuptools.command.build_py
import setuptools.command.develop
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

# Check Python version
python_version = sys.version.split()[0]
if Version(python_version) < Version("3.9") or Version(python_version) >= Version("3.12"):
    raise RuntimeError("NViXTTS requires python >= 3.9 and < 3.12 but your Python version is {}".format(sys.version))

# Read version file
cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "NViXTTS", "VERSION")) as fin:
    version = fin.read().strip()

# Custom class for build_py
class build_py(setuptools.command.build_py.build_py): 
    def run(self):
        setuptools.command.build_py.build_py.run(self)

# Custom class for develop
class develop(setuptools.command.develop.develop):
    def run(self):
        setuptools.command.develop.develop.run(self)

# Packet data
package_data = ["NViXTTS/server/templates/*"]

# pip dependency installation function
def pip_install(package_name):
    subprocess.call([sys.executable, "-m", "pip", "install", package_name])

# Read the requirements file
requirements = open(os.path.join(cwd, "requirements.txt"), "r").readlines()

# Read README
with open("README.md", "r", encoding="utf-8") as readme_file:
    README = readme_file.read()

# Cython extensions
exts = [
    Extension(
        name="NViXTTS.tts.utils.monotonic_align.core",
        sources=["NViXTTS/tts/utils/monotonic_align/core.pyx"],
    )
]

setup(
    name="NViXTTS",
    version=version,
    url="https://github.com/iris-mygh/NViXTTS_pl",
    author="Iris",
    author_email="irisle.cv@gmail.com",
    description="Deep learning for Vietnamese Text to Speech",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    include_dirs=[numpy.get_include()],
    ext_modules=cythonize(exts, language_level=3),
    include_package_data=True,
    packages=find_packages(include=["NViXTTS", "NViXTTS.*"], exclude=["*.tests", "*tests.*", "tests.*", "*tests", "tests"]),
    package_data={
        "NViXTTS": ["VERSION"],
    },
    package_dir={"NViXTTS": "NViXTTS"},
    cmdclass={
        "build_py": build_py,
        "develop": develop,
    },
    install_requires=requirements,
    python_requires=">=3.9.0, <3.12",
    entry_points={"console_scripts": ["nvixtts=NViXTTS.bin.synthesize:main", "nvixtts-server=NViXTTS.server.server:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
)
