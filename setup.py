from setuptools import setup, find_packages

setup(
    name='osa_system',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
