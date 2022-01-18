Before you launch the solution, review the architecture, supported regions, and other considerations discussed in this guide. Follow the step-by-step instructions in this section to configure and deploy the solution into your account.

**Time to deploy**: Approximately 10 minutes

## Overview

Complete the following steps in your AWS account. 

- Step 1: Launch the AWS CloudFormation template
- Step 2: Create a super resolution task

!!! warning "Important"

    Make sure you have sufficient EC2 quotas (such as inf1 instances vcpu) to run Batch jobs.

## Step 1: Launch the AWS CloudFormation template

This automated AWS CloudFormation template deploys the solution in the AWS Cloud.

1. Sign in to the AWS Management Console and use one of the buttons below to launch the AWS CloudFormation template. Alternatively, you can [download the template][template] as a starting point for your own implementation.

    - [Launch solution in AWS Standard Regions][launch-template]
    - [Launch solution in AWS China Regions][launch-template-cn]
    
2. By default, the template launches in the default Region you have logged in. To launch this solution in a different AWS Region, use the Region selector in the console navigation bar.
3. On the **Create stack** page, verify that the correct template URL is shown in the **Amazon S3 URL** text box and choose **Next**.
4. On the **Specify stack details** page, assign a valid and account level unique name to your solution stack. This ensures all the resources in the stack remain under the maximum length allowed by CloudFormation. For information about naming character limitations, refer to [IAM and STS Limits][iam-limit] in the `AWS Identity and Access Management User Guide`.
5. Under **Parameters**, review the parameters for the template and modify them as necessary. This solution uses the following default values.

    |      Parameter      |    Default   |                                                      Description                                                      |
    |:-------------------:|:------------:|:--------------------------------------------------------------------------------------------------------------|
    |  MaxvCpus | 16 | The maximum vcpu limit of the instance called by the Batch job, which will affect the number of nodes that the Batch starts. By default, the instance of `inf1.xlarge` has 4 vcpus. When MaxvCpus is set to 16, 16/4=4 instances will be started. |

6. Choose **Next**.
7. On the **Configure stack options** page, choose **Next**.
8. On the **Review** page, review and confirm the settings. Check the box acknowledging that the template will create AWS Identity and Access Management (IAM) resources.
9. Choose **Create stack** to deploy the stack.
	 
    You can view the status of the stack in the AWS CloudFormation Console in the **Status** column. You should receive a CREATE_COMPLETE status in approximately 10 minutes.

10. After the stack is created successfully, you can see the endpoint URL in **Outputs** tab of AWS Cloudformation. 

## Step 2: Create a super resolution task

To create a super resolution task, you need to send a request with the following parameters to the endpoint URL.

| Parameter | Default | Description |
|---|---|---|
| key | <Requires input\> | Indicates the file name in S3.  |
| scale | 2 | Defines super resolution scaling (one-sided). The allowed values are 2 or 4. |
| task | inference | Specifies the task type. The allowed values are debug or inference. When it is set to debug, all intermediate files will be uploaded to S3 for debugging purposes.  |
| env | spot | Specifies the Job running environment. The allowed values are onDemand or spot. |

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

[template]:https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template]: https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template-cn]: https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.cn-north-1.amazonaws.com.cn/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[iam-limit]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html
[lambda]: https://aws.amazon.com/cn/lambda/
[s3]: https://aws.amazon.com/cn/s3/
[api-gateway]: https://aws.amazon.com/cn/api-gateway/
[Batch]: https://aws.amazon.com/cn/batch/
[inf1]: https://aws.amazon.com/cn/ec2/instance-types/inf1/

