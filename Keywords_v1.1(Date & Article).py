import pandas as pd
import jieba
import jieba.analyse
from collections import Counter
from datetime import datetime
import os
import json

board = 'Gossiping'


os.chdir('C:/Users/home/PyCharm/PTT')

jieba.load_userdict('Data/Normal_words.txt')
jieba.set_dictionary('Data/BigDict.txt')

drop_words = [word.strip() for word in open('Data/Drop_words.txt', 'r', encoding='utf-8').readlines()]
del_words = [word.strip() for word in open('Data/Del_words.txt', 'r', encoding='utf-8').readlines()]
drop_words += del_words + ['\n', ' ', '\u3000']


def drop_word(Seg_list):
    Seg_list = list(set(Seg_list))
    for word in drop_words:
        if word in Seg_list:Seg_list.remove(word)
    Seg_list.sort()
    return Seg_list


def drop_counters_word(counters_dict):
    for word in drop_words:
        if word in counters_dict:del counters_dict[word]
    return counters_dict


def Jieba_words(article):
    seg_list = jieba.lcut(article)
    counters = Count_words(seg_list)

    isinstance(counters, dict)                              # 將counters轉字典
    counters_dict = {**counters}
    counters_dict = drop_counters_word(counters_dict)
    print('text(Counter_dict):', counters_dict)

    return counters_dict

def Count_words(Seg_list):
    counters = Counter(Seg_list)
    return counters


def Article_wordsCount_main(file_name):

    file_path = '[Backup]/[Article]/' + board
    PTT_Dataframe = pd.read_csv(file_path + '/' + file_name.replace('.csv','_clean.csv'))

    ArticleCounter_dict_all, MessagesCounter_dict_all = [], []
    for i in range(len(PTT_Dataframe)):
        print(i)
        try:
            ArticleCounter_dict = Jieba_words(PTT_Dataframe.loc[i, 'article'])
            ArticleCounter_dict_all.append(ArticleCounter_dict)
        except:
            print(PTT_Dataframe.loc[i, 'article'])
            ArticleCounter_dict_all.append('NAN')

        print('==============================================================================================================================================================================')

    PTT_Dataframe['Article_wordsCounter'] = ['NAN' for i in range(len(PTT_Dataframe))]

    for index, counter in enumerate(ArticleCounter_dict_all):
        PTT_Dataframe.loc[index, 'Article_wordsCounter'] = str(counter)

    PTT_Dataframe.reindex(columns=['Date', 'Article_wordsCounter']).to_csv(file_path + '/' + file_name.replace('.csv','_count.csv'), encoding='utf-8-sig', index=False)


if __name__ == "__main__":
    Article_wordsCount_main('PTT_' + board + '_article(7w).csv')