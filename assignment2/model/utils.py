# -*- coding: UTF-8 -*-
# 作者：xuh5156 
# 来源：CSDN 
# 原文：https://blog.csdn.net/xuh5156/article/details/9111735 

import sys

#judge a character is a Chinese Character
def is_Chinese(uchar):
	if len(uchar) != 1:
		raise TypeError('expected a character, but a string found!')
 
	if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
		return True
	else:
		return False
 
#Judge a ustr is all Chinese
def is_all_Chinese(ustr): 
	for uchar in ustr:
		if not is_Chinese(uchar):
			return False
 
	return True
 
#Judge a char is a number
def is_digit(uchar):
	if len(uchar) != 1:
		raise TypeError('expected a character, but a string found!')
 
	if uchar >= u'\u0030' and uchar<=u'\u0039':
		return True
	else:
		return False
 
#Judge a str is all num
def is_all_digit(ustr):
	for uchar in ustr:
		if not is_digit(uchar):
			return False
	
	return True
 
#Judge a char is a alphabet
def is_alpha(uchar):
	if len(uchar) != 1:
		raise TypeError('expected a character, but a string found!')
 
	if (uchar >= u'\u0041' and uchar<=u'\u005a') or \
	   (uchar >= u'\u0061' and uchar<=u'\u007a'):
		return True
	else:
		return False
 
#Judge a str is all alphabet
def is_all_alpha(ustr):
	for uchar in ustr:
		if not is_alpha(uchar):
			return False
	return True
 
#半角转全角
def B2Q(uchar):
	if len(uchar) != 1:
		raise TypeError('expected a character, but a string found!')
 
	inner_code = ord(uchar)
	if inner_code < 0x0020 or inner_code > 0x7e:      #不是半角字符就返回原来的字符
		return uchar
	if inner_code == 0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
		inner_code = 0x3000
	else:
		inner_code += 0xfee0
	
	return unichr(inner_code)
 
#全角转半角
def Q2B(uchar):
	if len(uchar) != 1:
		raise TypeError('expected a character, but a string found!')
 
	inner_code = ord(uchar)
	if inner_code == 0x3000:
		inner_code = 0x0020
	else:
		inner_code -= 0xfee0
	if inner_code < 0x0020 or inner_code > 0x7e:      #转完之后不是半角字符返回原来的字符
		return uchar
	
	return unichr(inner_code)
 
#把字符串全角转半角
def stringQ2B(ustring):
	return ''.join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()
	
# 作者：xuh5156 
# 来源：CSDN 
# 原文：https://blog.csdn.net/xuh5156/article/details/9111735 
# END

def load_word_dict(path):
    word_dict = {}
    with open(path, 'r') as f:
        for line in f:
            content = line.strip().split()
            word, freq, pos = content[0], content[1], content[2]
            word_dict[word] = (freq, pos)
    return word_dict

def load_pronunciation(path):
	m_dict = {}
	with open(path, 'r', encoding='utf-8') as f:
		first = True
		for line in f:
			if first:
				first = False
				continue
			results = line.strip().split()
			key = results[0]
			values = []
			for value in results[1:]:
				values.extend(set(list(value)))
			m_dict[key] = values
	return m_dict

def load_shape(path):
	m_dict = {}
	with open(path, 'r', encoding='utf-8') as f:
		for line in f:
			results = line.strip().split(',')
			key = results[0]
			values = set(list(results[1]))
			m_dict[key] = values
	return m_dict

if __name__ == '__main__':
	m_dict = load_pronunciation('data/pronunciation.utf8')
	
	print(list(m_dict.keys())[:1])
	print(list(m_dict.values())[:1])