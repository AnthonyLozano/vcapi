from setuptools import setup

setup(
    name='vcapi',
    packages=['vcapi'],
    version='1.0.1a4',
    description="Python CLI for Veracode's API",
    long_description=open('README.rst').read(),
    author="Anthony Lozano",
    author_email='amlozano1@gmail.com',
    keywords=['veracode', 'api', 'wrapper'],
    install_requires=['requests>=2.11.1',
                      'click>=6.6',
                      'clint',
                      'requests-toolbelt'],
    url='https://github.com/AnthonyLozano/vcapi',
    entry_points={
        'console_scripts': [
            'vcapi=vcapi.vcapi:main',
        ],
    },
)
