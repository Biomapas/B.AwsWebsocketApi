from aws_cdk.aws_lambda import Code, Runtime, Function
from aws_cdk.core import Stack, CfnOutput

from b_aws_websocket_api.ws_api import WsApi
from b_aws_websocket_api.ws_deployment import WsDeployment
from b_aws_websocket_api.ws_function import WsFunction
from b_aws_websocket_api.ws_lambda_integration import WsLambdaIntegration
from b_aws_websocket_api.ws_route import WsRoute
from b_aws_websocket_api.ws_stage import WsStage


class TestingInfrastructure(Stack):
    def __init__(self, scope: Stack):
        super().__init__(
            scope=scope,
            id='TestingStack',
            stack_name='TestingStack'
        )

        CfnOutput(
            self,
            'TestOutput',
            value='Hello World!',
        )

        Function(
            self,
            'TestFunction',
            code=Code.from_inline(
                'def test():'
                '    return "Success!"'
            ),
            handler='index.test',
            runtime=Runtime.PYTHON_3_6,
        )

        api = WsApi(
            scope=self,
            id='TestWsApi',
            description='Test description.',
            name='TestWsApi',
            route_selection_expression='$request.body.action',
        )

        stage = WsStage(
            scope=self,
            id='TestStage',
            ws_api=api,
            stage_name=f'test',
            auto_deploy=True,
        )

        backend = WsFunction(
            scope=self,
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

        integration = WsLambdaIntegration(
            scope=self,
            id='TestIntegration',
            integration_name='TestIntegration',
            ws_api=api,
            function=backend
        )

        route = WsRoute(
            scope=self,
            id='TestRoute',
            ws_api=api,
            route_key='test',
            authorization_type='NONE',
            route_response_selection_expression='$default',
            target=f'integrations/{integration.ref}',
        )

        deployment = WsDeployment(
            scope=self,
            id='TestDeployment',
            ws_stage=stage
        )

        deployment.node.add_dependency(route)
        deployment.node.add_dependency(stage)
