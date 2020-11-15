#!/usr/bin/env python3

from aws_cdk import core

from cloud_account_monitor.account_provisioning_monitor import AccountProvisioningMonitor
#from cloud_account_monitor.test_step_fns_stack import TestStepFnsStack

app = core.App()
AccountProvisioningMonitor(app, "fcc-acct-prov-monitor")
#TestStepFnsStack(app,"Test-StepFn-Acct-Monitor")
app.synth()
