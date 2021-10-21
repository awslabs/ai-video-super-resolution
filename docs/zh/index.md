从低分辨率视频中重建高分辨率视频的过程称为超分辨率重建。亚马逊云科技数据科学家们开发了一种基于深度学习的超分辨率的算法。帮助客户以较低的成本从低分辨率视频中重建高分辨率视频 (例如，480p转换成1080p, 低清晰度转换成4K高清晰度)。此方案支持私有化部署，使您可以在自己的账户中实现视频数据的转换。

该解决方案包括以下主要功能：

- 提供基于自研算法预构建并训练好的领先的超分辨率模型
- 利用[Amazon Batch][Batch]提供并行处理能力
- 利用[Amazon Inferentia][Inferentia]提供高吞吐量的推理

本实施指南介绍了在 Amazon Web Services (亚马逊云科技) 云中部署AI视频超分辨率重建解决方案的架构注意事项和配置步骤。 它包含指向 [CloudFormation][cloudformation] 模板的链接，这些模板使用亚马逊云科技安全性和可用性最佳实践来启动和配置部署此解决方案所需的亚马逊云科技服务。

本指南面向具有亚马逊云科技架构实践经验的 IT 架构师、开发人员、DevOps、数据科学家和算法工程师等专业人士。

[Batch]: https://aws.amazon.com/cn/batch/
[Inferentia]: https://aws.amazon.com/cn/machine-learning/inferentia/
[cloudformation]: https://aws.amazon.com/cn/cloudformation/