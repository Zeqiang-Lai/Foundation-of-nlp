# 中文文本纠错系统

中文文本纠错系统,能对读音相近与字形相似的错误进行检测与纠正，对于语义上的错误，纠正能力较小。

## Requirements
- python3.6
- kenlm
- numpy
- jieba

可视化还需要: 
- flask
- flask_cors

pip安装: `pip install -r requirements.txt`

## How to Start?
1. **网页方式**
- 使用远程服务器:
网址(校内访问): http://10.108.16.157:5000/proofreader

第一次访问要下载css和javascript,所以速度可能较慢,请耐心等待.

如长时间无响应,可能是服务器出错: 请联系18811031367或尝试使用本地服务器.

- 使用本地服务器:
执行以下命令启动本地服务器: 
```shell
cd assignment2
python3 app.py
```
然后打开`templates`文件夹下的`demo.html`文件。

2. **命令行方式**

```shell
cd assignment2
python3 demo.py
```

## Evaluation
```shell
cd assignment2
python3 scorer_detect.py
python3 scorer_correct.py
```

## Reference 

- Guillaume Genthial [Serving a model with Flask](https://guillaumegenthial.github.io/serving.html)
- xuh5156 [python 判断unicode字符串是汉字/数字/字母,全角/半角转换](https://blog.csdn.net/xuh5156/article/details/9111735)
- shibing624 [pycorrector](https://github.com/shibing624/pycorrector)