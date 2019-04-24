from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, LSTM
from keras_contrib.layers import CRF

def BiLSTM(vocab_size, tag_num, embd_dim = 200, lstm_size = 100, use_crf=True):
    model = Sequential()

    model.add(Embedding(vocab_size, embd_dim, mask_zero=True))
    model.add(Bidirectional(LSTM(lstm_size, return_sequences=True)))

    crf = CRF(tag_num, sparse_target=True)
    model.add(crf)

    model.summary()
    model.compile('adam', loss=crf.loss_function, metrics=[crf.accuracy])

    return model
