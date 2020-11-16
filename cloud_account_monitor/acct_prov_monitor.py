from aws_cdk import core
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from .acct_factory_monitor import AccountFactoryMonitor
from .acct_config_monitor import AccountConfigMonitor

class AccountProvMonitor (core.Construct):

    def __init__(self, scope: core.Construct, id: str, factory: AccountFactoryMonitor, config: AccountConfigMonitor, statemachine_timeout: int= 300 ,**kwargs):
        super().__init__(scope, id, **kwargs)

        start_factory_machine = tasks.StepFunctionsStartExecution(
            self, 
            "Account-Factory-StateMachine", 
            state_machine=factory.state_machine,
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,
            output_path="$.Output"
        )

        start_config_machine = tasks.StepFunctionsStartExecution(
            self, 
            "Account-Config-StateMachine", 
            state_machine=config.state_machine,
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,
            output_path="$.Output"
        )        

        start_task = sfn.Pass(self, "start creation")
        inter_task = sfn.Pass(self, "start configuration")
        end_task = sfn.Pass(self, "end provisioning")

        def_chain = start_task.next(start_factory_machine).next(inter_task).next(start_config_machine).next(end_task)

        self.state_machine = sfn.StateMachine(
            self,
            "Account-Provsioning-StateMachine",
            definition = def_chain,
            timeout = core.Duration.seconds(statemachine_timeout)

        )