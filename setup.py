
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='iaklogger',
    packages=find_packages(),
    version='1.0.9',
    license='MIT',
    description='Very basic and easy logger with tag-based filtering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Iakl',
    author_email='estebaniakl@gmail.com',
    url='https://github.com/Iakl/iaklogger',
    download_url='https://github.com/Iakl/iaklogger/archive/refs/tags/v1.0.9.tar.gz',
    keywords=['logger', 'easy', 'print', 'log', 'basic', 'logging', 'tags', 'filtering', 'rich', 'console'],
    install_requires=[
        'rich>=10.0.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
