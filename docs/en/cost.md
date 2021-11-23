You are responsible for the cost of Amazon cloud technology services used when running this solution. As of November 2021, with the default settings in the us-west-2 region, for 540p to 4K super resolution tasks, the estimated cost of running the solution to process the original video is approximately $8.86 per hour.

## Cost estimate

Use the following formula for cost estimate:

```
{Video Height} * {Video Width} * {Frame Rate} * 3e-6 = The number of charging seconds corresponding to the original video per second
```

For a 540p (960*540) video, the number of charging seconds corresponding to the original video per second is 960*540*25*3e-6=38.88 seconds. Suppose the video is 30 minutes (1800 seconds) in length, which corresponds to 1800*38.88=69984 seconds=19.44 hours. So the cost is:

* OnDemand: 19.44 hours*$0.228=$4.43
* Spot: 19.44 hours*$0.0684=$1.32

**Note**

The actual cost may include charges incurred for Amazon S3, Amazon EFS, and Amazon Lambda.