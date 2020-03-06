from setuptools import setup

setup(
    name="pyvavr",
    version="0.0.1",
    author="Florian Schulz",
    author_email="florian.schulz@flschlz.de",
    description=("Try to reimplement vavr for python."),
    license="Apache 2.0",
    keywords="functional datastructures",
    # url = "http://packages.python.org/an_example_pypi_project",
    packages=['pyvavr', 'tests'],
    # long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License"
    ],
    install_requires=[],
)
