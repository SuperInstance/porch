from setuptools import setup, find_packages

setup(
    name="porch-cli",
    version="0.1.0",
    description="A CLI for 3 a.m. thoughts. The small gods, as a tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SuperInstance",
    license="MIT",
    packages=["porch"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup",
    ],
    entry_points={
        "console_scripts": [
            "porch=porch.cli:main",
        ],
    },
)
