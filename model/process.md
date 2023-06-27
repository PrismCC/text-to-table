# 模型训练使用流程

该文档会阐述基于 [shirley-wu 所建立的 `text-to-table` 框架](https://github.com/shirley-wu/text_to_table) 是如何进行训练并使用的。

如果你想直接使用训练好的 `checkpoint`，可以前往 [Google Drive](https://drive.google.com/file/d/1Gbp8cET2p4AhYbC0wAnq_v9RG23PSChh/view?usp=sharing) 进行下载。

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
$ pip install "numpy<1.24"
$ pip install nltk
$ pip install -r requirements.txt
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

## 使用

如果你想要看我是如何知道该模型是如何使用的，可以[查看 `model_usage.md`](model_usage.md)。

项目的 `model` 文件夹中，除 markdown 文件外有如下文件：
1. `get_constructed_data.py`，此文件内包含将模型产出的文件转化为结构化数据（列表）的函数；
2. `table_visualization_utils.py`，此文件提供了实现 `get_constructed_data` 的必需结构和函数，实际使用时无需理会；
3. `out.data.text`，此文件是将我们小组所选的文本经过模型转化成表格后的文本，可以用它来实验 `get_constructed_data` 的功能；
4. `text_to_table.sh`，此文件是将源文本喂给训练好的模型、产生目标表格文件的自动化脚本。

使用步骤：
1. 将 `text_to_table.sh` 移至模型根目录下，假定源文本为 `to_transform.text`，目标表格文件为 `out.data.text`，输入如下指令：
``` bash
bash text_to_table.sh to_transform.text out.data
```

执行完毕后，会在模型根目录下生成相应的中间文件和目标文件 `out.data.text`。

2. 使用 `get_constructed_data` 函数，将文本表格文件转化为列表，以便可视化操作：
``` python
from get_constructed_data import *
# ...

data = get_constructed_data("out.data.text")

# 每条数据对应一个 table
for table in data:
    # 获取此段文本的 Teams 表格
    teams_table = table.get_teams_table()

    # 获取此段文本的 Players 表格
    players_table = table.get_players_table()

    # ...
```

`out.data.text` 中一段文本与其 `teams_table`、`players_table` 示例如下：

`out.data.text` 一段文本：
``` text
Team: <NEWLINE> |  | Losses | Total points | Wins | <NEWLINE> | Hawks | 12 | 95 | 46 | <NEWLINE> | Magic | 41 | 88 | 19 | <NEWLINE> Player: <NEWLINE> |  | Assists | Points | Total rebounds | Steals | <NEWLINE> | Nikola Vucevic |  | 21 | 15 |  | <NEWLINE> | Al Horford | 4 | 17 | 13 | 2 | <NEWLINE> | Jeff Teague | 7 | 17 |  | 2 |
```

`teams_table` 结构：
``` python
[['Teams', 'Losses', 'Totalpoints', 'Wins'], ['Hawks', '12', '95', '46'], ['Magic', '41', '88', '19']]
```

`players_table` 结构：
``` python
[['Players', 'Assists', 'Points', 'Totalrebounds', 'Steals'], ['NikolaVucevic', '', '21', '15', ''], ['AlHorford', '4', '17', '13', '2'], ['JeffTeague', '7', '17', '', '2']]
```

获得到对应列表后可进一步执行下面的操作。
