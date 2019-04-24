import numpy as np
from collections import Counter
from keras.preprocessing.sequence import pad_sequences
import pickle
import os


def load_data(data_path, vocab, tags, maxlen=None, onehot=False):
    """ 加载数据
        Args:
            data_path: 数据路径.
            vocab: list, 词典.
            tags: list, 标记词典.
        Returns:
            x: numpy array
            y: numpy array
    """
    data = parse_data(data_path)

    if maxlen is None:
        maxlen = max(len(s) for s in data)

    w2ix = dict((w, i) for i, w in enumerate(vocab))
    tag2ix =  dict((t, i) for i, t in enumerate(tags))

    x = [[w2ix.get(w[0].lower(), 1) for w in s] for s in data]
    y = [[tag2ix.get(w[1].lower(), 1) for w in s] for s in data]

    x = pad_sequences(x, maxlen)
    y = pad_sequences(y, maxlen, value=-1)

    if onehot:
        y = np.eye(len(tags), dtype=np.float32)[y]
    else:
        y = np.expand_dims(y, 2)

    return x, y

def load_vocab(data_dir, model_dir=None):
    """ 根据训练集生成词典
        Args:
            data_dir: 数据集文件夹路径,需包含train.txt,编码utf-8.
            model_dir: 模型存储路径,生成词典将保存在该路径下.名称为config.pkl.
        Returns:
            vocab[list], tags[list]
    """
    train = parse_data(os.path.join(data_dir, 'train.txt'))

    word_counts = Counter(row[0].lower() for sample in train for row in sample)
    vocab = [w for w, f in iter(word_counts.items()) if f >= 1]

    tag_counts = Counter(row[1].lower() for sample in train for row in sample)
    tags = [w for w, f in iter(tag_counts.items()) if f >= 1]

    if model_dir is not None:
        with open(os.path.join(model_dir, 'config.pkl'), 'wb') as f:
            pickle.dump((vocab, tags), f)

    return vocab, tags

def parse_data(path):
    data = []
    sep = '\n'

    with open(path, 'r', encoding='utf-8') as f:
        for sent in f.read().strip().split(sep+sep):
            sample = []
            for word in sent.strip().split(sep):
                sample.append(word.strip().split())
            data.append(sample)

    return data

def tags2words(sentence, tags):
    words = []
    lo, hi = 0, 0

    for i in range(len(tags)):
        if tags[i] == 'E' or tags[i] == 'e':
            hi = i + 1
            words.append(sentence[lo:hi])
            lo = i+1
        elif tags[i] == 'S' or tags[i] == 's':
            words.append(sentence[lo:i + 1])
            lo = i+1

    if lo < len(tags):
        words.append(sentence[lo:len(tags)])

    assert len(sentence) == len("".join(words)), "还原失败,长度不一致\n{0}\n{1}\n{2}".format(sentence, "".join(words),
                                                                                    "".join(tags))
    return words

def process_data(data, vocab, maxlen=1000):
    word2idx = dict((w, i) for i, w in enumerate(vocab))
    x = [word2idx.get(w[0].lower(), 1) for w in data]
    length = len(x)
    x = pad_sequences([x], maxlen)  # left padding
    return x, length

if __name__ == '__main__':
    sentence = "夜间晴"
    tags = "beb"

    words = tags2words(sentence, tags)
    print(words)