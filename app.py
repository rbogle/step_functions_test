#!/usr/bin/env python3

from aws_cdk import core

from test_step_fns.test_step_fns_stack import TestStepFnsStack


app = core.App()
TestStepFnsStack(app, "test-step-fns")

app.synth()
