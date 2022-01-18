在部署解决方案之前，建议您先查看本指南中有关架构图和区域支持等信息。然后按照下面的说明配置解决方案并将其部署到您的帐户中。

部署时间：约10分钟

## 概述
在您的亚马逊云科技账户中完成以下步骤。

- 步骤1: 启动AWS CloudFormation模板
- 步骤2: 创建超分任务

!!! warning "重要提示"

    请确保有足够的EC2配额（例如inf1实例vcpu）用于运行Batch作业。

## 步骤1: 启动AWS CloudFormation模板

此自动化AWS CloudFormation模板在亚马逊云科技中部署解决方案。

1. 登录亚马逊云科技管理控制台，选择下面的链接启动AWS CloudFormation模板。您还可以选择直接[下载模板][template]进行部署。

    - [全球区域链接][launch-template]
    - [中国区域链接][launch-template-cn]

2. 默认情况下，该模板将在您登录控制台后默认的区域启动。要在不同的亚马逊云科技区域中启动解决方案，请使用控制台导航栏中的区域选择器。
3. 在**创建堆栈**页面，验证正确的模板URL位于Amazon S3 URL文本框中，然后选择**下一步**。
4. 在**指定堆栈详细信息**页面，为您的解决方案堆栈分配一个账户内唯一且符合命名要求的名称。有关命名字符限制的信息，请参阅 `AWS Identity and Access Management 用户指南`中的[IAM 和 STS 限制][iam-limit]。
5. 在**参数**部分，查看本解决方案模板的参数并根据需要进行修改。以下为参数的默认值。

    |         参数        |    默认值    |                                                      描述                                                      |
    |:-------------------:|:------------:|:--------------------------------------------------------------------------------------------------------------|
    |  MaxvCpus | 16 | Batch作业所调用实例的最大vcpu限制，这将影响Batch所启动的节点数。默认情况下，使用的`inf1.xlarge`实例有4个vcpu。当MaxvCpus设置为16时，将启动16/4=4台实例。 |

6. 选择**下一步**。
7. 在**配置堆栈选项**页面，选择**下一步**。
8. 在**审核**页面，查看并确认设置。选中确认模板将创建Identity and Access Management (IAM)资源的框。
9. 选择**创建堆栈**以部署堆栈。

    您可以在CloudFormation控制台的状态列中查看堆栈的状态。正常情况下，大约十分钟内可以看到`CREATE_COMPLETE`状态。

10. 堆栈成功创建之后，您可以在CloudFormation的**Outputs**页签查看endpoint URL。

## 步骤2: 创建超分任务

您需要发送请求给endpoint URL以创建超分任务。请求中包含的参数如下所示：

| 参数 | 默认值 | 说明 |
|---|---|---|
| key | 无 | S3桶中的文件名。 |
| scale | 2 | 超分缩放倍数（单边）。可取值为2或4。 |
| task | inference | 任务类型。可取值为debug或inference。当设置为debug时，会将所有中间文件传到S3，以供调试使用。默认为inference，即正常推理。 |
| env | spot | 运行作业的环境。可取值为onDemand或spot。 |
| segment_time | 60 | 并行处理分片的时长（秒）。 |

以下为使用默认设置部署后使用各种语言发送请求的代码示例。

cURL

```
curl --location --request POST 'https://xxxxx.execute-api.xxxxx.amazonaws.com/prod' \
--header 'Content-Type: application/json' \
--data-raw '{
    "key": "xxxx.mp4"
}'
```

Python (requests)

```
import requests
import json

url = "https://xxxxx.execute-api.xxxxx.amazonaws.com/prod"

payload = json.dumps({
  "key": "xxxx.mp4"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Java (OkHttp)

```
OkHttpClient client = new OkHttpClient().newBuilder()
  .build();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\n    \"key\": \"xxxx.mp4\"\n}");
Request request = new Request.Builder()
  .url("https://xxxxx.execute-api.xxxxx.amazonaws.com/prod")
  .method("POST", body)
  .addHeader("Content-Type", "application/json")
  .build();
Response response = client.newCall(request).execute();
```

PHP (curl)

```
<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'https://xxxxx.execute-api.xxxxx.amazonaws.com/prod',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS =>'{
    "key": "xxxx.mp4"
}',
  CURLOPT_HTTPHEADER => array(
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;
```

[template]:https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template]: https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template-cn]: https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.cn-north-1.amazonaws.com.cn/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[iam-limit]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html