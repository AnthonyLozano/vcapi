from distutils.core import setup

setup(
    name='vcapi',
    packages=['vcapi'],
    version=1.0,
    description="Python API wrapper for Veracode's API",
    author="Anthony Lozano",
    author_email='amlozano1@gmail.com',
    keywords=['veracode', 'api'],
    requires=['requests', 'click']

)