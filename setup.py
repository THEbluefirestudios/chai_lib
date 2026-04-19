from setuptools import setup, find_packages

setup(
    name="token-chai",
    version="1.0.0",
    description="Token-efficient LLM prompting via Chinese compression",
    packages=find_packages(),
    install_requires=[
        "translate>=3.6",
        "openai>=1.0",
        "google-generativeai>=0.7",
        "anthropic>=0.25",
    ],
    python_requires=">=3.9",
)