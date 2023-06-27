# 模型分析过程

对于一个从未接触过机器学习、深度学习的人来说，不要说搞懂模型的原理了，能跑起来，知道怎么用，用出来效果怎么样，就够谢天谢地了。

因此，本文记录了如何搞懂去**使用** [`text-to-table`](https://github.com/shirley-wu/text_to_table) 的流程。

## 训练

摘自 [CSDN 上的一篇文章](https://blog.csdn.net/windmyself/article/details/108545942)，
模型训练可分为如下步骤：

1.	数据处理（即有关数据获取、数据分类、数据预处理）
2.	模型设计（网络结构设计）
3.	训练配置（训练算法）
4.	训练过程
5.	保存模型

在 `text-to-table` 项目中，其本身也包含 Dataset（数据获取与预处理）、Training（训练）。
至于其 Inference and Evaluation 步骤，乍一看为训练完成后对模型的测试。
但经过搜索，在 [CSDN 上的一篇文章](https://blog.csdn.net/weixin_43135178/article/details/117885165)指出，
“当模型参数已经求解出来，使用和部署模型，则称为推断（Inference）阶段。”
即此步骤即为使用训练好的模型步骤。
因此，在训练之后，想要知道如何使用就要着重看此阶段的代码。

在训练过程中，因为有其指令的协助，即便其中有些许地方需要调整，整体流程还算成功。
接下来，这个模型训练好之后该怎么使用，使用出来的效果是什么样的呢？

## 机理

首先我去翻阅了这个 [`text-to-table` 项目的 paper](https://arxiv.org/abs/2109.02707)。
前面三页提到了有关模型和实验，叭啦叭啦，没有背景看不懂。
第四页，他们讲解了这个模型是如何将文本进行分割的，其实就是将非结构化数据结构化。
他们将模型中不同列的数据用 $\langle s \rangle$ 分割，
不同行的数据用 $\langle n\rangle$ 分割，因此转化后表格的数据形式如下：
$$
\begin{align*}
t
=& t_1, \langle n \rangle, t_2, \langle n \rangle, \cdots, \langle n \rangle, t_{n_r} \\
=& \langle s\rangle,t_{1,1},\langle s\rangle,\cdots,\langle s\rangle,t_{1,n_c},\langle s\rangle,\langle n\rangle, \\
& \langle s\rangle,t_{2,1},\langle s\rangle,\cdots,\langle s\rangle,t_{2,n_c},\langle s\rangle,\langle n\rangle, \\
&\vdots \\
& \langle s\rangle,t_{n_r,1},\langle s\rangle,\cdots,\langle s\rangle,t_{n_r,n_c},\langle s\rangle
\end{align*}
$$

除此之外，还看到了这个项目是一个 auto-regressive（自回归）模型，和学的线性回归有类似之处，
只不过是用 $x$ 来预测 $x$，具体也不清楚，不多说了。
在此之后，这个文档就没看得懂的地方了。因此，转战项目本身。

## 代码分析

因为此项目本身的文本来源即为 rotowire，
因此在数据预处理阶段直接查看 `preprocess_rotowire.sh` 相关内容。
其开头为如下指令：
``` bash
mkdir raw
git clone https://github.com/harvardnlp/boxscore-data raw/rotowire && cd raw/rotowire && \
    tar -xf rotowire.tar.bz2 && cd ../../
```

为了一探究竟这个 `raw` 是什么类型的文件，
我去[其项目地址](https://github.com/harvardnlp/boxscore-data)下载了这份文件。
打开了可以看见里面是 json 文件。在 `preprocess_rotowire.sh` 中还有如下指令：
``` bash
# Preprocess text
PYTHONPATH=. python ./preprocess_rotowire/preprocess_text.py \
    raw/rotowire/rotowire preprocessed/rotowire/
```

可以知道，作者对这堆 json 文件进行预处理的第一步是调用 `preprocess_text.py`。
转向该文件查看，有如下代码：
``` python
for split in ['train', 'valid', 'test', ]:
    with open(os.path.join(inp_dir, f'{split}.json'))as f:
        o = json.load(f)
    with open(os.path.join(oup_dir, f'{split}.text'), 'w') as f:
        for oo in tqdm.tqdm(o, desc=split):
            f.write(detokenize(oo['summary']) + '\n')
```

具体就是将 json 文件读取，经过 `tqdm` 模块的方法，得到 text 文件并储存。
我们不知道 `tqdm` 方法究竟干了什么，但我们可以通过作者提供的预处理过的内容，查看 text 文件的内容是什么。
其内容节选为如下：
``` text
The Celtics saw great team play in their Christmas Day win, and it...
```

即利用 json 文件生成源文本。

对于 `preprocess_rotowire.sh` 文件，剩下几行可推断是利用 json 文件生成 data 文件。
作者给出的 data 文件中正是我们上面从 paper 中看到的格式，截取如下：
``` text
Team: <NEWLINE> |  | Number of team assists | <NEWLINE> | Knicks...
```

整体看来，作者在此步将 rotowire 的源文本和目标表格的生成，用来作为后面的训练材料。

作者在 `README.md` 中预处理过程提供的指令如下：
``` bash
bash scripts/preprocess.sh data/rotowire/ bart.base/
```

且下方说明如下：
``` text
then you'll have BPE-ed files under data/rotowire and binary files under data/rotowire/bins.
```

可推断此步是为了下面训练，将源 text 和 data 文件转成训练对应文件，可不管。
对下面的训练步骤同理。

值得注意的是 `train_vanilla.sh` 文件末尾有这么一行代码：
``` bash
# average checkpoints
bash scripts/eval/average_ckpt_best.sh checkpoints/
```

查看 `average_ckpt_best.sh`，其内容如下：
``` bash
d=${1:-"checkpoints/"}
n=${2:-3}
ls $d/*pt -lht
ckpts=`ls $d/checkpoint*best_*pt -lht | tail -n $n | rev | cut -d " " -f1 | rev`
echo $ckpts
python $( dirname $0 )/average_checkpoints.py --inputs $ckpts --output $d/checkpoint_average_best-${n}.pt
```

`average_checkpoints.py` 内容如下：
``` python
# ...
def main():
    # ...
    parser.add_argument('--inputs', required=True, nargs='+',
                        help='Input checkpoint file paths.')
    parser.add_argument('--output', required=True, metavar='FILE',
                        help='Write the new checkpoint containing the averaged weights to this path.')
    # ...
    new_state = average_checkpoints(args.inputs)
    with PathManager.open(args.output, "wb") as f:
        torch.save(new_state, f)
    print("Finished writing averaged checkpoint to {}".format(args.output))
# ...
```

可知训练完成后，最终的 `checkpoint` 存储在 `checkpoints/checkpoint_average_best-3.pt` 中。

正如上面所说，接下来的 Inference 步骤是重点。它指明了如何使用这个训练好的模型进行文本转化。
首先查看 `test_vanilla.sh`，其内容如下：
``` bash
DATA_PATH=$1
ckpt=${2:-"checkpoints/checkpoint_average_best-3.pt"}

export PYTHONPATH=.

fairseq-interactive ${DATA_PATH}/bins --path $ckpt --beam 5 --remove-bpe --buffer-size 1024 --max-tokens 8192 --max-len-b 1024 --user-dir src/ --task text_to_table_task  --table-max-columns 38 --unconstrained-decoding > $ckpt.test_vanilla.out < ${DATA_PATH}/test.bpe.text
bash scripts/eval/convert_fairseq_output_to_text.sh $ckpt.test_vanilla.out

for table in Team Player; do
  printf "$table table wrong format:\n"
  python scripts/eval/calc_data_wrong_format_ratio.py $ckpt.test_vanilla.out.text ${DATA_PATH}/test.data --row-header --col-header --table-name $table
  for metric in E c BS-scaled; do
    printf "Team table $metric metric:\n"
    python scripts/eval/calc_data_f_score.py $ckpt.test_vanilla.out.text ${DATA_PATH}/test.data --row-header --col-header --table-name $table --metric $metric
  done
done
```

我们仔细阅读代码，可以粗略地将其分为三部分：
1. 准备阶段
``` bash
DATA_PATH=$1
ckpt=${2:-"checkpoints/checkpoint_average_best-3.pt"}

export PYTHONPATH=.
```

这一步是为了指明使用哪个 `checkpoint`，以及一些环境设置，不重要。

2. 喂数据
``` bash
fairseq-interactive ${DATA_PATH}/bins --path $ckpt --beam 5 --remove-bpe --buffer-size 1024 --max-tokens 8192 --max-len-b 1024 --user-dir src/ --task text_to_table_task  --table-max-columns 38 --unconstrained-decoding > $ckpt.test_vanilla.out < ${DATA_PATH}/test.bpe.text
bash scripts/eval/convert_fairseq_output_to_text.sh $ckpt.test_vanilla.out
```

`convert_fairseq_output_to_text.sh` 的内容如下：
``` bash
x=$1
python $( dirname $0 )/get_hypothesis.py $x $x.hyp
python $( dirname $0 )/gpt2_decode.py $x.hyp $x.text
```

因此，这段代码的意义为：将 `bpe` 化、待喂给模型的 `xxx.bpe.text` 文件喂给模型，
并将转化为表格后的 `xxx.out` 逆 `bpe` 化，所得的 `xxx.out.text` 文件即为我们所需的表格。

我们可以看到，用来测试的样本经过 `bpe` 化（暂且这么说）后的文件，即 `test.bpe.text`，被传入。
最后输出 `test_vanilla.out` 文件，再经过 `convert_fairseq_output_to_text.sh` 
将 `bpe` 化的输出转为可供日后分析的表格文件。

3. 检验
``` bash
for table in Team Player; do
  printf "$table table wrong format:\n"
  python scripts/eval/calc_data_wrong_format_ratio.py $ckpt.test_vanilla.out.text ${DATA_PATH}/test.data --row-header --col-header --table-name $table
  for metric in E c BS-scaled; do
    printf "Team table $metric metric:\n"
    python scripts/eval/calc_data_f_score.py $ckpt.test_vanilla.out.text ${DATA_PATH}/test.data --row-header --col-header --table-name $table --metric $metric
  done
done
```

对这个部分进行合理的猜想是检验训练后的精确度，类似在课上所学的区间估计、假设检验、方差分析这种。
这种对只是想搞懂如何使用模型的人来说，自然不重要了。

同样，我们分析另一份名为 `test_constraint.sh` 的文件。可以看到，
其文件整体除对文件名进行修改和一个参数的缺失，并无区别。
此缺失的参数为 `--unconstrained-decoding`。

两文件中 `$ckpt.test_vanilla.out.text`（喂给模型后模型产出的数据）
 和 `${DATA_PATH}/test.data`（`test.text` 本应对应的表格文件）
的出现，进一步验证了我们的猜想。

## 总结

综上，我们可以知道，想要使用模型，我们假定待转换文本为 `to_transform.text`。
其步骤为：

1. 将文本 `bpe` 化（出自 `preprocess.sh`）：
``` bash
python scripts/multiprocessing_bpe_encoder.py \
    --encoder-json encoder.json \
    --vocab-bpe vocab.bpe \
    --inputs "to_transform.text" \
    --outputs "to_transform.bpe.text" \
    --workers 60 \
    --keep-empty
```
2. 给训练好的模型喂数据：
``` bash
fairseq-interactive ${DATA_PATH}/bins --path $ckpt --beam 5 --remove-bpe --buffer-size 1024 --max-tokens 8192 --max-len-b 1024 --user-dir src/ --task text_to_table_task  --table-max-columns 38 > $ckpt.out.out < ${DATA_PATH}/to_transform.bpe.text
bash scripts/eval/convert_fairseq_output_to_text.sh $ckpt.out.out
```

未使用 `--unconstrained-decoding` 参数的原因，是因为我们在实际使用时，
总想要生成一个行、列数正确的表格。

我们可以根据生成的 `out.out.text` 文件来导出表格或是绘制表格，具体就看获得数据的人如何做了。

## 附录

将以下脚本置于 `text-to-table` 根目录，命名为 `text_to_table.sh`，
使用 `bash text_to_table.sh source.text out.data`，生成的 `out.data.text` 即为 `source.text` 的表格化形式：
``` bash
input_file=${1:-"to_transform.text"}
output_file=${2:-"out.data"}
ckpt=${3:-"checkpoints/checkpoint_average_best-3.pt"}
medium_file="${input_file%.*}.bpe.${input_file##*.}"

sed -i '/^$/d' "${input_file}"

python scripts/multiprocessing_bpe_encoder.py \
    --encoder-json data/rotowire/encoder.json \
    --vocab-bpe data/rotowire/vocab.bpe \
    --inputs "${input_file}" \
    --outputs "${medium_file}" \
    --workers 60 \
    --keep-empty

fairseq-interactive data/rotowire/bins \
    --path $ckpt --beam 5 --remove-bpe --buffer-size 1024 \
    --max-tokens 8192 --max-len-b 1024 \
    --user-dir src/ --task text_to_table_task --table-max-columns 38 \
    > ${output_file} < ${medium_file}

bash scripts/eval/convert_fairseq_output_to_text.sh ${output_file}
```
