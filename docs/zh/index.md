AI视频超分辨率解决方案通过自研的基于深度学习的超分辨率算法从低分辨率视频中重建高分辨率视频。例如，从480p的分辨率转换成1080p的分辨率。通过该解决方案，客户能够高效地为海量视频生成高清以及超高清版本，从而充分利用已有的视频资产。本解决方案允许客户在自己的账户中转换视频数据。

本解决方案主要包括以下功能：

- 提供基于自研算法预训练好的超分辨率模型；
- 利用[Amazon Batch][Batch]提供并行处理能力；
- 利用[Amazon Inferentia][Inferentia]实现高吞吐量推理。


本实施指南介绍在Amazon Web Services（亚马逊云科技）云中部署AI视频超分辨率解决方案的架构信息和具体配置步骤。它包含指向[CloudFormation][cloudformation]模板的链接，这些模板使用亚马逊云科技在安全性和可用性方面的最佳实践来启动和配置本解决方案所需的亚马逊云科技服务。

本指南面向具有亚马逊云科技架构实践经验的IT架构师、开发人员、DevOps、数据科学家和算法工程师等专业人士以及媒体技术人员。

[Batch]: https://aws.amazon.com/batch/
[Inferentia]: https://aws.amazon.com/machine-learning/inferentia/
[cloudformation]: https://aws.amazon.com/cloudformation/