# 模型训练使用流程

该文档会阐述基于 [shirley-wu 所建立的 `text-to-table` 框架](https://github.com/shirley-wu/text_to_table) 是如何进行训练并使用的。

如果你想直接使用训练好的 `checkpoint`，可以前往 [Google Drive](https://drive.google.com/file/d/1YOnFl0czWpfSHpVDWGrC9bJykkeBwDXj/view?usp=sharing) 进行下载。

## 训练

### 测试机

- Ubuntu 22.04.1 LTS
- NVIDIA GeForce RTX 3080 Ti Laptop GPU

预计磁盘空间 > 20G

### 训练步骤

1. 安装 `Python 3.8` 和相关包
``` bash
$ sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update
$ sudo apt install python3.8 python3.8-dev python3.8-venv
```
2. 创建虚拟环境并安装依赖
``` bash
$ cd path/to/text_to_table_parent_folder
$ python3.8 -m venv pyvenv
$ source pyvenv/bin/activate
$ cd text_to_table
$ pip install -r requirements.txt
$ pip install nltk
$ pip install "numpy<1.24"
```
3. 修改项目中的脚本，使脚本正常运行
``` bash
$ sed -i '12s/\.\/rotowire/\.\/preprocess_rotowire/' \
      data_preprocessing/preprocess_rotowire.sh
```
4. 对 `rotowire` 进行预处理
``` bash
$ cd data_preprocessing
$ bash preprocess_rotowire.sh
$ ls preprocessed/rotowire
$ cd .. && mkdir -p data/rotowire
$ cp data_preprocessing/preprocessed/rotowire/* \
     data/rotowire
$ bash scripts/preprocess.sh data/rotowire/ bart.base/
```
5. 开始训练
``` bash
$ bash scripts/rotowire/train_had.sh data/rotowire \
       bart.base/ 5
```
6. 评估
``` bash
$ bash scripts/rotowire/test_constraint.sh data/rotowire/
$ bash scripts/rotowire/test_vanilla.sh data/rotowire/
```

## 使用

To-do
