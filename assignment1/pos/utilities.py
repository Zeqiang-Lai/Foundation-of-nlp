# coding=utf-8

def load_renmin(ds_path, encoding='gbk'):
    """ 加载人民日报-分词与词性标注数据集
    
        Returns:
          返回一个列表,列表内容为一系列词典,每个词典包含一个句子中的
          所有词语及其词性. 示例:[{'开始':'v',...},{...},...]
    """
    corpus = []
    with open(ds_path, 'r', encoding=encoding) as f:
        for line in f.readlines():
            sent = []
            for cb in line.strip().split():
                pair = cb.strip().split('/')
                sent.append((pair[0], pair[1]))
            corpus.append(sent)

    return corpus

if __name__ == '__main__':
    corpus = load_renmin('datasets/199801.txt')
    print(corpus[:3])