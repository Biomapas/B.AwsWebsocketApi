from aws_cdk.core import App

from b_aws_websocket_api_test.infrastructure import Infrastructure

app = App()
Infrastructure(app)
app.synth()
