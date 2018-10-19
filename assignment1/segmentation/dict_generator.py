# coding=utf-8

import json
import argparse

def json_read(file_path, encoding):
    """ 读取json文件解析为dict返回.
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return json.load(f)

def dict_save(mdict, save_path="dict.json"):
    """ 将词典保存至json文件中

        Args:
          mdict: 待保存词典
          save_path: 词典将保存在该路径下
    """
    with open(save_path, 'w', encoding="utf-16") as f:
        json.dump(mdict, f)
        print("Dict is saved in -- {0}.".format(save_path))
    
def generate_dict(corpus_path, encoding='utf-16', verbose=True):
    """ 根据数据集生成词典.

        Args:
          corpus_path: 数据集路径,数据集必须采用空白分割词语.
          verbose: 是否打印进度.

        Returns:
          返回一个词典, 格式为{词: 词出现次数}.
    """
    corpus_dict = {}
    with open(corpus_path, "r", encoding=encoding) as f:
        print("Start processing.")
        count = 0
        for line in f.readlines():
            for word in line.strip().split():
                if(word in corpus_dict):
                    corpus_dict[word] += 1
                else:
                    corpus_dict[word] = 1
                    count += 1

                if(count % 10000 == 0):
                    print("Found {0} words.".format(count))

        print("Finished. Total number of words: {0}".format(count))
    
    return corpus_dict

def generate_dict_multi_source(corpus_directory, verbose=True):
    # TODO: 从千万级词表中建立词典
    pass

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus_path', default='datasets/shanxi/train.txt')
    parser.add_argument('--dict_path', default='dicts/shanxi_dict.json')
    parser.add_argument('--encoding', default='utf-16')
    args = parser.parse_args()

    corpus_dict = generate_dict(args.corpus_path, encoding=args.encoding)
    dict_save(corpus_dict, save_path=args.dict_path)

    print("Preview: (First 50 items)")
    count = 0
    for pair in corpus_dict.items():
        print(pair)
        count += 1 
        if count == 50:
            break