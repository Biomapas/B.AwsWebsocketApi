import logging

import boto3

from biomapas_aws_api_ws_test.testing_manager import TestingManager

logger = logging.getLogger(__name__)


def test_invoke_function() -> None:
    """
    Invokes a backend lambda function and tests its response.

    :return: No return.
    """
    # The function name is defined in our testing infrastructure file.
    WS_FUNCTION_NAME = 'TestFunction'

    logger.info(f'Invoking function: {WS_FUNCTION_NAME}.')

    session = boto3.session.Session(profile_name=TestingManager.TEST_PROFILE)
    response = session.client('lambda', region_name=TestingManager.AWS_REGION_NAME).invoke(
        FunctionName=WS_FUNCTION_NAME,
        InvocationType='RequestResponse'
    )

    logger.info(f'Response from lambda function: {response}.')
