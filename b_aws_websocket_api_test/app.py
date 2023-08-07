from aws_cdk import App

from b_aws_websocket_api_test.infrastructure import Infrastructure

app = App()
Infrastructure(app)
app.synth()
