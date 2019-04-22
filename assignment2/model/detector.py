# coding=utf-8
import kenlm
import jieba
import numpy as np

import model.utils as utils

class Detector:
    def __init__(self, lm, word_dict, user_confusion={}):
        """ Args:
                lm: [dict],语言模型字典,keys={'',''}
                word_dict: [dict],词典 {词: 出现频率}
                user_confusion: [dict], 用户自定义混淆集, {混淆词: 正确词}
        """
        self.lm = lm
        self.word_dict = word_dict
        self.user_confusion = user_confusion
        self.errors = []

    def detect(self, sent):
        """ 识别给定句子中可能出现的错误,
            返回一个列表[(错误内容,开始idx,结束idx,错误类型)]
            
            错误类型有
            1. user-defined: 由自定义混淆集识别的错误
            2. pro: 读音相似
            3. shape: 字形相似
        """
        sent = sent.strip()
        self.errors = []
        # 分词
        # words, pos = self._tokenize(sent)
        words = self._tokenize(sent)

        # 判断是否含有自定义混淆集中的错误, 若有则加入错误候选集合
        for confuse in self.user_confusion.keys():
            idx = sent.find(confuse)
            if idx > -1:
                error = [confuse, idx, idx + len(confuse), 'user-defined']
                if self._valid(error):
                    self.errors.append(error)

        # 词粒度的错误识别: 分词后的未登录词的加入错误候选集合
        self._detect_word_level(words)

        # 字粒度的错误识别: 使用语言模型
        self._detect_char_level(sent)

        return sorted(self.errors, key=lambda k: k[1], reverse=False)

    def _detect_word_level(self, words):
        """ 词粒度的错误识别: 分词后的未登录词的加入错误候选集合 """
        for word, b_idx, e_idx in words:
            # 不考虑空格
            if len(word.strip()) == 0:
                continue
            # 不考虑数字和英文
            if utils.is_all_digit(word.lower()) or utils.is_all_alpha(word.lower()):
                continue
            # 不考虑标点符号
            PUNCTUATION_LIST = "。，,、？：；{}[]【】“‘’”《》/!！%……（）<>@#$~^￥%&*\"\'=+-"
            if word in PUNCTUATION_LIST:
                continue
                
            if word in self.word_dict.keys():
                continue
            error = [word, b_idx, e_idx, 'word']
            if self._valid(error):
                    self.errors.append(error)

    def _detect_char_level(self, sent):
        """ 字粒度的错误识别: 使用语言模型 """
        # ---- 先给每个字打分 ---- #
        scores = [0] * len(sent)
        # 不同级别的ngram
        for n in self.lm.keys():
            if len(sent)-n+1 <= 0:
                continue
            tmp_scores = []
            for i in range(len(sent)-n+1):
                # 前后向ngram
                ans = 0
                for model in self.lm[n]:
                    ans += self._n_gram_score(sent[i:i+n], model)
                tmp_scores.append(ans / len(self.lm[n]))
            for _ in range(n-1):
                tmp_scores.insert(0, tmp_scores[0])
                tmp_scores.append(tmp_scores[-1])

            for i in range(len(sent)):
                scores[i] += sum(tmp_scores[i:i+n]) / n
        
        scores = [score / len(self.lm.keys()) for score in scores]

        # ---- 再找分数异常的作为错误候选 ---- #
        for idx in self._find_char_candidates(scores):
            error = [sent[idx], int(idx), int(idx+1), 'char']
            if self._valid(error):
                self.errors.append(error)
        
    def _find_char_candidates(self, scores, threshold=15):
        """ 找分数异常的作为错误候选,使用绝对中位差
            Args:
                scores: 每个字的分数
                threshold: 阈值越小，得到错别字候选越多
        """
        scores = np.array(scores)
        scores = scores[:, None]
        # 取中位数
        median = np.median(scores, axis=0)  
        # 计算每个分数对中位数的方差
        dev_median = np.sqrt(np.sum((scores - median) ** 2, axis=-1))  
        # 计算绝对中位差
        med_abs_deviation = np.median(dev_median)
        if med_abs_deviation == 0:
            return []
        # 计算偏离比例
        y_score = dev_median / med_abs_deviation
      
        scores = scores.flatten()
     
        candidates_indices = np.where((y_score > threshold) & (scores < median))

        return list(candidates_indices[0])

    def _n_gram_score(self, frag, model):
        return model.score(" ".join(frag), bos=False, eos=False)

    def _tokenize(self, sent):
        """ Hanlp分词与词性标注并返回每个词在原句中的位置
            格式: [(词/词性, 开始位置, 结束位置),...]
        """
        # words, pos = [], []
        # for term in HanLP.segment(sent):
        #     words.append(term.word)
        #     pos.append(str(term.nature))
        
        # tmp_words, temp_pos = [], []
        # for word, p in zip(words, pos):
        #     b_idx = sent.find(word)
        #     e_idx = b_idx + len(word)
        #     tmp_words.append((word, b_idx, e_idx))
        #     temp_pos.append((p, b_idx, e_idx))
        
        # return tmp_words, temp_pos

        return list(jieba.tokenize(sent))

    def _valid(self, error):
        """ 判断一个错误是否可以加入错误集中.
            标准: 错误不重复重叠
        """
        if error in self.errors:
            return False
        
        word_idx, b_idx, e_idx = 0, 1, 2
        for tmp_error in self.errors:
            if error[b_idx] >= tmp_error[b_idx] and error[e_idx] <= tmp_error[e_idx]:
                return False

        return True