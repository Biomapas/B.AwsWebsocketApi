from aws_cdk.core import Stack, CfnOutput
from b_aws_testing_framework.tools.cdk_testing.testing_manager import TestingManager
from b_aws_websocket_api_test.testing_stack import TestingStack


class TestingInfrastructure(Stack):
    if not TestingManager.is_global_prefix_set():
        TestingManager.set_global_prefix()

    PREFIX = TestingManager.get_global_prefix()
    ROOT_STACK_NAME = f'{PREFIX}TestingInfrastructure'

    LAMBDA_FUNCTION_NAME_KEY = f'{PREFIX}LambdaFunctionName'
    WEBSOCKET_API_URL_KEY = f'{PREFIX}WsApiUrl'

    def __init__(self, scope: Stack):
        super().__init__(
            scope=scope,
            id=self.ROOT_STACK_NAME,
            stack_name=self.ROOT_STACK_NAME
        )

        testing_stack: TestingStack = TestingStack(self, self.PREFIX)

        CfnOutput(self, self.LAMBDA_FUNCTION_NAME_KEY, value=testing_stack.backend.function_name)
        CfnOutput(self, self.WEBSOCKET_API_URL_KEY, value=testing_stack.stage.ws_url)
