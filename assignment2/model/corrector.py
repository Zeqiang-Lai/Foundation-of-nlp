# coding=utf-8
import model.utils as utils

class Corrector:
    def __init__(self, lm, shape_dict, pro_dict, word_dict, user_confusion={}):
        self.lm = lm
        self.shape_dict = shape_dict
        self.pro_dict = pro_dict
        self.word_dict = word_dict
        self.user_confusion = user_confusion

    def correct(self, sent, errors):
        """ 根据Detector识别出的错误候选进行修正,
            给出对应的修正候选.
        """
        details = []

        for error in errors:
            frag, b_idx, e_idx, err_type = error
            candidates = self._correct_single_error(sent, frag, b_idx, e_idx, err_type)
            if len(candidates) > 0:
                details.append((error, candidates))

        return details

    def _correct_single_error(self, sent, frag, b_idx, e_idx, err_type):
        """ 对单个错误进行修正, 返回候选词"""
        candidates = []

        before_sent = sent[:b_idx]
        after_sent = sent[e_idx:]

        if err_type == 'user-defined':
            candidates = self.user_confusion[frag]
            return candidates
        else:
            # 不考虑不是中文的错误
            if not utils.is_all_Chinese(frag):
                return candidates
            # 找所有候选
            all_candidates = self._find_all_candidates(frag)
            # 如果没有候选,直接返回
            if not all_candidates:
                return candidates
            # 对候选进行排序,取前5个
            candidates = sorted(all_candidates, key=lambda k: self._score(list(before_sent + k + after_sent)))[:5]
        
        if candidates[0] == frag:
            return []
        else:
            return candidates

    def _find_all_candidates(self, frag):
        # 单字的话直接用相似的字作为候选
        candidates = [frag]

        if len(frag) == 1:
            candidates.extend(self._similar_char(frag))
        elif len(frag) == 2:
            # 第一个字有错
            candidates.extend([ch + frag[1] for ch in self._similar_char(frag[0]) if ch + frag[1] in self.word_dict])
            # 第二个字有错
            candidates.extend([frag[0] + ch for ch in self._similar_char(frag[1]) if frag[0] + ch in self.word_dict])
    
        return list(candidates)

    def _similar_char(self, ch):
        shape = self.shape_dict.get(ch)
        pro = self.pro_dict.get(ch)
        if shape == None and pro == None:
            return []
        if shape == None:
            return list(pro)
        else:
            return list(shape.union(pro))

    def _score(self, sent):
        return self.lm.perplexity(' '.join(sent))