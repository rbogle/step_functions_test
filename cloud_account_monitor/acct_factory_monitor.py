from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from .lambdas import StateHandlerLambda, AccountFactoryLambda

class AccountFactoryMonitor(core.Construct):
    def __init__(self, scope: core.Construct, id: str, *, polling_delay: int = 5, statemachine_timeout: int= 300,**kwargs):
        super().__init__(scope, id, **kwargs)

        state_fn = StateHandlerLambda(self, "factory-state-handler").function
        factory_fn = AccountFactoryLambda(self, "account-create-handler").function

        creating_state = tasks.LambdaInvoke(
            self,
            "Set Creating State",
            lambda_function = state_fn,
            output_path="$.Payload"
        )

        completed_state = tasks.LambdaInvoke(
            self,
            "Set Completed State",
            lambda_function = state_fn,
            output_path="$.Payload"
        )

        factory_task = tasks.LambdaInvoke(
            self,
            "Request Account Creation",
            lambda_function = factory_fn,
            output_path="$.Payload"
        )

        polling_task = tasks.LambdaInvoke(
            self,
            "Poll Account Creation",
            lambda_function = factory_fn,
            output_path="$.Payload"
        )

        delay = sfn.Wait(
            self,
            "Delay Polling",
            time=sfn.WaitTime.duration(core.Duration.seconds(polling_delay))
        )

        is_ready = sfn.Choice(self, "Account Ready?")
        acct_ready = sfn.Condition.string_equals('$.state', "READY")
        acct_pending = sfn.Condition.string_equals('$.state', "PENDING")
        success = sfn.Succeed(self, "Creation Succeeded")

        failed = sfn.Fail(
            self,
            "Creation Failed",
            cause="Bad value in Polling loop"
        )
        # this is the loop which polls for state change, either looping back to delay or setting completion state and finishing
        is_ready.when(acct_pending, delay).when(acct_ready, completed_state.next(success)).otherwise(failed)
        # this is the main chain starting with creation request a delay and then polling loop
        creator_chain = factory_task.next(creating_state).next(delay).next(polling_task).next(is_ready)
        
        self.state_machine = sfn.StateMachine(
            self,
            "Account-Creation-StateMachine",
            definition = creator_chain,
            timeout = core.Duration.seconds(statemachine_timeout)
        )