To uninstall the **AI Video Super Resolution** solution, you must delete the AWS CloudFormation stack. You can use the AWS Management Console or the AWS Command Line Interface (AWS CLI) to delete the CloudFormation stack.


!!! warning "Important"
    
    Because two S3 buckets starting with `superresolutionstack-superresolutionstorage` and `superresolutionstack-superresolutionbucketaccessl` will persist while you delete the stack, make sure to empty the two buckets before deleting the AWS CloudFormation stack.


## Uninstall the stack using the AWS Management Console
1. Sign in to the [AWS CloudFormation][cloudformation-console] console.
1. Select this solution’s installation parent stack.
1. Choose **Delete**.

## Uninstall the stack using AWS Command Line Interface

Determine whether the AWS Command Line Interface (AWS CLI) is available in your environment. For installation instructions, refer to [What Is the AWS Command Line Interface][aws-cli] in the *AWS CLI User Guide*. After confirming that the AWS CLI is available, run the following command.

```bash
aws cloudformation delete-stack --stack-name <installation-stack-name> --region <aws-region>
```

## Deleting the Amazon S3 buckets

The solution creates two S3 buckets that are not automatically deleted. You can choose to follow the following steps to delete these buckets manually.

1. Sign in to the [Amazon S3][s3-console] console.
1. Select the bucket name starting with `superresolutionstack-superresolutionstorage`.
1. Choose **Empty**.
1. Choose **Delete**.
1. Select the bucket name starting with `superresolutionstack-superresolutionbucketaccessl`.
1. Choose **Empty**.
1. Choose **Delete**.

To delete the S3 bucket using AWS CLI, run the following command:

```bash
aws s3 rb s3://<bucket-name> --force
```

[cloudformation-console]: https://console.aws.amazon.com/cloudformation/home
[aws-cli]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
[s3-console]: https://console.aws.amazon.com/s3/