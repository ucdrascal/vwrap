from setuptools import setup, find_packages
from os import path

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='vwrap',
    version='0.1.0',

    description='',
    long_description=readme(),

    url='https://github.com/ucdrascal/vwrap',

    author='Kenneth Lyons',
    author_email='ixjlyons@gmail.com',

    license='GPLv3',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='vrep robotics simulation',

    packages=find_packages()
)
