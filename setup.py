#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="mouse-rebind",
    version="0.1.0",
    description="Ferramenta para reconfigurar botões de mouse USB via comandos de controle HID",
    author="Seu Nome",
    author_email="seuemail@exemplo.com",
    url="https://github.com/seunome/mouse-rebind",
    packages=find_packages(),
    install_requires=[
        "pyusb>=1.2.1",
    ],
    entry_points={
        'console_scripts': [
            'mouse-finder=mouse_finder:main',
            'mouse-rebind=mouse_rebind:main',
            'mouse-finder-en=mouse_finder_en:main',
            'mouse-rebind-en=mouse_rebind_en:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
