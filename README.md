# B.AwsWebsocketApi

An AWS CDK based python library that helps you to create websocket based APIs.

### Description

Creating APIs in AWS is pretty challenging. You have to create stages, deployments,
apis, resources, methods, etc. One might argue that creating a websocket based
API is even harder. This AWS CDK based python library tries to solve this 
inconvenience by offering resources and examples on how to create a websocket
API the correct way. We have spent countless hours to perfect it but still
there will always be some "gotchas" in AWS environment.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

### Related technology

- Python 3
- AWS CDK
- AWS CloudFormation
- AWS API Gateway
- Websockets

### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS.
- You have basic knowledge in websockets.

### Useful sources

- Read more about AWS API Gateway:<br>
https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html.

- Read more about AWS websocket API:<br>
https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-overview.html

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b-aws-websocket-api
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

Create a stack to hold your resources:

```python
from aws_cdk.core import Stack
stack = Stack(...)
```

Create an API:
```python
from b_aws_websocket_api.ws_api import WsApi
api = WsApi(
    scope=stack,
    id='TestWsApi',
    description='Test description.',
    name='TestWsApi',
    route_selection_expression='$request.body.action',
)
```

Create a stage (usually it is called `prod`):
```python
from b_aws_websocket_api.ws_stage import WsStage
stage = WsStage(
    scope=stack,
    id='TestStage',
    ws_api=api,
    stage_name='prod',
    auto_deploy=True,
)
```

Create a lambda function to handle incoming requests (frames):
```python
from b_aws_websocket_api.ws_function import WsFunction
from aws_cdk.aws_lambda import Code, Runtime
backend = WsFunction(
    scope=stack,
    id='TestFunction',
    function_name='TestFunction',
    code=Code.from_inline(
        'def handler(*args, **kwargs):\n'
        '    return {\n'
        '        "isBase64Encoded": False,\n'
        '        "statusCode": 200,\n'
        '        "headers": {},\n'
        '        "body": "{\\"message\\": \\"success\\"}"\n'
        '    }\n'
    ),
    handler='index.handler',
    runtime=Runtime.PYTHON_3_6,
)
```

Create a lambda integration (later will be needed for a route):
```python
from b_aws_websocket_api.ws_lambda_integration import WsLambdaIntegration
integration = WsLambdaIntegration(
    scope=stack,
    id='TestIntegration',
    integration_name='TestIntegration',
    ws_api=api,
    function=backend
)
```

Create a custom route backed by a lambda function:
```python
from b_aws_websocket_api.ws_route import WsRoute
route = WsRoute(
    scope=stack,
    id='TestRoute',
    ws_api=api,
    route_key='test',
    authorization_type='NONE',
    route_response_selection_expression='$default',
    target=f'integrations/{integration.ref}',
)
```

Finally deploy the API:
```python
from  b_aws_websocket_api.ws_deployment import WsDeployment
deployment = WsDeployment(
    scope=stack,
    id='TestDeployment',
    ws_stage=stage
)
```

And don't forget to solve dependencies for the resources!
```python
deployment.node.add_dependency(route)
deployment.node.add_dependency(stage)
```

Now execute `cdk deploy *` and enjoy your new websocket API!

### Testing

The project has tests that can be run. 
Note, that tests are integration tests inherently because they
test how resources are created in AWS environment. Since resources 
are created and tested in AWS you are subject for all the applicable
charges while tests are being run.

#### Setting environment

Before running tests set environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

Or:
- AWS_PROFILE
- AWS_DEFAULT_REGION

#### Running tests

Then run tests from a root directory with `pytest` python testing library:
```
pytest b_aws_websocket_api_test
```

Note that integration tests usually take a while to complete (from 5 to 30
minutes on average).

### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
