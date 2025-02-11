import setuptools
import sys
import platform

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("./src/singletonator/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(-1)

# Determine which attach binary to take into package
package_data = {}

setuptools.setup(
    name="singletonator",
    version=version,
    author="WaimChiu",
    author_email="anothersm@163.com",
    long_description=long_description,
    url="https://github.com/CLAY-zhao/singletonator",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data=package_data,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: System :: Logging"
    ],
    python_requires=">=3.6"
)