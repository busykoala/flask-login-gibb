import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

NAME = '183_lb3_gruppe2'
VERSION = '1.0.0'
AUTHOR = 'gruppe_2'
URL = 'git@gitlab.iet-gibb.ch:mos111952/183_lb3_gruppe2.git'
REQUIRED = [
    'Flask',
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNUv3',
    ],
    install_requires=REQUIRED,
)
