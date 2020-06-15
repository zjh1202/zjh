# coding=utf-8
import re
import sys
import jieba.posseg as pseg
from django.shortcuts import render, HttpResponse
import jieba
import math
from pyhanlp import HanLP
from pathlib import Path
from collections import Counter
import numpy as np

#停用词库
def stop_words(cut_word):
    stop = []# 创建停用词列表（一行数组）
    standard_stop = []#创建存放列表（多行数组，一行一个）
    after_text = []
    file_stop = r'E:\python\练习\chinese_dictionary-master\stop.txt'  # 停用词表地址
    with open(file_stop, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()  # lines是list类型
        for line in lines:
            lline = line.strip()  # 去掉停用字符放到lline中
            stop.append(lline)  # 将其放入stop列表中
    # stop 的元素是一行一行的 句子,需要进行转化为一个词一行,即下面:
    for i in range(0, len(stop)):#开始循环，循环0到停用词数量次数
        for word in stop[i].split():
            standard_stop.append(word)#一行一次加入到数组中
    #判断分词是否存在standard_stop停用数组中的停用词
    for line in cut_word:
        lline = line.split()
        for i in lline:
            # 将不存在的加入到after_text数组中
            if i not in standard_stop:
                after_text.append(i)
    return after_text#返回停用词

# 获取标准答案
# def teacher_word():
#     words = "物流系统是由物流作业系统和支持物流信息流动的物流信息系统"
#     return words

#切分标准答案
def cut_words(words):
    # words = teacher_word()
    # words = request.POST.get('words')
    # 分词
    s1_cut = [i for i in jieba.cut(words, cut_all=True) if i != '']  # 分割标准答案
    #s1_cut = stop_words(cut)
    return s1_cut

# 获取关键字
# def keyword():
#     keyword = "物流作业系统、物流信息流动、物流信息系统"  # 得分词：必须回答
#     return keyword

# 获取关键字分词
def key(key):
    # key = keyword()  # 得分词：必须回答
    # 分词
    s3_cut = [i for i in jieba.cut(key, cut_all=True) if i != '']
    return s3_cut

# 获取考生答案
# def answer_word():
#     answer_word = "物流作业和物流信息"
#     return answer_word

# 获取考生答案分词
def answer(answer_word):
    # answer = answer_word()  # "物流管理、物流采集、物流统计"
    # 分词
    s2_cut = [i for i in jieba.cut(answer_word, cut_all=True) if i != '']  # 分割考生答案
    #s2_cut = stop_words(cut)
    return s2_cut

#查询词频最高的词
def high_word(cut_word):
    document = stop_words(cut_word)
    word_counts = Counter(document)
    #计算一个最高次数的词并放入high中
    high = [x[0] for x in word_counts.most_common(1)]
    return high

#调用近义词库，判断是否存在近义词，若存在则可以替换(若存在多个则无法判断)
def synonym(s1_cut,answer_words):
    # string1 = answer_word()
    # string2 = cut_words()
    string1 = answer_words
    string2 = s1_cut
    combine_dict = []
    # synonymWords.txt是同义词表，每行是一系列同义词，用空格分割
    for line in open(
            "E:\python\练习\chinese_dictionary-master\dict_synonym.txt",
            "r", encoding='gbk'):
        seperate_word = line.strip('\ufeff').split()
        combine_dict.append(seperate_word)
    seg_list = jieba.cut(string1, cut_all=False)
    f = "/".join(seg_list).encode("utf-8")
    f = f.decode("utf-8")
    print(f)
    #找考生答案近义词
    for word in f.split('/'):
        for i in range(len(combine_dict)):
            for j in range(len(combine_dict[i])):
                if word == combine_dict[i][j]:
                    syn1 = combine_dict[i]
    #找标准答案近义词
    for word in string2:
        for i in range(len(combine_dict)):
            for j in range(len(combine_dict[i])):
                if word == combine_dict[i][j]:
                    syn2 = combine_dict[i]
    a = [x for x in syn1 if x in syn2]
    return a

#调用反义词库，判断否定反义词
def antonym(answer_words):
    string1 = answer_words
    combine_dict = []
    # synonymWords.txt是同义词表，每行是一系列同义词，用空格分割
    for line in open(
            "E:\python\练习\chinese_dictionary-master\dict_antonym.txt",
            "r", encoding='utf-8'):
        seperate_word = line.strip('\ufeff').split()
        combine_dict.append(seperate_word)

    sentence = ""
    row = len(combine_dict)
    col = len(seperate_word)
    seg_list = jieba.cut(string1, cut_all=False)
    f = "/".join(seg_list).encode("utf-8")
    f = f.decode("utf-8")
    for word in f.split('/'):
        for i in range(row):
            for j in range(col):
                if word == combine_dict[i][j]:
                    ant = combine_dict[i][1 - j]
                    bool = word
    cut = [i for i in jieba.cut(string1, cut_all=False) if i != '']
    print(cut)
    # 判断考生答案是否存在否定
    deny = deny_word()
    for i in range(len(cut)):
        for j in range(len(deny)):
            if cut[i] == deny[j] and cut[i + 1] == bool:
                replace = cut[i] + word
                sentence = string1.replace(replace, ant)
    return sentence

#否定词库
def deny_word():
    text_path = Path(
        Path.cwd() / 'E:\python\练习\chinese_dictionary-master\dict_negative.txt')
    with text_path.open(encoding='gbk') as f:
        text_content = f.readlines()
        deny = []

        for k in text_content:
            k = k.strip('\n')  # 去掉读取中的换行字符
            k = k.strip('\ufeff')
            deny.append(k)
        return deny

#判断标准答案是否存在双重否定
def t_double(teacher_word):
    l = []
    m = []
    q = []
    b = []
    deny = deny_word()
    # words = teacher_word()  # 标准答案字符串
    words = teacher_word
    word = pseg.cut(words)
    for i in word:
        l.append(i.word + i.flag)
        m.append(i.word)
    x = 0
    for i in range(len(m)):
        for j in range(len(deny)):
            if m[i] == deny[j]:
                x = 1
                b.append(x)
                q.append(i)
    for r in range(len(q)):
        if q[r] - q[r - 1] == 1:
            y = m[q[r]]
            z = m[q[r - 1]]
            m.remove(y)
            m.remove(z)
    return m

#判断考生答案是否存在双重否定
def s_double(answer_word):
    l = []
    m = []
    q = []
    b = []
    deny = deny_word()
    answer = answer_word #考生答案字符串
    word = pseg.cut(answer)
    for i in word:
        l.append(i.word + i.flag)
        m.append(i.word)
    x = 0
    for i in range(len(m)):
        for j in range(len(deny)):
            if m[i] == deny[j]:
                x = 1
                b.append(x)
                q.append(i)
    for r in range(len(q)):
        if q[r] - q[r-1] == 1:
            y = m[q[r]]
            z = m[q[r-1]]
            m.remove(y)
            m.remove(z)
    return m

#去除考生答案中最高频词的词
def remove_word(cut_word):
    n = high_word(cut_word)
    cut_word = stop_words(cut_word)
    array1 = cut_word
    array2 = n

    for i in range(len(array1)):
        for j in array1:
            if j in array2:
                array1.remove(j)

    return array1

#计算除高词频与标准答案的相似度
def count_high(s1_cut,s2_cut):
    # 分词
    list_word1 = s1_cut
    # s2_cut = answer()
    list_word2 = remove_word(s2_cut)

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    dist1=float(np.dot(word_vector1,word_vector2)/(np.linalg.norm(word_vector1)*np.linalg.norm(word_vector2)))
    return dist1

#计算标准答案与考生答案相似度
def count(s1_cut,s2_cut):
    # s1_cut = cut_words()  # 标准答案分词
    # s2_cut = answer()  # 考生答案分词

    word_set = set(s1_cut).union(set(s2_cut))  # 组合起来·
    word_dict = dict()  # 字典
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1

    s1_cut_code = [word_dict[word] for word in s1_cut]  # 标准答案向量
    s1_cut_code = [0] * len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]] += 1

    s2_cut_code = [word_dict[word] for word in s2_cut]  # 考生答案向量
    s2_cut_code = [0] * len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]] += 1
    # 计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(s1_cut_code)):
        sum += s1_cut_code[i] * s2_cut_code[i]
        sq1 += pow(s1_cut_code[i], 2)
        sq2 += pow(s2_cut_code[i], 2)

    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        result = 0.0

    return result

