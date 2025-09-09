"""
NOTE use as a configuration file and a command-line interface 
        for various tasks related to package management
"""
from setuptools import setup, find_packages

setup(
    name="E-commerce-Behavior-Analysis-Platform-for-customers-",
    version="0.1.0",
    author="Sommer Thao Le",
    author_email="thaosle4@gmail.com",
    description="A project that uses the framework Apache AirFlow and using a pre-trained AI model from Textblob",
    packages=find_packages(),
    url="https://github.com/slethao/E-commerce-Behavior-Analysis-Platform-for-customers-.git",
    install_requires=[
        'scikit-learn',
        'apache-airflow',
        'textblob',
        'os',
        'psycopg2',
        'dotenv',
        're'
    ],
    python_requires=">=3.5",
)