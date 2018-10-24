# coding=utf-8
from hmm import *

def precision(preds, golds):
    """ 求词性标注的准确率 """
    total_count = 0
    correct = 0
    for pred, gold in zip(preds, golds):
        for p, g in zip(pred, gold):
            if p == g:
                correct += 1
        total_count += len(pred)
    
    return float(correct) / total_count

if __name__ == '__main__':
    corpus_path = 'datasets/199801.txt'
    corpus = utilities.load_renmin(corpus_path)
    idxed_corpus, (obsv2idx, idx2obsv), (hide2idx, idx2hide) = utilities.index_corpus(corpus)
    builder = HmmMatBuilder(idxed_corpus, len(obsv2idx.keys()),len(hide2idx.keys()))
    builder.build()

    hmm = Hmm()
    hmm.setup(builder.sp_mat, builder.tp_mat, builder.ep_mat, len(obsv2idx.keys()),len(hide2idx.keys()))

    preds = []
    golds = []

    count = 0
    total_sent = len(idxed_corpus)
    for sent in idxed_corpus:
        words = [pair[0] for pair in sent]
        tags = [pair[1] for pair in sent]

        if len(words) <= 0: continue
        pred = hmm.find_hidden_state(words)
    
        preds.append(pred)
        golds.append(tags)

        count += 1
        if count % 10 == 0:
            print("Processing: {0}/{1}".format(count, total_sent))
        if count % 100 == 0:
            print("Precision: {0}".format(precision(preds, golds)))
    
