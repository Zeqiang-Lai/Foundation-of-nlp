import argparse
import os

import numpy as np
import tensorflow as tf

import net
import utilities


def predict(model, sent, vocab, tags):
    s, length = utilities.process_data(sent, vocab)

    raw = model.predict(s)[0][-length:]

    result = [np.argmax(row) for row in raw]
    result_tags = [tags[i] for i in result]

    return utilities.tags2words(sent, result_tags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument('--data_dir', default='data/pos', help='contains data files')
    parser.add_argument('--model_dir', default='model/pos', help='save models in this directory')
    parser.add_argument('--weights_file', default='crf.h5', help='weights file')

    args = parser.parse_args()

    with tf.device('/cpu:0'):
        vocab, tags = utilities.load_vocab(args.data_dir)
        model = net.BiLSTM(len(vocab), len(tags))
        model.load_weights(os.path.join(args.model_dir, args.weights_file))

        count = 0
        with open(os.path.join(args.data_dir, 'test.txt'), 'r') as fin:
            with open(os.path.join(args.data_dir, 'pred.txt'), 'w') as fout:
                lines = fin.readlines()
                for line in lines:
                    words = predict(model, line.strip(), vocab, tags)
                    fout.write(" ".join(words) + '\n')
                    count += 1
                    if count % 200 == 0:
                        print("Process sentence: {0}/{1}".format(count, len(lines)))
