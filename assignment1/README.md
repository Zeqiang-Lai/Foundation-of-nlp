# 大作业1: 分词+词性标注

Author: 赖泽强, 刘文卓, 钱泽, 谭超

> 命名实体识别在BiLSTM-CRF模型中

## Requirement

- python3
- numpy

## 如何运行？

推荐使用Linux/macos进行测试

###分词

**第一步：**下载测试数据 `test_data` ,并放入对应文件夹中 

下载链接: https://share.weiyun.com/5MSjuWW

**第二步：** 下载`隐式马尔可夫预训练模型` ，并放入对应文件夹(`model/hmm_para`和`model/sx_hmm_para`)中

下载链接：https://share.weiyun.com/5T9ijOK

**第三步：** 使用以下命令进行评测

- 确保路径正确

```shell
cd segmentation
```

- 分词, 分词结果保存在 `test_data/[dataset]/[model]_seg.txt` , 编码为`gb18030`。

```shell
python3 seg.py --segger [unigram|mm|hmm] --dataset [shanxi|pku]
# segger可以选择三种模型 dataset可以选择两种数据集
```

- 评测

```shell
方法1,pku数据集推荐使用方法2
python3 scorer.py --pred_path [] --gold_path [] --pred_encoding [] --gold_encoding []
# 例如评测shanxi的mm_seg.txt
# python3 scorer.py --pred_path test_data/shanxi/mm_seg.txt --gold_path test_data/shanxi/gold.txt --pred_encoding gb18030 --gold_encoding utf-16

方法2,适用于pku数据集
# score为perl脚本,windows下需安装对应程序才能执行
cd test_data/pku
./score pku_training_words.txt gold.txt hmm_seg.txt > score.txt
# 将hmm_seg.txt替换为你想评测的文件,需要为gb18030编码.
```

**运行demo**

```shell
python3 demo.py
```



###词性标注 

**第一步：**下载人名日报数据集 ,并放入对应文件夹中 

下载链接: https://share.weiyun.com/5WmQkiA

**第二步：** 下载`隐式马尔可夫预训练模型`, 并放入对应文件夹

下载链接：https://share.weiyun.com/5zJzFr2

**第二步： ** 使用以下命令进行评测：

```shell
cd pos
python3 scorer.py
```



**运行demo**

```shell
python3 demo.py
```

## 如何训练？

### 分词

```shell
 # 最大匹配和Unigram
 # 训练词典完即可
 cd segmentation/model
 python3 dict_generator.py --corpus_path [] --dict_path [] --encoding []
 
 # HMM
 # 训练不同数据集,需修改hmm_seg.py中的部分代码
 cd segmentation
 python3 hmm_seg.py
```

### 词性标注

```shell
cd pos
python3 hmm_tagger.py
```

## 目录结构

```shell
.
├── README.md
├── README.pdf
├── pos
│   ├── README.md
│   ├── datasets
│   ├── demo.py
│   ├── hmm_para
│   ├── hmm_tagger.py
│   ├── scorer.py
│   └── utilities.py
├── segmentation
│   ├── demo.py
│   ├── model
│   │   ├── __init__.py
│   │   ├── dict_generator.py
│   │   ├── dicts
│   │   │   ├── pku_dict.json
│   │   │   └── shanxi_dict.json
│   │   ├── hmm_para
│   │   ├── hmm_seg.py
│   │   ├── mm_seg.py
│   │   ├── sx_hmm_para
│   │   └── unigram_seg.py
│   ├── scorer.py
│   ├── seg.py
│   └── test_data
└── shared
    ├── hmm.py
    └── smooths.py
```

## 遇到的问题

1. **山西分词语料库的读取问题**

生成字典的时候，需要根据数据集提取词语。山西数据集是用空格进行分割，但又不是一个空格，因此不能用方法1进行切割。
使用方法2，`split()`默认分割方式为任何空白，因此能够正确分割。

```python
#方法1: 
line.strip().split(' ')    # 错误
#方法2
line.strip().split()    #正确
```

2. **人民日报语料库的编码问题**

通过文本编辑器查看人民日报语料库的编码时，其显示为`gb2312`，但在python中使用该编码进行读取会出现如下错误

```
UnicodeDecodeError: 'gb2312' codec can't decode byte 0xe9 in position 7524: illegal multibyte sequence
```

改为使用`gbk`编码进行解码，则能够正确读取。

3. **搜狗词典的编码问题**

通过文本编辑器查看`SogouLabDic.dic`的编码时，其显示为`gb2312`,但在python中使用该编码进行读取会出现如下错误
```
UnicodeDecodeError: 'gb2312' codec can't decode byte 0xb2 in position 6549: illegal multibyte sequence
```
改用`gbk`进行读取仍然报错
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xfa in position 799: illegal multibyte sequence
```
通过一阵google,终于在知乎上找到了这个问题的[解决方法](https://www.zhihu.com/question/36368902)。
使用gbk的超集gb18030尝试,解码成功！

## Reference

### Survey

http://www.isnowfy.com/introduction-to-chinese-segmentation/
https://datartisan.gitbooks.io/begining-text-mining-with-python/content/第4章%20分词与词性标注/4.1%20中文分词及词性标注.html

### 分词
https://applenob.github.io/statistics_seg.html
http://www.isnowfy.com/python-chinese-segmentation/
http://www.isnowfy.com/introduction-to-chinese-segmentation/
http://www.isnowfy.com/analysis-of-chinese-segmentaion/

最大匹配法分词:
双向: https://blog.csdn.net/PKU_ZZY/article/details/54730972

HMM分词:
https://blog.csdn.net/PKU_ZZY/article/details/56479627

jieba:
http://www.cnblogs.com/zhbzz2007/p/6092313.html

uni-gram:
http://www.isnowfy.com/python-chinese-segmentation/
https://applenob.github.io/statistics_seg.html

感知机: 
https://github.com/hankcs/HanLP/wiki/结构化感知机标注框架
### 词性标注
https://heshenghuan.github.io/2016/03/23/词性标注调研/
HMM:
https://blog.csdn.net/rm_wang/article/details/50838243