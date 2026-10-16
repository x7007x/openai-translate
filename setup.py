from setuptools import setup

setup(
    name="openai-translate",
    version="1.0.0",
    description="Translate via OpenAI ChatGPT Translate with requests, no login or API key",
    packages=["openai_translate"],
    install_requires=["requests"],
    python_requires=">=3.8",
)
