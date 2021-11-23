Before you launch the solution, review the architecture, supported regions, and other considerations discussed in this guide. Follow the step-by-step instructions in this section to configure and deploy the solution into your account.

**Time to deploy**: Approximately 10 minutes

## Deployment overview

Use the following steps to deploy this solution on AWS. 

- Launch the AWS CloudFormation template into your AWS account.
- Review the template parameters, and adjust them if necessary.

## Deployment steps

This automated AWS CloudFormation template deploys the solution in the AWS Cloud.

1. Sign in to the AWS Management Console and use one of the buttons below to launch the AWS CloudFormation template.
    - [Launch solution in AWS Standard Regions][launch-template]
    - [Launch solution in AWS China Regions][launch-template-cn]
    
2. The template launches in the US East (N. Virginia) Region by default. To launch this solution in a different AWS Region, use the Region selector in the console navigation bar.
3. On the **Create stack** page, verify that the correct template URL is shown in the **Amazon S3 URL** text box and choose **Next**.
4. On the **Specify stack details** page, assign a valid and account level unique name to your solution stack. This ensures all the resources in the stack remain under the maximum length allowed by CloudFormation. For information about naming character limitations, refer to [IAM and STS Limits][iam-limit] in the `AWS Identity and Access Management User Guide`.
5. Under **Parameters**, review the parameters for the template and modify them as necessary. This solution uses the following default values.

    |      Parameter      |    Default   |                                                      Description                                                      |
    |:-------------------:|:------------:|:--------------------------------------------------------------------------------------------------------------|
    |  MaxvCpus | 16 | The maximum vcpu limit of the instance called by the Batch job, which will affect the number of nodes that the Batch starts. The default instance of `inf1.xlarge` has 4 vcpus. When MaxvCpus is set to 16, 16/4=4 instances will be started. |

6. Choose **Next**.
7. On the **Configure stack options** page, choose **Next**.
8. On the **Review** page, review and confirm the settings. Check the box acknowledging that the template will create AWS Identity and Access Management (IAM) resources.
9. Choose **Create stack** to deploy the stack.

You can view the status of the stack in the AWS CloudFormation Console in the **Status** column. You should receive a CREATE_COMPLETE status in approximately 10 minutes.

[launch-template]: https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.amazonaws.com/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[launch-template-cn]: https://console.amazonaws.cn/cloudformation/home?region=cn-north-1#/stacks/new?stackName=SuperResolution&templateURL=https://aws-gcr-solutions.s3.cn-north-1.amazonaws.com.cn/Aws-gcr-ai-super-resolution/latest/SuperResolutionStack.template
[iam-limit]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html