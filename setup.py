""" Setup for breaker library """

from setuptools import setup, find_packages

setup(
    name="breaker",
    version="0.0.1",
    description="Simple python library for circuit breaker pattern",
    url="https://github.com/80pctsols/breaker.git",
    author="Sam Johnson",
    author_email="sjohnson540@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages()
)
