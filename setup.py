# See LICENSE.txt for license details.
# Copyright (c) 2018 onwards Chris Withers
from setuptools import setup, find_packages

setup(
    name="switcheroo",
    version='2.0.0',
    author='Chris Withers',
    author_email='chris@withers.org',
    license='MIT',
    description=(
        "Efficient dispatch-based calling, that might be a switch statement in another language."
    ),
    long_description=open('README.rst').read(),
    url="https://github.com/simplistix/switcheroo",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.6",
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'sybil>=4',
            'testfixtures'
        ],
        'build': [
            'twine',
            'wheel'
        ]
    },
)
