## Workflow

1. Upload the original video file to the [Amazon S3][s3] bucket.
2. Initiate a processing request through [Amazon API Gateway][api-gateway] (see below for request parameters).
3. The [Amazon Lambda][lambda] function receives user requests, reads the metadata of the original video file from the S3 bucket, and calculates the number of blocks, then submits the calculation job of [Amazon Batch][Batch].
4. [Amazon Batch][Batch] pulls the pre-built model image from ECR, and launches the [Amazon EC2 Inf1][inf1] instance through ECS to run the following calculation Job:
     1. Video slicing: download the original video from the S3 bucket and split it into several slices. Currently, every minute of the video is considered as one slice.
     2. Super-resolution processing: run a Job for each slice, and perform super resolution on each slice of the video based on the pre-trained model.
     3. Merging: the super resolution results are merged, and then the merged result file is uploaded to S3.

## Request parameters

| Parameter | Default | Description |
|---|---|---|
| key | \<Requires input\> | Indicates the file name in S3.  |
| scale | 2 | Defines super resolution scaling (one-sided). The allowed values are 2 or 4. |
| task | inference | Specifies the task type. The allowed values are debug or inference. When it is set to debug, all intermediate files will be uploaded to S3 for debugging purposes.  |
| env | spot | Specifies the Job running environment. The allowed values are onDemand or spot. |

## Example of request code

The following example shows the request code after the deployment with default configurations.

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
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/