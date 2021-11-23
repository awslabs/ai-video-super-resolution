在部署解决方案之前，建议您先查看本指南中有关架构图和区域支持等信息。然后按照下面的说明配置解决方案并将其部署到您的帐户中。

部署时间：约 10 分钟

## 部署概述
在亚马逊云科技上部署本解决方案主要包括以下过程：

- 在您的亚马逊云科技账户中启动Amazon CloudFormation模板。
- 查看模板参数，并在必要时进行调整。

## 部署步骤

此自动化Amazon CloudFormation模板在亚马逊云科技中部署解决方案。

1. 登录亚马逊云科技管理控制台，选择下面的链接启动Amazon CloudFormation模板。
    - [海外区启动模板][launch-template]
    - [中国区启动模板][launch-template-cn]

2. 默认情况下，该模板将在您登录控制台后默认的区域启动。要在不同的亚马逊云科技区域中启动解决方案，请使用控制台导航栏中的区域选择器。
3. 在**创建堆栈**页面，验证正确的模板URL位于Amazon S3 URL文本框中，然后选择**下一步**。
4. 在**指定堆栈详细信息**页面，为您的解决方案堆栈分配一个账户内唯一且符合命名要求的名称。有关命名字符限制的信息，请参阅 `Identity and Access Management 用户指南`中的[IAM 和 STS 限制][iam-limit]。
5. 在**参数**部分，查看本解决方案模板的参数并根据需要进行修改。以下为参数的默认值。

    |         参数        |    默认值    |                                                      描述                                                      |
    |:-------------------:|:------------:|:--------------------------------------------------------------------------------------------------------------|
    |  MaxvCpus | 16 | Batch作业所调用实例的最大vcpu限制，这将影响Batch所启动的节点数。默认使用的`inf1.xlarge`实例有4个vcpu。当MaxvCpus设置为16时，将启动16/4=4台实例。 |

6. 选择**下一步**。
7. 在**配置堆栈选项**页面，选择**下一步**。
8. 在**审核**页面，查看并确认设置。选中确认模板将创建Identity and Access Management (IAM)资源的框。
9. 选择**创建堆栈**以部署堆栈。

您可以在CloudFormation控制台的状态列中查看堆栈的状态。正常情况下，大约十分钟内可以看到`CREATE_COMPLETE`状态。


[launch-template]: https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template-cn]: https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.cn-north-1.amazonaws.com.cn/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[iam-limit]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html