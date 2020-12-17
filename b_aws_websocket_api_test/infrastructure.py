from aws_cdk.aws_lambda import Code, Runtime
from aws_cdk.core import CfnOutput, Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_aws_websocket_api.ws_api import WsApi
from b_aws_websocket_api.ws_deployment import WsDeployment
from b_aws_websocket_api.ws_function import WsFunction
from b_aws_websocket_api.ws_lambda_integration import WsLambdaIntegration
from b_aws_websocket_api.ws_route import WsRoute
from b_aws_websocket_api.ws_stage import WsStage


class Infrastructure(TestingStack):
    LAMBDA_FUNCTION_NAME_KEY = 'LambdaFunctionName'
    WEBSOCKET_API_URL_KEY = 'WsApiUrl'

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        self.api: WsApi = WsApi(
            scope=self,
            id=f'{self.global_prefix()}TestWsApi',
            description='Test description.',
            name=f'{self.global_prefix()}TestWsApi',
            route_selection_expression='$request.body.action',
        )

        self.stage: WsStage = WsStage(
            scope=self,
            id=f'{self.global_prefix()}TestStage',
            ws_api=self.api,
            stage_name=f'{self.global_prefix()}test'.lower(),
            auto_deploy=False,
        )

        self.backend: WsFunction = WsFunction(
            scope=self,
            id=f'{self.global_prefix()}TestFunction',
            function_name=f'{self.global_prefix()}TestFunction',
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
            id=f'{self.global_prefix()}TestIntegration',
            integration_name=f'{self.global_prefix()}TestIntegration',
            ws_api=self.api,
            function=self.backend
        )

        self.route: WsRoute = WsRoute(
            scope=self,
            id=f'{self.global_prefix()}TestRoute',
            ws_api=self.api,
            route_key='test',
            authorization_type='NONE',
            route_response_selection_expression='$default',
            target=f'integrations/{self.integration.ref}',
        )

        deployment: WsDeployment = WsDeployment(
            scope=self,
            id=f'{self.global_prefix()}TestDeployment',
            ws_stage=self.stage
        )

        deployment.node.add_dependency(self.route)
        deployment.node.add_dependency(self.stage)

        self.add_output(self.LAMBDA_FUNCTION_NAME_KEY, self.backend.function_name)
        self.add_output(self.WEBSOCKET_API_URL_KEY, self.stage.ws_url)
