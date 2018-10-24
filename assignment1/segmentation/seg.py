from model import dict_generator 
from model.mm_seg import MMSeg
from model.unigram_seg import UniGramSeg
import timeit

if __name__ == '__main__':

    # seg = MMSeg()
    seg = UniGramSeg()
    # mdict = dict_generator.load_sogou_dict('datasets/SogouLabDic.dic')
    mdict = dict_generator.json_read("model/dicts/pku_dict.json", encoding='utf-16')
    seg.set_dict(mdict)

    pred = []
    ch_count = 0
    time_cost = 0
    test_path = "model/datasets/icwb2-data/testing/pku_test.utf8"
    with open(test_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        start = timeit.default_timer()
        for sent in lines:
            pred.append(seg.cut(sent))
            ch_count += len(sent)
        end = timeit.default_timer()
        time_cost = end - start
    
    print("Total number of characters: {0}.".format(ch_count))
    print("Time cost: {0}s.".format(time_cost))
    print("Processed characters per second: {0}.".format(int(ch_count / time_cost)) )

    # 保存分词结果
    save_path = "pku_seg/pku_uni_seg.txt"
    with open(save_path, "w", encoding='gb18030') as f:
        for words in pred:
            s = " ".join(words)
            s.encode('gb18030')
            f.write(s)

    print("Segmentation result is saved in {0}.".format(save_path))