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
            state_machine=factory
        )

        start_config_machine = tasks.StepFunctionsStartExecution(
            self, 
            "Account-Config-StateMachine", 
            state_machine=config
        )        

        def_chain = start_factory_machine.next(start_config_machine)

        provisioning_machine = sfn.StateMachine(
            self,
            "Account-Provsioning-StateMachine",
            definition = def_chain,
            timeout = core.Duration.seconds(statemachine_timeout)

        )