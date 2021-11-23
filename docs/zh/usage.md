## 工作流程

1. 用户自行上传待处理的视频文件到[Amazon S3][s3]桶。
2. 通过[Amazon API Gateway][api-gateway]发起处理请求（请求参数见下文）。
3. [Amazon Lambda][lambda]函数接收用户请求，从S3桶读取原始视频文件的元信息，计算分块数。并提交[Amazon Batch][Batch]的计算Job。
4. [Amazon Batch][Batch]从ECR拉取预构建的模型镜像，并通过ECS启动[Amazon EC2 Inf1][inf1]实例运行下面的计算Job：
    1. 视频切片。从S3桶中下载原始视频，并切分成若干个分片。目前的策略是每分钟的视频为一个分片。
    2. 超分处理。对每个分片分别运行一个Job，通过预训练的模型对每个分片视频进行超分处理。
    3. 合并操作。对每个分片的超分结果进行合并，然后将合并后的结果文件上传至S3。

## 请求参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| key | 无 | S3桶中的文件名。 |
| scale | 2 | 超分缩放倍数（单边）。可取值为2或4。 |
| task | inference | 任务类型。当设置为debug时，会将所有中间文件传到S3，以供debug使用。默认为inference，即正常推理。 |
| env | spot | 运行作业的环境。可取值为onDemand或spot。 |
| segment_time | 60 | 并行处理分片的时长（秒） |

## 请求代码示例

以下代码示例均为默认部署后的测试方式。

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

[lambda]: https://aws.amazon.com/cn/lambda/
[s3]: https://aws.amazon.com/cn/s3/
[api-gateway]: https://aws.amazon.com/cn/api-gateway/
[Batch]: https://aws.amazon.com/cn/batch/
[efs]: https://aws.amazon.com/cn/efs/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/