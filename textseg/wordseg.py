#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import re

import jieba
import jieba.posseg as pseg
import jieba.analyse

# 類別詞性: n(名詞)
# 正負評詞性: a(形容詞), v(動詞), z(狀態詞), i(成語), l(慣用語)
# 刪除: p(介詞), u(助詞), e(嘆詞), eng(英文), o(狀聲詞), s(處所詞), f(方位詞), r(代詞), h(前綴), k(後綴), w(標點)
#       c(連詞), x(字符), y(語氣詞)
#       t(時間詞-除"過期"外都可刪), m(數詞n), q(量詞-諧音), d(副詞a), b(區別詞a), j(簡稱n), g(語素n，前頭加字母)

class WordSeg:
    words = None			# 斷完後的詞
    fre = None				# 詞頻
    speech = None			# 詞性

    keyspeech_re = None		# 要保留的詞性

    # 設定辭典
    def setDict(self, path):
        jieba.set_dictionary("extra_dict/dict.txt.big")		# 更改辭典
        jieba.load_userdict(path)							# 加入自定義辭典

    # 設定要保留的詞性
    def setSpeech(self, key):
        regex = "^(" + key[0]
        for i in range(1, len(key)):
            regex += "|" + key[i]
        regex += ")"
        self.keyspeech_re = re.compile(regex)

    # 斷詞處理
    def segment(self, content, mode=False):
        self.words = jieba.cut(content, cut_all=mode)

        self.fre = collections.defaultdict(int)
        for word in self.words:
            self.fre[word] += 1

        return self.words

    # 搜尋引擎斷詞模式
    def segSearch(self, content):
        self.words = jieba.cut_for_search(content)
        return self.words

    #斷詞、取得位置
    def segPos(self, content):
        self.words = jieba.tokenize(content)
        for tk in self.words:
            print("%s\t start: %d \t end:%d" % (tk[0], tk[1], tk[2]))
        return self.words

    # 斷詞、取得詞性
    def segSpeech(self, content):
        self.words = pseg.cut(content)		# 斷詞、標注詞性

        self.fre = collections.defaultdict(int)
        self.speech = collections.defaultdict(str)

        for word in self.words:
            if self.keyspeech_re != None and not self.keyspeech_re.search(word.flag):
                continue
            self.fre[word.word] += 1
            self.speech[word.word] = word.flag

        return self.words

    # 取出前 n 個 tf-idf 值最大的關鍵詞
    def extractKey(self, content, n=20):
        self.words = jieba.analyse.extract_tags(content, n)
        print(",".join(self.words))
        return self.words
