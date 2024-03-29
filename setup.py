from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_aws_websocket_api',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_aws_websocket_api_test'
    ]),
    description=(
        'AWS CDK package that helps creating web socket APIs.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        # AWS CDK.
        'aws-cdk-lib>=2.0.0,<3.0.0',
        'aws-cdk-constructs>=2.0.0,<3.0.0',

        # Our.
        'b-stage-deployment>=1.0.0,<2.0.0',

        # Other.
        'websockets>=11.0.0,<12.0.0',
        'pytest>=6.0.2,<7.0.0',
        'pytest-cov>=2.10.1,<3.0.0',
        'pytest-timeout>=1.3.4,<1.5.0'
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='AWS CDK API WebSocket',
    url='https://github.com/Biomapas/B.AwsWebsocketApi.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
