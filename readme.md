# 自然语言处理基础-大作业

*Author: Zeqiang*
</br>

## 大作业1: 中文分词+词性标注

### 如何运行？

1. 下载仓库到本地
2. 在`assignment1/segmentation`目录下建立两个文件夹`datasets`和`dicts`。
    1. datasets: 存放训练数据
    2. dicts: 存放根据训练数据生成的词典

**生成词典**
例子: 
1. 将对应的训练数据放入`datasets`文件夹中,假设为`train.txt`,编码为`utf-8`, 以空白符作为分割。
2. 在命令行(shell)中键入以下命令,生成以`train.txt`为基础的词典。

```
cd assignment1/segmentation

python3 dict_generator.py --corpus_path datasets/train.txt --dict_path dicts/dict.json --encoding utf-8
```
python3 dict_generator.py --corpus_path datasets/icwb2-data/training/pku_training.utf8 --dict_path dicts/pku_dict.json --encodi
ng utf-8

**使用评测器**

　以下利用其自带的中文分词工具进行说明。在scripts目录里包含一个基于最大匹配法的中文分词器mwseg.pl，以北京大学提供的人民日报语料库为例，用法如下：
　　./mwseg.pl ../gold/pku_training_words.txt < ../testing/pku_test.txt > pku_test_seg.txt
　　其中第一个参数需提供一个词表文件pku_training_word.txt，输入为pku_test.txt，输出为pku_test_seg.txt。
　　利用score评分的命令如下：
　　./score ../gold/pku_training_words.txt ../gold/pku_test_gold.txt pku_hmm_seg.txt > score.txt
　　其中前三个参数已介绍，而score.txt则包含了详细的评分结果，不仅有总的评分结果，还包括每一句的对比结果。这里只看最后的总评结果：

### 选做: 命名实体识别

### 遇到的问题

1. 山西分词语料库的读取问题

生成字典的时候，需要根据数据集提取词语。山西数据集是用空格进行分割，但又不是一个空格，因此不能用方法1进行切割。
使用方法2，`split()`默认分割方式为任何空白，因此能够正确分割。

```python
#方法1: 
line.strip().split(' ')    # 错误
#方法2
line.strip().split()    #正确
```

2. 人民日报语料库的编码问题

通过文本编辑器查看人民日报语料库的编码时，其显示为`gb2312`，但在python中使用该编码进行读取会出现如下错误

```
UnicodeDecodeError: 'gb2312' codec can't decode byte 0xe9 in position 7524: illegal multibyte sequence
```

改为使用`gbk`编码进行解码，则能够正确读取。

3. 搜狗词典的编码问题

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

# Reference
## Survey
http://www.isnowfy.com/introduction-to-chinese-segmentation/
https://datartisan.gitbooks.io/begining-text-mining-with-python/content/第4章%20分词与词性标注/4.1%20中文分词及词性标注.html

## 分词
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
## 词性标注
https://heshenghuan.github.io/2016/03/23/词性标注调研/
HMM:
https://blog.csdn.net/rm_wang/article/details/50838243