import json

from aws_cdk import core
from stacks.lambda_stack import LambdaStack


def test_lambda_handler():
    template = get_template()
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']

    assert len(functions) == 1
    assert functions[0]['Properties']['Handler'] == 'handler.main'


def get_template():
    app = core.App()

    LambdaStack(app, 'Stack')

    return app.synth().get_stack_by_name('Stack').template


def get_template_as_json():
    return json.dumps(get_template())
