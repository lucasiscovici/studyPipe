from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'studyPipe', 'version.py')) as f:
    exec(f.read())
    
setup(
    name='studyPipe',
    version=__version__,
    description='Conveniant Pipe in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/luluperet/studyPipe',
    },
    author='Lucas Iscovici',
    author_email='iscovici.lucas@yahoo.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='pipe helper tool magrittr data science',
    packages=find_packages(exclude=[]),
    install_requires=[
        'sspipe==0.1.13',
        'dfply==0.3.3',
        'toolz==0.10.0'
    ]
)
