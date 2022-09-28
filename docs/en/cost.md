You are responsible for the cost of using AWS's services used while running this solution. As of September 2022, in the AWS Oregon Region (us-west-2), for 540p to 4K super resolution tasks, the estimated cost of running the solution to process the original video is approximately $8.86 per hour.

## Formula for cost estimate

The cost mainly depends on Amazon EC2 launched by AWS Batch, and the actual cost may include charges incurred for Amazon S3, Amazon EFS, and AWS Lambda.

Use the following formula for cost estimate:

```
{Video Height} * {Video Width} * {Frame Rate} * 3e-6 = The number of charging seconds corresponding to the original video per second
```

## Example 1

In AWS Oregon Region (us-west-2), for a 540p (960\*540) video (~200MB), the number of charging seconds corresponding to the original video per second is 960\*540\*25\*3e-6=38.88 seconds. Suppose the video is 30 minutes (1800 seconds) in length, which corresponds to 1800\*38.88=69984 seconds=19.44 hours. So the cost is:

* OnDemand: 19.44 \*$0.228 = $4.43
* Spot: 19.44 \*$0.0684 = $1.32

| AWS service | Dimensions | Cost |
|---|---|---|
| Amazon EC2 | Launched by AWS batch, 0.228 per hour (inf1.xlarge) | $4.43 |
| Amazon S3 | 2 GET requests + 1 PUT request, 200MB+600MB (Approximate), 1 month | $0.023 |
| AWS Lambda | 1 request (~5s, 4096MB Memory) | $0.0007 |
| Amazon EFS | 200MB, 19.44 hours | $0.0015 |
|  | | TOTAL: $4.4552 |

## Example 2

In AWS China (Ningxia) Region operated by NWCD (cn-northwest-1), for a 1080p (1920\*1080) video (~1000MB), the number of charging seconds corresponding to the original video per second is 1920\*1080\*25\*3e-6=155.52 seconds. Suppose the video is 30 minutes (1800 seconds) in length, which corresponds to 1800\*155.52=279936 seconds=77.76 hours. So the cost is:

* OnDemand: 77.76 \*¥2.601 = ¥202.25
* Spot: 77.76 \*¥0.4839 = ¥37.62

| AWS service | Dimensions | Cost |
|---|---|---|
| Amazon EC2 | Launched by AWS batch, 2.601 per hour (inf1.xlarge) | ¥202.25 |
| Amazon S3 | 2 GET requests + 1 PUT request, 1000MB+4000MB (Approximate), 1 month | ¥0.877 |
| AWS Lambda | 1 request (~5s, 4096MB Memory) | ¥0.002 |
| Amazon EFS | 1000MB, 77.76 hours | ¥0.228 |
|  | | TOTAL: ¥203.357 |


