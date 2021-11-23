Deploying this solution with the default parameters builds the following environment in the AWS Cloud.

![architecture](./images/arch.png)
*Figure 1: AI Video Super Resolution architecture*

This solution deploys the Amazon CloudFormation template in your Amazon Cloud Technology account and completes the following settings.

1. Use [Amazon API Gateway][api-gateway] to implement user access interface.
1. The [Amazon Lambda][lambda] function is used to receive user requests and start the calculation job of [Amazon Batch][Batch].
1. [Amazon S3][s3] is used for persistent video storage.
1. [Amazon EFS][efs] is used for temporary storage of intermediate files during video processing.
1. [Amazon Batch][Batch] is used to pull pre-built model images from ECR, and start [Amazon EC2 Inf1][inf1] instances through ECS to run calculation jobs, and perform video slicing, sharding, and merging operations.

[Amazon VPC][vpc] is created using subnets in two Availability Zones (AZ) to achieve redundancy and ensure high availability. All resources are deployed in these two availability zones.

[vpc]: https://aws.amazon.com/en/vpc/
[api-gateway]: https://aws.amazon.com/en/api-gateway/
[lambda]: https://aws.amazon.com/en/lambda/
[s3]: https://aws.amazon.com/en/s3/
[Batch]: https://aws.amazon.com/cn/batch/
[efs]: https://aws.amazon.com/cn/efs/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/