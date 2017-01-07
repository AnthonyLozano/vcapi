from distutils.core import setup

setup(
    name='vcapi',
    packages=['vcapi'],
    version='1.0.0.a1',
    description="Python API wrapper for Veracode's API",
    author="Anthony Lozano",
    author_email='amlozano1@gmail.com',
    keywords=['veracode', 'api', 'wrapper'],
    install_requires=['requests', 'click'],
    url='https://github.com/AnthonyLozano/vcapi',
    entry_points={
        'console_scripts': [
            'vcapi=vcapi.vcapi:main',
        ],
    },
)
