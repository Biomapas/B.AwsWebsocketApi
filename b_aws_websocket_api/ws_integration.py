from typing import Optional, Any

from aws_cdk.aws_apigatewayv2 import CfnIntegration, CfnIntegrationResponse
from aws_cdk.core import Stack
from jsii import Number

from b_aws_websocket_api.ws_api import WsApi


class WsIntegration(CfnIntegration):
    """
    Creates web socket API route integration.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            integration_name: str,
            ws_api: WsApi,
            integration_type: str,
            connection_type: Optional[str] = None,
            content_handling_strategy: Optional[str] = None,
            credentials_arn: Optional[str] = None,
            description: Optional[str] = None,
            integration_method: Optional[str] = None,
            integration_uri: Optional[str] = None,
            passthrough_behavior: Optional[str] = None,
            request_parameters: Any = None,
            request_templates: Any = None,
            template_selection_expression: Optional[str] = None,
            timeout_in_millis: Optional[Number] = None,
            default_integration_response: Optional[bool] = None,
            *args,
            **kwargs
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param integration_name: The name of the integration.
        :param ws_api: Web socket API for with the integration is being done.
        :param integration_type: The integration type of an integration.
        :param connection_type: The type of the network connection to the integration endpoint.
        Specify INTERNET for connections through the public routable internet or VPC_LINK for private connections
        between API Gateway and resources in a VPC.
        :param content_handling_strategy: Specifies how to handle response payload content type conversions.
        Supported values are CONVERT_TO_BINARY and CONVERT_TO_TEXT.
        :param credentials_arn: Specifies the credentials required for the integration, if any.
        :param description: The description of the integration.
        :param integration_method: Specifies the integration's HTTP method type.
        :param integration_uri: For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration,
        specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load
        Balancer listener, Network Load Balancer listener, or AWS Cloud Map service.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the
        Content-Type header in the request, and the available mapping templates specified as the requestTemplates
        property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER.
        :param request_parameters: A key-value map specifying request parameters that are passed from the method
        request to the backend.
        :param request_templates: Represents a map of Velocity templates that are applied on the request payload
        based on the value of the Content-Type header sent by the client.
        :param template_selection_expression: The template selection expression for the integration.
        :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs.
        :param default_integration_response: Specify whether to create an integration response resource.
        """
        super().__init__(
            scope=scope,
            id=id,
            api_id=ws_api.ref,
            integration_type=integration_type,
            connection_type=connection_type,
            content_handling_strategy=content_handling_strategy,
            credentials_arn=credentials_arn,
            description=description,
            integration_method=integration_method,
            integration_uri=integration_uri,
            passthrough_behavior=passthrough_behavior,
            request_parameters=request_parameters,
            request_templates=request_templates,
            template_selection_expression=template_selection_expression,
            timeout_in_millis=timeout_in_millis,
            *args,
            **kwargs
        )

        if default_integration_response in [True, None]:
            CfnIntegrationResponse(
                scope=scope,
                id=f'{integration_name}Response',
                api_id=ws_api.ref,
                integration_id=self.ref,
                integration_response_key='$default',
            )
