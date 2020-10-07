from aws_cdk.aws_lambda import Code, Runtime
from aws_cdk.core import Stack
from b_aws_websocket_api.ws_api import WsApi
from b_aws_websocket_api.ws_deployment import WsDeployment
from b_aws_websocket_api.ws_function import WsFunction
from b_aws_websocket_api.ws_lambda_integration import WsLambdaIntegration
from b_aws_websocket_api.ws_route import WsRoute
from b_aws_websocket_api.ws_stage import WsStage


class TestingStack(Stack):
    def __init__(self, scope: Stack, prefix: str):
        super().__init__(
            scope=scope,
            id=f'{prefix}TestingStack',
            stack_name=f'{prefix}TestingStack'
        )

        self.api: WsApi = WsApi(
            scope=self,
            id=f'{prefix}TestWsApi',
            description='Test description.',
            name=f'{prefix}TestWsApi',
            route_selection_expression='$request.body.action',
        )

        self.stage: WsStage = WsStage(
            scope=self,
            id=f'{prefix}TestStage',
            ws_api=self.api,
            stage_name=f'{prefix}test'.lower(),
            auto_deploy=True,
        )

        self.backend: WsFunction = WsFunction(
            scope=self,
            id=f'{prefix}TestFunction',
            function_name=f'{prefix}TestFunction',
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

        self.integration: WsLambdaIntegration = WsLambdaIntegration(
            scope=self,
            id=f'{prefix}TestIntegration',
            integration_name=f'{prefix}TestIntegration',
            ws_api=self.api,
            function=self.backend
        )

        self.route: WsRoute = WsRoute(
            scope=self,
            id=f'{prefix}TestRoute',
            ws_api=self.api,
            route_key='test',
            authorization_type='NONE',
            route_response_selection_expression='$default',
            target=f'integrations/{self.integration.ref}',
        )

        deployment: WsDeployment = WsDeployment(
            scope=self,
            id=f'{prefix}TestDeployment',
            ws_stage=self.stage
        )

        deployment.node.add_dependency(self.route)
        deployment.node.add_dependency(self.stage)
