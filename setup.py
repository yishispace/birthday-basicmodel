#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="birthday-basicmodel",
    version="0.1.0",
    description="生日提醒工具（基础版）",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "lunar-python>=1.0.0",
        "python-dotenv==1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'birthday=birthday_reminder:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 