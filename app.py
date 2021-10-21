#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from cdk_bootstrapless_synthesizer import BootstraplessStackSynthesizer
# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from lib.sr_stack import SuperResolutionStack

app = core.App()

# class DefaultStackSynthesizer2(core.DefaultStackSynthesizer):
# def synthesize(self, session: core.ISynthesisSession) -> None:


SuperResolutionStack(app, "SuperResolutionStack",
                     # If you don't specify 'env', this stack will be environment-agnostic.
                     # Account/Region-dependent features and context lookups will not work,
                     # but a single synthesized template can be deployed anywhere.

                     # Uncomment the next line to specialize this stack for the AWS Account
                     # and Region that are implied by the current CLI configuration.
                     synthesizer=BootstraplessStackSynthesizer(
                         file_asset_bucket_name=os.getenv('BSS_FILE_ASSET_BUCKET_NAME'),
                         file_asset_prefix=os.getenv('BSS_FILE_ASSET_PREFIX'),
                         file_asset_region_set=[os.getenv('BSS_FILE_ASSET_REGION_SET')],
                     )
                     # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                     )

app.synth(force=True)
