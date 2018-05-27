import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import requests
import random
import re
import time

def korea_time_string():
	"""REPL.IT 전용. UTC를 한국 시간으로 변환"""
	tm = time.gmtime()
	tm_str = '{}월 {}일 {}:{}:{}'.format(tm.tm_mon, tm.tm_mday, tm.tm_hour+9, tm.tm_min, tm.tm_sec)

	return tm_str

def daum_search(keyword):
	page = requests.get('http://dic.daum.net/search.do?q=' + keyword)
	tree = html.fromstring(page.content)

	result = ''
	i = 1
	while True:
		result += '\n'
		word = tree.xpath('//div[@id="mArticle"]/div[1]/div[2]/div[2]/div['+str(i)+']/div[1]/strong[1]//text()')
		if len(word) == 0: break
		result += ' '.join(''.join(word).split()) + '\n'

		meanings = []
		j = 1
		while True:
			meaning = tree.xpath('//div[@id="mArticle"]/div[1]/div[2]/div[2]/div['+str(i)+']/ul/li['+str(j)+']//text()')
			if len(meaning) == 0: break
			meaning.insert(1, ' ')
			meanings.append(''.join(meaning))
			meanings.append(' ')
			j += 1
		result += ''.join(meanings[:-1]) + '\n'
		i += 1
	
	return result

def daum_realtime():
	""" 1~10위 배열 반환 """
	response = requests.get('https://www.daum.net/')
	tree = html.fromstring(response.content)

	word = tree.xpath('//*[@id="mArticle"]/div[2]/div[1]/div[2]/div[1]/ol//text()')
	word = list(filter(lambda x: x != '\n', word))

	result = []
	for i in range(1, 39, 4):
		result.append(word[i])
	return result

BASE, CHO, JUNG = 44032, 588, 28
CHO_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
CHO_LITE_LIST = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
PARSED_CHO_LIST = ['%A1', '%A2', '%A4', '%A7', '%A8', '%A9', '%B1', '%B2', '%B3', '%B5', '%B6', '%B7', '%B8', '%B9', '%BA', '%BB', '%BC', '%BD', '%BE']

def cho(keyword):
	""" 단어를 초성으로 """
	split_keyword_list = list(keyword)
	result = []
	for letter in split_keyword_list:
		if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', letter) is not None:
			char_code = ord(letter) - BASE
			cho_code = int(char_code / CHO)
			result.append(CHO_LIST[cho_code])
		else:
			result.append(letter)

	return ''.join(result)

def cho_gen_lite(length):
	result = ''
	for _ in range(0, length):
		result += CHO_LITE_LIST[random.randint(0, 13)]

	return result

def jaum_search(genre=None, chos=cho_gen_lite(random.randint(2,3))):
	""" genre : movie, music, animal, dic, game, people, book """
	query = ''
	for i in range(0, len(chos)):
		query += '%A4' + PARSED_CHO_LIST[CHO_LIST.index(chos[i])]
	if genre == None:
			page = requests.get('http://www.jaum.kr/index.php?w='+query)
	else:
		page = requests.get('http://www.jaum.kr/index.php?w='+query+'&k='+genre)
	tree = html.fromstring(page.content)
	
	result = tree.xpath('//*[@id="container"]/div/table/tbody/tr[1]/td[1]//text()')

	return result

def jaum_quiz(genre=None):
	if genre == "영화": genre = 'movie'
	elif genre == "음악": genre = 'music'
	elif genre == "동식물": genre = 'animal'
	elif genre == "사전": genre = 'dic'
	elif genre == "게임": genre = 'game'
	elif genre == "인물": genre = 'people'
	elif genre == "책": genre = 'book'
	else:	return None

	answers = []
	while len(answers) == 0:
		answers = jaum_search(genre, cho_gen_lite(random.randint(2,3)))
	answer = re.sub(r'\s+$', '', re.sub(r'^\s+', '', re.sub(r'(?i)[A-Z().]', '', random.choice(answers))))

	print('정답 : '+answer) #DEBUG
	return answer
