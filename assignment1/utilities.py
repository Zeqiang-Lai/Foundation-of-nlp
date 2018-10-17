import json

def json_read(file_path, encoding):
    """ 读取json文件解析为dict返回.
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return json.load(f)

def generate_dict(corpus_path, save_path="dict.json", verbose=True):
    """ 根据数据集生成词典,并保持到本地文件中.

        Args:
          corpus_path: 数据集路径,数据集必须为utf-16编码,且采用
                       空白分割词语.
          save_path: 词典将保存在该路径下
          verbose: 是否打印进度.

        Returns:
          返回一个词典, 格式为{词: 词出现次数}, 采用utf-16编码.
    """

    corpus_dict = {}
    with open(corpus_path, "r", encoding="utf-16") as f:
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

    with open(save_path, 'w', encoding="utf-16") as f:
        json.dump(corpus_dict, f)
        print("Dict is saved in -- {0}.".format(save_path))
    
    return corpus_dict

if __name__ == '__main__':
    corpus_dict = generate_dict("datasets/shanxi/train.txt")
    
    print("Preview: (First 50 items)")
    count = 0
    for pair in corpus_dict.items():
        print(pair)
        count += 1 
        if count == 50:
            break