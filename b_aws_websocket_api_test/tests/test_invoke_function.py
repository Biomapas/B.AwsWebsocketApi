import logging
from typing import Any

from b_aws_testing_framework.credentials import Credentials

from b_aws_websocket_api_test.testing_infrastructure import TestingInfrastructure

logger = logging.getLogger(__name__)


def test_invoke_function(
        stack_outputs: Any
) -> None:
    """
    Invokes a backend lambda function and tests its response.

    :return: No return.
    """
    function_name = stack_outputs[TestingInfrastructure.LAMBDA_FUNCTION_NAME_KEY]

    logger.info(f'Invoking function: {function_name}.')

    session = Credentials().boto_session
    response = session.client('lambda').invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse'
    )

    logger.info(f'Response from lambda function: {response}.')
