import kenlm
from model.proofreader import CNProofReader

def precision_or_recall (answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total):
    '''求纠正错误的正确率
    '''
    correct_find = 0
    correct = 0 
    total_num = total
    
    for i in range(len(truth_find_list)):     
        for j in range(len(answer_find_list[i])):
            if answer_find_list[i][j] in truth_find_list[i]:
                correct_find += 1
                index = truth_find_list[i].index(answer_find_list[i][j])
                for correct_word in dict_list[i][answer_find_list[i][j]]:
                    if correct_word.find(truth_correct_list[i][index]) >= 0:
                        correct += 1
                        break
                
    return float(correct) / total_num 

def f1_score(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total1, total2):
    '''求纠正错误的f1值
    '''
    prec = precision_or_recall(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total1)
    rec = precision_or_recall(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total2)

    return 2.0 * prec * rec / (prec + rec)

if __name__ == '__main__':
    pf = CNProofReader()
    
    test_list = []
    with open('./test/Task2_simple.txt', 'r', encoding = 'utf-8') as f1:
        all_lines = f1.readlines()
        for line in all_lines:
            test_list.append(line[12:])


    total2 = 0
    truth_list = []
    with open('./test/Task2_Truth_simple.txt', 'r', encoding = 'utf-8') as f2:
        all_lines = f2.readlines()
        for line in all_lines:
            truth_list.append(line[7:].strip('\n').split(', '))

    truth_find_list = []
    truth_correct_list = []
    for truth in truth_list:
        temp_list1 = []
        temp_list2 = []
        for i in range(len(truth)):
            if i%2 == 0:
                temp_list1.append(truth[i])
            else:
                temp_list2.append(truth[i])
        truth_find_list.append(temp_list1)
        truth_correct_list.append(temp_list2)

    for truth_find in truth_find_list:
        total2 += len(truth_find)

    answers = []
    for sent in test_list:
        answers.append(pf.proofread(sent))

    total1 = 0
    dict_list = []
    answer_find_list = []
    answer_correct_list = []
    for answer in answers:
        temp_list1 = []
        temp_list2 = []
        temp_dict = {}
        if answer == []:
            temp_list1.append('0')
            answer_find_list.append(temp_list1)
            answer_correct_list.append(temp_list2)
            temp_dict['0'] = []
            dict_list.append(temp_dict)
            continue 
        for temp_tuple in answer:
            total1 += 1
            temp1, temp2 = temp_tuple[0][1],temp_tuple[0][2]
            for i in range(temp1 + 1, temp2 + 1):
                temp_list1.append(str(i))
                temp_dict[str(i)] = temp_tuple[1] 
            temp_list2.append(temp_tuple[1])
        answer_find_list.append(temp_list1)
        answer_correct_list.append(temp_list2)
        dict_list.append(temp_dict)

    print("Precision: {0}.".format(precision_or_recall(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total1)))
    print("Recall: {0}.".format(precision_or_recall(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total2)))
    print("F1 Score: {0}.".format(f1_score(answer_find_list, answer_correct_list, truth_find_list, truth_correct_list, dict_list, total1, total2)))
