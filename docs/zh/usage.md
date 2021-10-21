## 工作流程及请求参数

### 工作流程

1. 用户自行上传待处理的视频文件到[Amazon S3][s3] 桶。
2. 通过[Amazon API Gateway][api-gateway] 发起处理请求（请求参数见下文）。
3. [Amazon Lambda][lambda] 函数接收用户请求，从s3读取原始视频文件的元信息，计算分块数。并提交[Amazon Batch][Batch]的计算Job。
4. [Amazon Batch][Batch] 从ECR拉取预构建的模型镜像，并通过ECS启动[Amazon EC2 Inf1][inf1]实例运行下面的计算Job：
    1. 视频切片。从S3桶中下载原始视频，并切分成若干个分片。目前的策略是每分钟的视频作为一个分片。
    2. 分片超分处理。对每个分片分别运行一个Job，通过预训练好的模型对每个分片视频进行超分处理。
    3. 合并操作。对每个分片的超分结果进行合并。并将合并后的结果文件上传s3

### 请求参数

| 参数名 | 说明                                                                                                   |
|--------|--------------------------------------------------------------------------------------------------------|
| key    | S3桶中的文件名                                                                                         |
| scale  | ['2', '4'] 超分缩放倍数（单边），默认为2                                                               |
| task   | [inference, debug] 当设置为debug时，会将所有中间文件传到s3，以供debug使用。默认为inference，即正常推理 |
| env    | [onDemand, spot] 指定使用按需或Spot实例来运行作业。默认为Spot                                          |

[vpc]: https://aws.amazon.com/cn/vpc/
[lambda]: https://aws.amazon.com/cn/lambda/
[s3]: https://aws.amazon.com/cn/s3/
[api-gateway]: https://aws.amazon.com/cn/api-gateway/
[Batch]: https://aws.amazon.com/cn/batch/
[efs]: https://aws.amazon.com/cn/efs/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/