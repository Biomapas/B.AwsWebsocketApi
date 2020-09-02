from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='biomapas_aws_api_ws',
    version='0.0.2',
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'biomapas_aws_api_ws_test'
    ]),
    description=(
        'AWS CDK package that helps creating web socket APIs.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        # Aws cdk specific.
        "aws-cdk.core>=1.61.1,<2.0.0",
        "aws_cdk.aws_apigatewayv2>=1.61.1,<2.0.0",
        "aws-cdk.aws-lambda>=1.61.1,<2.0.0",
        "aws-cdk.custom_resources>=1.61.1,<2.0.0",
        # Other.
        "biomapas-continuous-subprocess>=1.0.0,<2.0.0"
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='AWS CDK API WebSocket',
    url='https://github.com/biomapas/BiomapasAwsApiWs.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
