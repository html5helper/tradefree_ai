from setuptools import setup, find_packages

setup(
    name="tradefree_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "requests"
    ],
    python_requires=">=3.10",
) 