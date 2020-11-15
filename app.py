#!/usr/bin/env python3

from aws_cdk import core

from cloud_account_monitor.account_provisioning_monitor import AccountProvisioningMonitor


app = core.App()
AccountProvisioningMonitor(app, "Account-Provisioning-Monitor")

app.synth()
