import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),

    install_requires=[
        "aws-cdk.core==1.117.0",
        "aws-cdk.aws_iam==1.117.0",
        "aws-cdk.aws_ec2==1.117.0",
        "aws-cdk.aws_apigateway==1.117.0",
        "aws-cdk.aws_s3==1.117.0",
        "aws-cdk.aws_batch==1.117.0",
        "aws-cdk.aws_lambda==1.117.0",
        "aws-cdk.aws_lambda_python==1.117.0",
        "aws-cdk.aws_ecr_assets==1.117.0",
        "aws-cdk.aws_ecs==1.117.0",
        "aws-cdk.aws_ssm==1.117.0"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
