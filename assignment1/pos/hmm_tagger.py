# coding=utf-8

import utilities

class HmmTagger:
    """ 采用隐式马尔可夫模型的中文词性标注器
    """
    def __init__(self, hmm):
        self.obsv_dict = None
        self.hide_dict = None
        self.hmm = hmm

    def train(self, corpus, verbose=False):
        """ 根据数据集构建隐式马尔可夫模型.

            可能耗费较长时间,使用verbose=True查看进度.
        """
        idxed_corpus = self.__index_corpus(corpus)
        # self.hmm.setup()

    def __index_corpus(self, corpus):
        self.obsv2idx, self.idx2obsv = {}, {}
        self.hide2idx, self.idx2hide = {}, {}
        obsv_idx, hide_idx = 0, 0 

        # build dictionaries and indexing
        idxed_corpus = []
        for seq in corpus:
            idxed_seq = []
            for obsv, hide in seq:
                if obsv not in self.obsv2idx.keys():
                    self.obsv2idx[obsv] = obsv_idx
                    self.idx2obsv[obsv_idx] = obsv
                    obsv_idx += 1
                if hide not in self.hide2idx.keys():
                    self.hide2idx[hide] = hide_idx
                    self.idx2hide[hide_idx] = hide
                    hide_idx += 1
                # indexing
                idxed_seq.append((self.obsv2idx[obsv], self.hide2idx[hide]))
            idxed_corpus.append(idxed_seq)
        
        return idxed_corpus

    def tag(self, sentence):
        """ 对给定句子进行词性标注,需要提前分词.

            Args:
              sentence: 元组,长度为句子包含的词语数.

            Returns:
              一组键值对,内容为(词语, 词性).
        """
        pairs = {}
        return pairs       

if __name__ == '__main__':
    corpus = utilities.load_renmin('datasets/199801.txt')
    tagger = HmmTagger()
   