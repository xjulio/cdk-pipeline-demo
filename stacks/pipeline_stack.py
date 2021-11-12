from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as actions
from aws_cdk import pipelines


class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #
        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(
            self, 'Pipeline',
            pipeline_name="InfraPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_artifact,
                trigger=actions.GitHubTrigger.POLL,
                owner="xjulio",
                repo="cdk-pipeline-demo",
                branch="main",
                oauth_token=core.SecretValue.secrets_manager("tokens/github/xjulio")
            ),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command="npm install -g aws-cdk && pip install -r requirements.txt",
                synth_command="cdk synth"
            )
        )
