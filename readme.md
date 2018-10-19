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

**使用评测器**


### 待办事项

- [ ] mm_seg.py: 最大匹配后向算法 
- [ ] mm_seg.py: 最大匹配双向算法
- [ ] scorer.py: 正确性检查
- [ ] dict_generator.py: 千万级词典的生成

### 选做: 命名实体识别

### 遇到的问题
生成字典的时候，需要根据数据集提取词语。

山西数据集是用空格进行分割，但又不是一个空格，因此不能用方法1进行切割。

使用方法2，`split()`默认分割方式为任何空白，因此能够正确分割。

```python
#方法1: 
line.strip().split(' ')    # 错误
#方法2
line.strip().split()    #正确
```

