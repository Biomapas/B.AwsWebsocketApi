from functools import lru_cache

from b_aws_testing_framework.credentials import Credentials
from b_cf_outputs.cf_outputs import CfOutputs

from b_aws_websocket_api_test.testing_infrastructure import TestingInfrastructure


@lru_cache
def get_stack_outputs():
    outputs = CfOutputs(Credentials().boto_session).get_outputs(TestingInfrastructure.ROOT_STACK_NAME)
    return outputs[TestingInfrastructure.ROOT_STACK_NAME]
