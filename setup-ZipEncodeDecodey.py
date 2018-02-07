from setuptools import setup, find_packages
import os,sys

setup(
    name = "ZipEncodeDecode",
    version = "1.0",
    author="Miki Manor",
    author_email="mmanor@isracard.co.il",
    description="Run this module to encode zip to binary and decode the other way",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.5"
    ],
    install_requires=[],
    python_requires='>=3',
    packages = ['ZipEncodeDecode'],
    entry_points={
        'console_scripts': [
            'ZipEncodeDecode = ZipEncodeDecode.__main__:main'
        ]
    },
    )