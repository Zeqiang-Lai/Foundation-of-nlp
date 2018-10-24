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
   