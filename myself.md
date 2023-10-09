
# error
1. 解决ValueError: Error initializing torch.distributed using env:// rendezvous:: environment variable 报错
[link](https://blog.csdn.net/weixin_57634679/article/details/129082198)
2. ERROR: Could not build wheels for mpi4py, which is required to install pyproject.toml-based projects
[link](https://blog.csdn.net/wenzhang1216/article/details/126902883)
3.  pip install bitsandbytes==0.39.0 否则报错  使用的cuda是11.6


# 调优经验

1) "num_train_epochs": 6,
    "per_device_train_batch_size": 10,
    "gradient_accumulation_steps": 2,
    "learning_rate": 1e-4,

指令调优可以, 效果未知

2) "num_train_epochs": 16,
    "per_device_train_batch_size": 10,
     "gradient_accumulation_steps": 2,
    "learning_rate": 3e-5,