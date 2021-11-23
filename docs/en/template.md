To automate deployment, this solution uses the following AWS CloudFormation templates, which you can download before deployment:

 [SuperResolutionStack.template][template]: Use this template to launch the solution and all associated components. The default configuration deploys [Amazon API Gateway][api-gateway], [Amazon Lambda][lambda], [Amazon Batch][Batch], [Amazon S3][s3], [Amazon EFS][efs] and [Amazon Batch][Batch], but you can customize the template to meet your specific needs.

[template]:https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
 [api-gateway]: https://aws.amazon.com/cn/api-gateway/
[lambda]: https://aws.amazon.com/cn/lambda/
[s3]: https://aws.amazon.com/cn/s3/
[Batch]: https://aws.amazon.com/cn/batch/
[efs]: https://aws.amazon.com/cn/efs/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/