import argparse
import os

import net
import utilities
import numpy as np
import tensorflow as tf


def predict_seg(model, sent, vocab, tags):
    s, length = utilities.process_data(sent, vocab)

    raw = model.predict(s)[0][-length:]

    result = [np.argmax(row) for row in raw]
    result_tags = [tags[i] for i in result]

    return utilities.tags2words(sent, result_tags)


def run_seg_demo(args):
    with tf.device('/cpu:0'):
        vocab, tags = utilities.load_vocab(args.data_dir)
        model = net.BiLSTM(len(vocab), len(tags))
        model.load_weights(os.path.join(args.model_dir, args.weights_file))

        print("这是一个中文分词的Demo")
        predict_text = '中华人民共和国国务院总理周恩来在外交部长陈毅的陪同下，连续访问了埃塞俄比亚等非洲10国以及阿尔巴尼亚'
        print("Sample: {0}".format(predict_text))
        words = predict_seg(model, predict_text, vocab, tags)
        print("/".join(words))

        while True:
            text = input("输入待分词句: ")
            words = predict_seg(model, text, vocab, tags)
            print("/".join(words))


def predict_ner(model, sent, vocab, tags):
    s, length = utilities.process_data(sent, vocab)

    raw = model.predict(s)[0][-length:]

    results = [np.argmax(row) for row in raw]
    result_tags = [tags[i] for i in results]

    print(result_tags)
    per, loc, org = '', '', ''

    for s, t in zip(sent, result_tags):
        if t in ('b-per', 'i-per'):
            per += ' ' + s if (t == 'b-per') else s
        if t in ('b-org', 'i-org'):
            org += ' ' + s if (t == 'b-org') else s
        if t in ('b-loc', 'i-loc'):
            loc += ' ' + s if (t == 'b-loc') else s

    return ['person:' + per, 'location:' + loc, 'organzation:' + org]


def run_ner_demo(args):
    vocab, tags = utilities.load_vocab(args.data_dir)
    model = net.BiLSTM(len(vocab), len(tags))
    model.load_weights(os.path.join(args.model_dir, args.weights_file))

    print("命名实体识别Demo:")
    predict_text = '中国国家主席江泽民在北京发表讲话'
    print("Sample: {0}".format(predict_text))
    result = predict_ner(model, predict_text, vocab, tags)
    print(result)
    while True:
        text = input("输入句子: ")
        result = predict_ner(model, text, vocab, tags)
        print(result)


def run_pos_demo(args):
    raise NotImplementedError()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument('--data_dir', default='data/seg', help='contains data files')
    parser.add_argument('--model_dir', default='model/seg', help='save models in this directory')
    parser.add_argument('--weights_file', default='crf.h5', help='weights file')
    parser.add_argument('--mode', default='seg', help='demo mode')

    args = parser.parse_args()

    if args.mode not in ['seg', 'pos', 'ner']:
        raise ValueError("invalid value for mode: only accept 'seg', 'pos', 'ner'.")

    if args.mode == 'seg':
        run_seg_demo(args)
    elif args.mode == 'pos':
        run_pos_demo(args)
    else:
        run_ner_demo(args)
