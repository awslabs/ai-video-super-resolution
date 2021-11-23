要卸载**AI视频超分辨率重建解决方案**，请删除CloudFormation堆栈。这将删除模板创建时的所有资源，但`superresolutionstack-superresolutionstorage`开头命名的S3存储桶和`superresolutionstack-superresolutionbucketaccessl`开头命名的存储桶除外。删除堆栈时将保留这两个存储桶，从而避免意外丢失数据。

您可以使用亚马逊云科技管理控制台或CLI删除CloudFormation堆栈，然后删除S3存储桶。

## 使用亚马逊云科技管理控制台删除堆栈

1. 登录[CloudFormation][cloudformation-console]控制台。
1. 选择本解决方案的安装父堆栈。
1. 选择**删除**。

## 使用CLI删除堆栈

1. 确定命令行在您的环境中是否可用。有关安装说明，请参阅CLI用户指南中的[CLI是什么][aws-cli]。
1. 确认CLI可用后，运行以下命令：

```bash
aws cloudformation delete-stack --stack-name <installation-stack-name> --region <aws-region>
```

## 删除Amazon S3存储桶

删除CloudFormation堆栈时，有两个S3存储桶不会被自动删除。您需要按照以下步骤手动删除这些存储桶。

1. 登录到[Amazon S3][s3-console]控制台。
1. 选择`superresolutionstack-superresolutionstorage`命名开头的存储桶。
1. 选择**空**。
1. 选择**删除**。
1. 选择`superresolutionstack-superresolutionbucketaccessl`命名开头的存储桶。
1. 选择**空**。
1. 选择**删除**。

您还可以使用CLI删除S3存储桶。请运行以下命令：

```bash
aws s3 rb s3://<bucket-name> --force
```

[cloudformation-console]: https://console.aws.amazon.com/cloudformation/home
[aws-cli]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
[s3-console]: https://console.aws.amazon.com/s3/