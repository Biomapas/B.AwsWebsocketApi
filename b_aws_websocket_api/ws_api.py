from typing import Optional, Any

from aws_cdk.aws_apigatewayv2 import CfnApi
from aws_cdk.core import Stack


class WsApi(CfnApi):
    """
    Creates a web socket api.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            api_key_selection_expression: Optional[str] = None,
            description: Optional[str] = None,
            disable_schema_validation: Optional[bool] = None,
            fail_on_warnings: Optional[bool] = None,
            name: Optional[str] = None,
            route_selection_expression: Optional[str] = None,
            tags: Any = None,
            version: Optional[str] = None,
            *args,
            **kwargs
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param api_key_selection_expression: An API key selection expression. Supported only for WebSocket APIs.
        :param description: The description of the API.
        :param disable_schema_validation: Avoid validating models when creating a deployment.
        :param fail_on_warnings: Specifies whether to rollback the API creation when a warning is encountered.
        By default, API creation continues if a warning is encountered.
        :param name: The name of the API.
        :param route_selection_expression: The route selection expression for the API.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        :param version: A version identifier for the API.
        """
        super().__init__(
            scope=scope,
            id=id,
            api_key_selection_expression=api_key_selection_expression,
            description=description,
            disable_schema_validation=disable_schema_validation,
            fail_on_warnings=fail_on_warnings,
            name=name,
            protocol_type='WEBSOCKET',
            route_selection_expression=route_selection_expression,
            tags=tags,
            version=version,
            *args,
            **kwargs
        )
