from setuptools import setup, find_packages

setup(
    name="python_calculator_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "calculator-app = app.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
