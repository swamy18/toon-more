from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="toon-format",
    version="0.1.0",
    author="Swamy Gadila",
    author_email="your.email@example.com",
    description="Token-Oriented Object Notation (TOON) encoder for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swamy18/toon-more/tree/main/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="toon format json llm prompt tokens data-annotation",
    project_urls={
        "Bug Reports": "https://github.com/swamy18/toon-more/issues",
        "Source": "https://github.com/swamy18/toon-more/tree/main/python-sdk",
        "Documentation": "https://github.com/swamy18/toon-more/blob/main/python-sdk/README.md",
    },
)
