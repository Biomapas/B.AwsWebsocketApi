import hashlib
from typing import Union

from aws_cdk.aws_lambda import IFunction
from aws_cdk.core import Stack
from b_aws_websocket_api.ws_function import WsFunction
from b_aws_websocket_api.ws_integration import WsIntegration


class WsLambdaIntegration(WsIntegration):
    """
    Creates web socket API route lambda integration.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            integration_name: str,
            ws_api: Union[IFunction, WsFunction],
            function: WsFunction,
            *args,
            **kwargs
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param integration_name: The name of the integration.
        :param ws_api: Web socket API for with the integration is being done.
        :param function: A Lambda function to integrate.
        :param args: Additional arguments.
        :param kwargs: Additional named arguments.
        """
        self.__id = id
        self.__integration_name = integration_name
        self.__function = function

        super().__init__(
            scope=scope,
            id=id,
            integration_name=integration_name,
            ws_api=ws_api,
            description=f'Lambda proxy integration for Websocket API {ws_api.name}.',
            integration_type='AWS_PROXY',
            integration_uri=f'arn:aws:apigateway:{scope.region}:lambda:path/2015-03-31/functions/{function.function_arn}/invocations',
            *args,
            **kwargs
        )

    @property
    def function(self):
        return self.__function

    @property
    def hash(self):
        hashable = (
               self.__id +
               self.__integration_name
        ).encode('utf-8')

        return hashlib.sha256(hashable).hexdigest()
