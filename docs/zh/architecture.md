下图展示的是使用默认参数部署本解决方案在亚马逊云科技中构建的环境。

![architecture](./images/arch.png)
      
图：方案架构

本解决方案在您的亚马逊云科技账户中部署Amazon CloudFormation模板并完成以下设置。

1. 向[Amazon S3][s3]上传待处理的视频文件。
1. 向[Amazon API Gateway][api-gateway]实现的接口发起请求。
1. [Amazon Lambda][lambda]函数用来接收请求，并读取视频元信息。
1. [Amazon Lambda][lambda]启动[Amazon Batch][Batch]的计算Job。
1. [Amazon Batch][Batch]从ECR拉取预构建的模型镜像，并通过ECS启动[Amazon EC2 Inf1][inf1]实例运行计算Job，进行视频切片、分片处理及合并操作。
1. [Amazon EFS][efs]用于视频处理时中间文件的临时存储。
1. [Amazon Batch][Batch]将处理后的分片视频合并后写入[Amazon S3][s3]。

[Amazon VPC][vpc]使用两个可用区 (AZ) 中的子网创建，从而实现冗余，保证高可用性。所有资源均部署在这两个可用区中。

[vpc]: https://aws.amazon.com/cn/vpc/
[api-gateway]: https://aws.amazon.com/cn/api-gateway/
[lambda]: https://aws.amazon.com/cn/lambda/
[s3]: https://aws.amazon.com/cn/s3/
[Batch]: https://aws.amazon.com/cn/batch/
[efs]: https://aws.amazon.com/cn/efs/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/