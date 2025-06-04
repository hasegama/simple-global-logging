from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simple-global-logging",
    version="0.1.0",
    author="hasegama",
    author_email="40445443+hasegama@users.noreply.github.com",
    description="A simple global logging wrapper library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasegama/simple-global-logging",
    packages=find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    include_package_data=True,
) 