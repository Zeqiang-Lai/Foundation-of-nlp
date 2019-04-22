import sys
sys.path.append('..')
from segmentation.model import unigram_seg
from segmentation.model import dict_generator
from hmm_tagger import HmmTagger

if __name__ == "__main__":
    seg = unigram_seg.UniGramSeg()
    mdict = dict_generator.json_read("../segmentation/model/dicts/pku_dict.json", encoding='utf-16')
    seg.set_dict(mdict)

    tagger = HmmTagger()
    tagger.load("hmm_para")

    s = ""
    print("## 这是一个词性标注Demo,输入exit退出. ##")
    print("####################################")
    while s != 'exit':
        s = input("请输入待分词句子: ")
        words = seg.cut(s)
        tags = tagger.tag(words)
        
        for word, tag in zip(words, tags):
            print(word + '/' + tag, end=' ')
        print("")