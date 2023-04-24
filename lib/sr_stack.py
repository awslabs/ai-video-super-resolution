from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_python as _lambda_py,
    aws_apigateway as apigw,
    aws_batch as batch,
    aws_efs as _efs,
    aws_s3 as as3,
    aws_iam as iam,
    aws_ec2 as ec2,
    core
)
import os

EFS_PATH = '/mnt/efs'

class SuperResolutionStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, enableInferentia: bool, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        stack = core.Stack.of(self)
        self.template_options.description = '(SO8009) AI Video Super Resolution. Template version v2.0.0'
        access_log_bucket = as3.Bucket(
            self, 'SuperResolutionBucketAccessLog',
            encryption = as3.BucketEncryption.S3_MANAGED,
            removal_policy = core.RemovalPolicy.RETAIN,
            object_ownership = as3.ObjectOwnership.OBJECT_WRITER,
            server_access_logs_prefix = 'logBucketAccessLog')

        s3 = as3.Bucket(
            self, 'SuperResolutionStorage',
            server_access_logs_bucket = access_log_bucket,
            server_access_logs_prefix = 'blobstoreBucketAccessLog',
            encryption = as3.BucketEncryption.S3_MANAGED,
            removal_policy = core.RemovalPolicy.RETAIN,
            object_ownership = as3.ObjectOwnership.OBJECT_WRITER,
            enforce_ssl = True,
        )

        # context
        # enableInferentia = self.node.try_get_context('inferentia')
        # if enableInferentia is None or enableInferentia[:1]=='t':
        #     enableInferentia = True
        # else:
        #     enableInferentia=False
        maxv_cpus_parameter = core.CfnParameter(self, 'MaxvCpus',
            type = 'Number',
            min_value=0,
            default = 16
        )
        
        core.CfnCondition(self, 'IsChinaRegionCondition', expression = core.Fn.condition_equals(core.Aws.PARTITION, 'aws-cn'))
        
        if enableInferentia:
            instanceTypes = 'inf1.xlarge'
            ami_id = ec2.MachineImage.from_ssm_parameter('/aws/service/ecs/optimized-ami/amazon-linux-2/inf/recommended/image_id', ec2.OperatingSystemType.LINUX)
            imageUrl = core.Fn.condition_if(
                'IsChinaRegionCondition',
                f'753680513547.dkr.ecr.cn-north-1.amazonaws.com.cn/ai-video-super-resolution-inf1:v2.2.0',
                f'366590864501.dkr.ecr.us-west-2.amazonaws.com/ai-video-super-resolution-inf1:v2.2.0'
            )
            #Pre-build docker image
            
            linux_parameters = {
                                    "devices": [
                                        {
                                            "containerPath": "/dev/neuron0",
                                            "hostPath": "/dev/neuron0",
                                            "permissions": [
                                                "read",
                                                "write"
                                            ]
                                        }
                                    ]
                                }
        else:
            instanceTypes = 'g4dn.xlarge'
            ami_id = ec2.MachineImage.from_ssm_parameter('/aws/service/ecs/optimized-ami/amazon-linux-2/gpu/recommended/image_id', ec2.OperatingSystemType.LINUX)
            imageUrl = core.Fn.condition_if(
                'IsChinaRegionCondition',
                f'753680513547.dkr.ecr.cn-north-1.amazonaws.com.cn/ai-video-super-resolution-gpu:v2.2.0',
                f'366590864501.dkr.ecr.us-west-2.amazonaws.com/ai-video-super-resolution-gpu:v2.2.0'
            )
            #Pre-build docker image
            linux_parameters = None
        compute_image = imageUrl.to_string()

        # create vpc
        vpc = ec2.Vpc(self, "SuperResolutionVPC",
            max_azs = 2,
            subnet_configuration= [
                {
                'cidrMask': 24,
                'name': 'public',
                'subnetType': ec2.SubnetType.PUBLIC
                },
                {
                'cidrMask': 24,
                'name': 'private',
                'subnetType': ec2.SubnetType.PRIVATE
                }
            ]
        )

        vpc.add_gateway_endpoint('S3GatewayEndpoint', service = ec2.GatewayVpcEndpointAwsService.S3)
        vpc.add_flow_log('VpcFlowlogs', destination=ec2.FlowLogDestination.to_s3(access_log_bucket, key_prefix='VpcFlowlogs'))

        access_log_bucket.add_to_resource_policy(iam.PolicyStatement(
            sid = 'AWSLogDeliveryWrite',
            principals =  [iam.ServicePrincipal('delivery.logs.amazonaws.com')],
            actions =  ['s3:PutObject'],
            resources = [access_log_bucket.arn_for_objects(f'VpcFlowlogs/AWSLogs/${core.Aws.ACCOUNT_ID}/*')],
        ))
        access_log_bucket.add_to_resource_policy(iam.PolicyStatement(
            sid = 'AWSLogDeliveryWrite',
            principals =  [iam.ServicePrincipal('delivery.logs.amazonaws.com')],
            actions =  ['s3:GetBucketAcl', 's3:ListBucket'],
            resources = [access_log_bucket.bucket_arn],
        ))
        # create efs
        filesystemSG = ec2.SecurityGroup(self, 'filesystemSG',
            vpc=vpc,
            allow_all_outbound =  False,
            description = 'EFS SG'
        )
        filesystemSG.add_egress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.all_tcp())
        filesystemSG.add_egress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.all_udp())
        filesystem =  _efs.FileSystem(
            self,
            'EfsFileSystem',
            encrypted=True,
            file_system_name = 'SuperResolutionTemp',
            vpc = vpc,
            lifecycle_policy = _efs.LifecyclePolicy.AFTER_7_DAYS,
            removal_policy = core.RemovalPolicy.RETAIN,
            security_group = filesystemSG
        )

        filesystem.connections.allow_default_port_from(ec2.Peer.ipv4(vpc.vpc_cidr_block))

        efs_ap = filesystem.add_access_point('AccessPoint',
                                           create_acl=_efs.Acl(owner_gid='1001', owner_uid='1001', permissions='750'),
                                           path="/sr",
                                           posix_user=_efs.PosixUser(gid="1001", uid="1001"))

        # Split Video and Submit Job
        lambdaSG = ec2.SecurityGroup(self, 'lambdaSG',
            vpc=vpc,
            allow_all_outbound =  True,
            description = 'Lambda SG'
        )

        my_lambda = _lambda_py.PythonFunction(
            self, 'split',
            handler='handler',
            entry='lambda',
            index = 'split.py',
            vpc = vpc,
            function_name = 'SuperResolutionSplitVideo',
            environment={
                'PARALLEL_GROUPS': '2',
                'EFS_PATH': EFS_PATH,
                'user_agent_extra': "AwsSolution/SO8009/v1.0.0",
                'S3_BUCKET': s3.bucket_name,
                'instance_types': instanceTypes
            },
            runtime=_lambda.Runtime.PYTHON_3_8,
            tracing = _lambda.Tracing.ACTIVE,
            layers = [_lambda.LayerVersion(self, 'ffprobe', code=_lambda.Code.asset('layers/ffprobe.zip'))],
            filesystem = _lambda.FileSystem.from_efs_access_point(efs_ap, EFS_PATH),
            #log_retention= alogs.RetentionDays.ONE_MONTH,
            timeout = core.Duration.seconds(300),
            memory_size = 4096,
            security_groups = [lambdaSG]
        )
        api_endpoint = apigw.LambdaRestApi(
            self, 'SuperResolutionEndpoint',
            endpoint_configuration = apigw.EndpointConfiguration(types=[apigw.EndpointType('REGIONAL')]),
            handler=my_lambda,
            #eploy_options=apigw.StageOptions(access_log_destination)
        )
        s3.grant_read(my_lambda)

        # IAM
        batchServiceRole = iam.Role(self, 'BatchServiceRole', assumed_by = iam.CompositePrincipal(iam.ServicePrincipal('batch.amazonaws.com')),
            managed_policies =[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSBatchServiceRole'),
            ]
        )

        ec2Role = iam.Role(self, 'BatchEC2Role', assumed_by = iam.CompositePrincipal(iam.ServicePrincipal('ec2.amazonaws.com')),
            managed_policies =[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonEC2ContainerServiceforEC2Role'),
            ]
        )

        ec2IAMProfile = iam.CfnInstanceProfile(self, 'BatchEC2RoleInstanceProfile', roles = [ec2Role.role_name] )

        batchSG = ec2.SecurityGroup(self, 'BatchSG',
            vpc=vpc,
            allow_all_outbound =  True,
            description = 'Batch SG'
        )
        #batchSG.add_egress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.all_tcp())

        batchPolicy = iam.PolicyStatement(effect =iam.Effect.ALLOW)
        batchPolicy.add_actions("batch:SubmitJob")
        batchPolicy.add_all_resources()
        my_lambda.add_to_role_policy(batchPolicy)
        spotFleetRole = iam.Role(self, 'SpotFleetRole', assumed_by = iam.CompositePrincipal(iam.ServicePrincipal('ec2.amazonaws.com')),
            managed_policies =[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonEC2SpotFleetTaggingRole'),
            ]
        )
        jobRole = iam.Role(self, 'BatchJobRole', assumed_by = iam.CompositePrincipal(iam.ServicePrincipal('ecs-tasks.amazonaws.com')))
        s3.grant_read_write(jobRole)

        # define launch template
        myLaunchTemplate = ec2.LaunchTemplate(self, 'LaunchTemplate',
            block_devices=[ec2.BlockDevice(device_name = '/dev/xvda',
                                           volume = ec2.BlockDeviceVolume.ebs(200, encrypted=True))
            ],
            detailed_monitoring = True,
            launch_template_name = 'SuperResolution_template'
        )

        # Compute Environment
        onDemandComputeEnv = batch.ComputeEnvironment(self, 'onDemandSuperResolutionComputeEnv',
            service_role = batchServiceRole,
            compute_resources = batch.ComputeResources(
                instance_role = ec2IAMProfile.attr_arn,
                vpc = vpc,
                image = ami_id,
                launch_template = batch.LaunchTemplateSpecification(launch_template_name='SuperResolution_template'),
                instance_types = [ec2.InstanceType(instanceTypes)],
                maxv_cpus = maxv_cpus_parameter.value_as_number,
                minv_cpus = 0,
                type = batch.ComputeResourceType('ON_DEMAND'),
                vpc_subnets = ec2.SubnetSelection(subnets=vpc.private_subnets),
                security_groups = [batchSG],
                )
        )
        SpotComputeEnv = batch.ComputeEnvironment(self, 'SpotSuperResolutionComputeEnv',
            service_role = batchServiceRole,
            compute_resources = batch.ComputeResources(
                instance_role = ec2IAMProfile.attr_arn,
                vpc = vpc,
                image = ami_id,
                launch_template = batch.LaunchTemplateSpecification(launch_template_name='SuperResolution_template'),
                instance_types = [ec2.InstanceType(instanceTypes)],
                maxv_cpus = maxv_cpus_parameter.value_as_number,
                minv_cpus = 0,
                type = batch.ComputeResourceType('SPOT'),
                vpc_subnets = ec2.SubnetSelection(subnets=vpc.private_subnets),
                security_groups = [batchSG],
                allocation_strategy = batch.AllocationStrategy('SPOT_CAPACITY_OPTIMIZED'),
                spot_fleet_role =  spotFleetRole
                )
        )
        # job Queue
        onDemandjobQueue = batch.JobQueue(self, 'onDemandjobQueue',
            compute_environments = [
                batch.JobQueueComputeEnvironment(compute_environment = onDemandComputeEnv, order=5)
                ],
            job_queue_name = 'SuperResolution_queue_onDemand',
            priority = 10
        )
        SpotjobQueue = batch.JobQueue(self, 'SpotjobQueue',
            compute_environments = [
                batch.JobQueueComputeEnvironment(compute_environment = SpotComputeEnv, order=5),
                ],
            job_queue_name = 'SuperResolution_queue_Spot',
            priority = 10
        )

        # Job Definition
        batch.CfnJobDefinition(self, 'ComputingBatch',
            type =  'container',
            container_properties = batch.CfnJobDefinition.ContainerPropertiesProperty(image = compute_image,
                memory = 7000,
                vcpus = 4,
                command = [
                    '-i',
                    'Ref::File',
                    '-s',
                    'Ref::Scale',
                    '-t',
                    'Ref::SegmentTime',
                    '--task',
                    'Ref::TaskFlag'
                ],
                resource_requirements = None if enableInferentia else [batch.CfnJobDefinition.ResourceRequirementProperty(type='GPU', value='1')],
                job_role_arn = jobRole.role_arn,
                linux_parameters = linux_parameters,
                volumes = [batch.CfnJobDefinition.VolumesProperty(
                    efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(file_system_id=filesystem.file_system_id, root_directory='/sr'),
                    name='efs')],
                environment= [
                    {
                        'name': 'S3_BUCKET',
                        'value': s3.bucket_name
                    },
                    {
                        'name': 'AWS_REGION',
                        'value': core.Aws.REGION
                    }
                ],
                mount_points = [batch.CfnJobDefinition.MountPointsProperty(container_path='/input', source_volume='efs')]

            ),
            retry_strategy = {'attempts': 3},
            job_definition_name = 'SuperResolution',
        )


        lambdaSG.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W40",
                },
                {
                    "id": "W5",
                }
            ]
        })
        for method in api_endpoint.methods:
            method.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W59",
                }
            ]
        })
        api_endpoint.latest_deployment.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W68",
                }
            ]
        })
        api_endpoint.deployment_stage.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W64",
                },
                {
                    "id": "W69",
                }
            ]
        })
        batchSG.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W40",
                },
                {
                    "id": "W5",
                }
            ]
        })

        filesystemSG.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W40",
                },
                {
                    "id": "W29",
                }
            ]
        })

        my_lambda.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W58",
                },
                {
                    "id": "W92",
                }
            ]
        })

        for subnet in vpc.public_subnets:
            subnet.node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W33",
                }
            ]
        })

        my_lambda.role.node.find_child('DefaultPolicy').node.default_child.add_metadata('cfn_nag',{
            "rules_to_suppress": [
                {
                    "id": "W12",
                }
            ]
        })