#计算关键字与考生答案的文本相似度
def count_keyword(s2_cut,s3_cut):
    # 分词
    list_word1 = s3_cut
    # s2_cut = answer()
    list_word2 = remove_word(s2_cut)

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    dist2 = float(np.dot(word_vector1, word_vector2) / (np.linalg.norm(word_vector1) * np.linalg.norm(word_vector2)))
    return dist2

def main(words,keyword,answer_word):
    s1 = words
    s1_cut = cut_words(words)  # 标准答案分词
    # print(s1_cut)
    s2_cut = answer(answer_word)  # 考生答案分词
    # print(s2_cut)
    s3_cut = key(keyword)
    key_word = keyword#关键字
    answer_cut = count_high(s1_cut,s2_cut)  #去最高频率词并与标准答案文本相似度分析结果
    # print("除最高词频的标准答案与标准答案相似度：", answer_cut)
    result = count(s1_cut,s2_cut)  #标准答案与考生答案相似度
    # print("考生答案与标准答案文本相似度：", result)
    key_result = count_keyword(s2_cut,s3_cut)#关键字与考生答案的文本相似度
    # print("考生答案与关键字文本相似度：", key_result)

    deny = deny_word()#调用否定词库

    grade = 0#定义分数为0
    if answer_cut > 0.1:
        if result+key_result < 0.5:
            grade = 0
        elif result+key_result >= 1.0:
            grade = 10
        else:
            grade = 5
    else:
        grade = 0

    # grade = 0  # 定义分数为0
    # if answer_cut != 0:
    #     if key_result > 0.5:
    #         grade += 5 + round((result * 10) / 2)
    #     else:
    #         grade += round(key_result * 10) + round((result * 10) / 2)
    # else:
    #     grade = 0
    #
    # if grade > 10:
    #     grade = 10

    a = [] #用于存放计算标准答案否定次数
    b = []#用于存放计算考生答案否定次数
    m = n = 0
    #判断标准答案是否存在否定
    for i in range(len(s1_cut)):

        for j in range(len(deny)):
            if s1_cut[i] == deny[j]:
                #print("标准答案否定句")
                n = 1
                a.append(n)

    #判断考生答案是否存在否定
    for i in range(len(s2_cut)):
        for j in range(len(deny)):
            if s2_cut[i] == deny[j]:
                #print("考生答案否定句")
                m = 1
                b.append(m)
    x = len(a)
    y = len(b)
    # print(x)
    # print(y)
    if x != y:
        grade = 0

    # print("该考生答案得分为：", grade)
    return grade
#
# if __name__ == '__main__':
#     words = "物流系统是由物流作业系统和支持物流信息流动的物流信息系统"
#     keyword = "物流作业系统、物流信息流动、物流信息系统"
#     answer_word = "物流作业和物流信息"
#     main(words,keyword,answer_word)