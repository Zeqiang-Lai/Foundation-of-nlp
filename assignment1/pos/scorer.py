# coding=utf-8
from hmm_tagger import HmmTagger
import utilities

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
    corpus = utilities.load_renmin('datasets/199801.txt')
    tagger = HmmTagger()
    # tagger.train(corpus)
    # tagger.save("hmm_para")
    tagger.load("hmm_para")

    preds = []
    golds = []

    count = 0
    total_sent = len(corpus)
    for sent in corpus:
        words = [pair[0] for pair in sent]
        tags = [pair[1] for pair in sent]

        if len(words) <= 0: continue
        pred = tagger.tag(words)
    
        preds.append(pred)
        golds.append(tags)

        count += 1
        if count % 10 == 0:
            print("Processing: {0}/{1}".format(count, total_sent))
        if count % 100 == 0:
            print("Precision: {0}".format(precision(preds, golds)))
    
