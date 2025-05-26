from setuptools import setup, find_packages

setup(
    name="sailer_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "openai>=0.27.0",
        "python-dotenv>=0.19.0",
        "sentence-transformers>=2.2.2",
        "faiss-cpu>=1.7.2",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "httpx>=0.24.0",
            "pytest-cov>=4.0.0",
        ],
    },
) 