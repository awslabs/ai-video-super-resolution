要卸载**AI视频超分辨率重建解决方案**，请删除 CloudFormation 堆栈。这将删除模板创建的所有资源，但 `superresolutionstack-superresolutionstorage` 开头命名的 S3 存储桶和 `superresolutionstack-superresolutionbucketaccessl` 开头命名的存储桶除外。删除解决方案堆栈时将保留这两个存储桶，以帮助防止意外丢失数据。 您可以使用亚马逊云科技管理控制台或 CLI 清空，然后在删除 CloudFormation 堆栈后删除这些 S3 存储桶。

### 使用亚马逊云科技管理控制台

1. 登录 [CloudFormation][cloudformation-console] 控制台。
1. 选择此解决方案的安装父堆栈。
1. 选择**删除**。

### 使用 CLI

确定命令行在您的环境中是否可用。有关安装说明，请参阅CLI 用户指南中的[CLI是什么][aws-cli]。确认 CLI 可用后，运行以下命令。

```bash
aws cloudformation delete-stack --stack-name <installation-stack-name> --region <aws-region>
```

### 删除 Amazon S3 存储桶

基于深度学习图神经网络的实时反欺诈解决方案创建两个不会自动删除的 S3 存储桶。 要删除这些存储桶，请使用以下步骤。

1. 登录到 [Amazon S3][s3-console] 控制台。
1. 选择 `superresolutionstack-superresolutionstorage` 命名开头的存储桶。
1. 选择**空**。
1. 选择**删除**。
1. 选择 `superresolutionstack-superresolutionbucketaccessl` 命名开头的存储桶。
1. 选择**空**。
1. 选择**删除**。

要使用 CLI 删除 S3 存储桶，请运行以下命令：

```bash
aws s3 rb s3://<bucket-name> --force
```

[cloudformation-console]: https://console.aws.amazon.com/cloudformation/home
[aws-cli]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
[s3-console]: https://console.aws.amazon.com/s3/