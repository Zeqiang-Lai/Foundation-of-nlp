import kenlm
import os

from model.corrector import Corrector
from model.detector import Detector
import model.utils as utils

class CNProofReader:
    def __init__(self, user_confusion={}):
        pwd_path = os.path.abspath(os.path.dirname(__file__))

        word_dict = utils.load_word_dict(os.path.join(pwd_path, 'data/word_dict.txt'))
        pro_dict = utils.load_pronunciation(os.path.join(pwd_path, 'data/pronunciation.utf8'))
        shape_dict = utils.load_shape(os.path.join(pwd_path, 'data/shape.utf8'))
        
        lm2, lm3 = None, None
        if os.path.exists(os.path.join(pwd_path, "data/pku2.bin")):
            lm2 = kenlm.Model(os.path.join(pwd_path, "data/pku2.bin"))
        if os.path.exists(os.path.join(pwd_path, "data/pku3.bin")):
            lm3 = kenlm.Model(os.path.join(pwd_path, "data/pku3.bin"))
        
        lm = {}
        if lm2 != None:
            lm[2] = [lm2]
        if lm3 != None:
            lm[3] = [lm3]

        self.detector = Detector(lm, word_dict)
        self.corrector = Corrector(lm3, shape_dict, pro_dict, word_dict)

    def proofread(self, sent):
        """ 对输入句子进行校对,返回校对结果.
            Args:
                sent: 待校对句子.
            Returns:
                corrected_sent: 校对后句子.
                errors: 出错的地方和修改候选(排好序)
        """
        errors_candidates = self.detector.detect(sent)
        details = self.corrector.correct(sent, errors_candidates)
        return details
        # return corrected_sent, detail
