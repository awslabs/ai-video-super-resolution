The AI ​​Video Super Resolution solution helps customers reconstruct high-resolution videos from low-resolution videos through self-developed super-resolution algorithms based on deep learning. For example, a 480p video can be converted to a 1080p video. The solution supports private deployment, and allows customers to convert video data in their own accounts.

This solution mainly includes the following features:

-Provide pre-built and trained super-resolution models based on self-developed algorithms;
-Use [Amazon Batch][Batch] to provide parallel processing capabilities;
-Use [Amazon Inferentia][Inferentia] to achieve high throughput inference.

This implementation guide describes architectural considerations and configuration steps for deploying the AI ​​Video Super Resolution solution in the Amazon Web Services (AWS) cloud. It includes links to [CloudFormation][cloudformation] templates that launches and configures the AWS services required to deploy this solution using AWS best practices for security and availability.

The guide is intended for IT architects, developers, DevOps, data scientists, algorithm engineers, and media technicians with practical experience architecting in the AWS Cloud.

[Batch]: https://aws.amazon.com/cn/batch/
[Inferentia]: https://aws.amazon.com/cn/machine-learning/inferentia/
[cloudformation]: https://aws.amazon.com/en/cloudformation/