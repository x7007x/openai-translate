from pathlib import Path

from setuptools import setup

setup(
    name="openai-translate",
    version="1.0.2",
    description="Translate via OpenAI ChatGPT Translate with requests, no login or API key",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Ahmed Negm",
    license="MIT",
    url="https://github.com/x7007x/openai-translate",
    project_urls={
        "Homepage": "https://github.com/x7007x/openai-translate",
        "Repository": "https://github.com/x7007x/openai-translate",
        "Bug Tracker": "https://github.com/x7007x/openai-translate/issues",
    },
    keywords=["openai", "chatgpt", "translate", "translation", "translator"],
    packages=["openai_translate"],
    install_requires=["requests"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
)
