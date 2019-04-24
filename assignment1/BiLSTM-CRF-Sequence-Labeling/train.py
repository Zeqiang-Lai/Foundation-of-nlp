import argparse
import os

import net
import utilities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training a model')
    parser.add_argument('--data_dir', default='data/ner2', help='contains data files')
    parser.add_argument('--model_dir', default='model/ner2', help='save models in this directory')
    parser.add_argument('--weights_file', default='crf.h5', help='weights file')

    parser.add_argument('--epochs', type=int, default=5, help='training epochs')
    parser.add_argument('--batch_size', type=int, default=512, help='training batch_size')

    args = parser.parse_args()

    vocab, tags = utilities.load_vocab(args.data_dir, args.model_dir)

    train_x, train_y = utilities.load_data(os.path.join(args.data_dir, 'train.txt'), vocab, tags)
    valid_x, valid_y = utilities.load_data(os.path.join(args.data_dir, 'valid.txt'), vocab, tags)

    model = net.BiLSTM(len(vocab), len(tags))

    # model.load_weights(os.path.join(args.model_dir, args.weights_file))

    model.fit(train_x, train_y,
              batch_size=args.batch_size,
              epochs=args.epochs,
              validation_data=[valid_x, valid_y])

    model.save(os.path.join(args.model_dir, args.weights_file))
