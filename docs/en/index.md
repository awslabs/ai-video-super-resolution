The AI ​​Video Super Resolution solution is designed to reconstruct high-resolution videos from low-resolution videos through self-developed super resolution algorithms based on deep learning, for example, a 480p video can be converted to a 1080p video. The solution allows you to efficiently convert mass videos into high resolution and ultra-high resolution videos, so as to make full use of existing video assets. Moreover, you can use the solution to convert video data in their own accounts.  

The solution mainly includes the following features:

- Offer pre-trained super resolution models based on self-developed algorithms;
- Use [AWS Batch][Batch] to provide parallel processing capabilities;
- Use [AWS Inferentia][Inferentia] to achieve high throughput inference.

This implementation guide describes architectural considerations and configuration steps for deploying the AI ​​Video Super Resolution solution in the Amazon Web Services (AWS) cloud. It includes links to AWS [CloudFormation][cloudformation] templates that launch and configure the AWS services required to deploy this solution using AWS best practices for security and availability.

The guide is intended for IT architects, developers, DevOps, data scientists, algorithm engineers, and media technicians who have practical experience architecting in the AWS Cloud.

[Batch]: https://aws.amazon.com/batch/
[Inferentia]: https://aws.amazon.com/machine-learning/inferentia/
[cloudformation]: https://aws.amazon.com/cloudformation/