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
	tm_str = '{}년 {}월 {}일 {}:{}:{}'.format(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour+9, tm.tm_min, tm.tm_sec)

	return tm_str

def bignumrize(numstr):
	"""Discord 이모지로 숫자 강조"""
	result = re.sub('0', ':zero:', re.sub('1', ':one:', re.sub('2', ':two:', re.sub('3', ':three:', re.sub('4', ':four:', re.sub('5', ':five:', re.sub('6', ':six:', re.sub('7', ':seven:', re.sub('8', ':eight:', re.sub('9', ':nine:', numstr))))))))))

	return result

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

	word = tree.xpath('//span[@class="txt_issue"]//text()')
	word = list(filter(lambda x: x != '\n', word))

	result = []
	for i in range(0, 20, 2):
		result.append(word[i])
	return result

def daum_lotto(inning=''):
	"""return [회차, 연, 월, 일, 번호...]"""
	response = requests.get('https://search.daum.net/search?w=tot&q='+inning+'%20로또%20당첨%20번호')
	tree = html.fromstring(response.content)

	result = tree.xpath('//div[@class="lottonum"]//text()')
	result = list(filter(lambda x: x not in [' ', '보너스'], result))
	day = tree.xpath('//span[@class="f_date"]//text()')
	if len(day) > 0:
		day = day[0][1:-3].split('.') # (0000.00.00추첨) -> 0000.00.00
		for i in range(0, 3):
			result.insert(0, day[2-i])
	inning = tree.xpath('//span[@class="f_red"]//text()')
	if len(inning) > 0:
		result.insert(0, inning[0])

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
		if re.match('.*[가-힣]+.*', letter) is not None:
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

# server: krjp, jp, as, na, eu, oc, sa, sea, ru
def pubg_profile(name, server='krjp'):
	if server is None:
		response = requests.get('https://dak.gg/profile/'+name)
	else:
		year = str(time.gmtime().tm_year)
		month = str(time.gmtime().tm_mon)
		if len(month) < 2: month = '0' + month
		response = requests.get('https://dak.gg/profile/'+name+'/'+year+'-'+month+'/'+server)
	
	tree = html.fromstring(response.content)
	data = tree.xpath('//section[@class="solo modeItem"]//text()')
	data = list(map(lambda x: re.sub('\n', '', re.sub(' ', '', x)), data))
	data = list(filter(lambda x: x != '', data))

	if len(data) >= 44:
		result = {}
		result['avatar'] = tree.xpath('//div[@class="userInfo"]/img/@src')[0]
		result['solo-playtime'] = data[1]
		result['solo-record'] = data[2]
		result['solo-grade'] = data[3]
		result['solo-score'] = data[4]
		result['solo-rank'] = data[6]
		if len(data) == 45:
			result['solo-top'] = data[7]
		i = 7 if len(data) == 44 else 8
		result['solo-win-rating'] = data[i]	
		result['solo-win-top'] = data[i+2]
		result['solo-kill-rating'] = data[i+3]
		result['solo-kill-top'] = data[i+5]
		result['solo-kd'] = data[i+8]
		result['solo-kd-top'] = data[i+9]
		result['solo-winratio'] = data[i+11]
		result['solo-winratio-top'] = data[i+12]
		result['solo-top10'] = data[i+14]
		result['solo-top10-top'] = data[i+15]
		result['solo-avgdmg'] = data[i+17]
		result['solo-avgdmg-top'] = data[i+18]
		result['solo-games'] = data[i+20]
		result['solo-games-top'] = data[i+21]
		result['solo-mostkills'] = data[i+23]
		result['solo-mostkills-top'] = data[i+24]
		result['solo-headshots'] = data[i+26]
		result['solo-headshots-top'] = data[i+27]
		result['solo-longest'] = data[i+29]
		result['solo-longest-top'] = data[i+30]
		result['solo-survived'] = data[i+32]
		result['solo-survived-top'] = data[i+33]
	else:
		result = None

	return result

GF_TIMES = { '00:20': ['M1911', '나강 리볼버', 'P38'], '00:22': ['PPK'], '00:25': ['FNP-9', 'MP-446'], '00:28': ['USP Compact', 'Bren Ten'], '00:30': ['P08', 'C96'], '00:35': ['92식', 'P99'], '00:40': ['아스트라 리볼버', 'M9', '마카로프'], '00:45': ['토카레프'], '00:50': ['콜트 리볼버', 'Mk23'], '00:52': ['스핏파이어'], '00:53': ['K5'], '00:55': ['P7', '스테츠킨'], '01:00': ['웰로드 MKII'], '01:02': ['컨텐더'], '01:05': ['M950A', 'NZ75'], '01:10': ['그리즐리 Mk V', 'IDW', 'PP-2000'], '01:20': ['Spectre M4', 'M45'], '01:25': ['64식'], '01:30': ['MP40', '베레타 38형', 'M3'], '01:40': ['스텐 Mk.II', '마이크로 우지'], '01:50': ['F1', 'PPSh-41'], '02:00': ['MAC-10', '스콜피온'], '02:05': ['Z-62'], '02:10': ['PPS-43'], '02:15': ['UMP-9', 'UMP-45'], '02:18': ['시프카', 'PP-19-01'], '02:20': ['MP5', 'PP-90'], '02:25': ['수오미'], '02:28': ['C-MS'], '02:30': ['톰슨', 'G36C'], '02:33': ['SR-3MP'], '02:35': ['벡터', '79식'], '02:40': ['갈릴', 'SIG-510'], '02:45': ['F2000', '63식'], '02:50': ['L85A1', 'G3'], '03:00': ['StG44'], '03:10': ['OTs-12', 'G43', 'FN-49'], '03:15': ['ARX-160'], '03:20': ['AK-47', 'FNC', 'BM59'], '03:25': ['56-1식', 'XM8'], '03:30': ['AS Val', 'FAMAS', 'TAR-21', '시모노프', 'SVT-38'], '03:35': ['9A-91'], '03:40': ['G36', '리베롤☆', 'M14', 'SV-98'], '03:45': ['FAL'], '03:48': ['T91'], '03:50': ['95식', '97식', '한양조88식', 'OTs-44(중형제조)'], '03:52': ['K2'], '03:53': ['MDR'], '03:55': ['HK416'], '03:58': ['RFB'], '04:00': ['M1 개런드'], '04:04': ['G11'], '04:05': ['G41', 'Zas M21'], '04:09': ['AN-94'], '04:10': ['모신나강', 'T-5000'], '04:12': ['AK-12'], '04:15': ['SVD'], '04:20': ['PSG-1(중형제조)', 'G28(중형제조)'], '04:25': ['스프링필드'], '04:30': ['PTRD', 'PzB39(중형제조)'], '04:38': ['카르카노 M1891'], '04:40': ['Kar98k'], '04:42': ['카르카노 M91/38'], '04:45': ['NTW-20'], '04:50': ['WA2000', 'AAT-52', 'FG42'], '04:52': ['IWS 2000'], '04:55': ['M99'], '05:00': ['리엔필드', 'MG34', 'DP28'], '05:10': ['LWMMG'], '05:20': ['브렌'], '05:40': ['M1919A4'], '05:50': ['MG42'], '06:10': ['M2HB', 'M60'], '06:15': ['80식'], '06:20': ['Mk48', 'AEK-999'], '06:25': ['M1918', '아멜리'], '06:30': ['PK', 'MG3'], '06:35': ['네게브'], '06:40': ['MG4'], '06:45': ['MG5'], '06:50': ['PKP'], '07:15': ['NS2000'], '07:20': ['M500'], '07:25': ['KS-23'], '07:30': ['RMB-93', 'M1897'], '07:40': ['M590', 'SPAS-12'], '07:45': ['M37'], '07:50': ['Super-Shorty'], '07:55': ['USAS-12'], '08:00': ['KSG'], '08:05': ['Saiga-12'], '08:10': ['S.A.T.8'] }
def gf_times(pd_time):
	if len(pd_time) == 4:
		pd_time = pd_time[0:2] + ':' + pd_time[2:4]
	
	return GF_TIMES[pd_time]

class PlayingCard:
	NUMBERS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
	SUITS = ['♧', '◇', '♡', '♤']

	def __init__(self, number, suit, value, point):
		self.number = number
		self.suit = suit
		self.value = value
		self.point = point

	def __str__(self):
		return self.suit + self.number

	@classmethod
	def str(cls, cards):
		return [str(card) for card in cards]

	@classmethod
	def bj_sum(cls, cards):
		result = sum(card.value for card in cards)
		cnt_a = list(map(lambda x: x.number, cards)).count('A')
		result += cnt_a * 10
		if result > 21:
			for _ in range(0, cnt_a):
				result -= 10
				if result <= 21: break

		return result

class Deck:
	def __init__(self):
		self.cards = []
		point = 1
		for i, number in enumerate(PlayingCard.NUMBERS):
			for suit in PlayingCard.SUITS:
				self.cards.append(
				    PlayingCard(number, suit, min(i + 1, 10), point))
				point += 1

	def shuffle(self):
		random.shuffle(self.cards)

	def size(self):
		return len(self.cards)

	def draw(self):
		return self.cards.pop()

	def top(self):
		return self.cards[-1]  #if len(self.cards) > 0 else None

class Blackjack:
	def __init__(self, player):
		self.player = player
		self.cnt_dhit = 0
		self.deck = Deck()
		self.deck.shuffle()
		self.pcards = [self.deck.draw(), self.deck.draw()]  # player
		self.dcards = [self.deck.draw(), self.deck.draw()]  # dealer
		self.calc_psum()
		self.calc_dsum()

	def __str__(self):
		return 'Dealer\'s cards: {} ({} + ?)\nYour cards: {} ({})'.format(
		    ', '.join(PlayingCard.str(self.dcards[0:-1])),
		    str(PlayingCard.bj_sum(self.dcards[0:-1])), ', '.join(
		        PlayingCard.str(self.pcards)),
		    str(PlayingCard.bj_sum(self.pcards)))

	def result(self):
		return 'Dealer\'s cards: {} ({})\nYour cards: {} ({})'.format(
		    ', '.join(PlayingCard.str(self.dcards)),
		    str(PlayingCard.bj_sum(self.dcards)), ', '.join(
		        PlayingCard.str(self.pcards)),
		    str(PlayingCard.bj_sum(self.pcards)))

	def calc_psum(self):
		self.psum = PlayingCard.bj_sum(self.pcards)

	def calc_dsum(self):
		self.dsum = PlayingCard.bj_sum(self.dcards)

	def pdraw(self):
		self.pcards.append(self.deck.draw())
		self.calc_psum()

	def ddraw(self):
		self.dcards.append(self.deck.draw())
		self.calc_dsum()

	def win(self):
		print('* You win!')

	def lose(self):
		print('* You lose.')

BJ_BLACKJACK_MESSAGES = ['블랙잭!!']
BJ_HIT_MESSAGES = ['히트!', '히트다 히트!', '한 장 더 뽑을게요.']
BJ_HIT_MESSAGES_FIRST = ['저는 히트할게요.']
BJ_HIT_MESSAGES_MORE = []
BJ_STAND_MESSAGES = ['스탠드!', '스탠드.']
BJ_STAND_MESSAGES_HIT = ['여기까지 할게요.']
BJ_STAND_MESSAGES_NOHIT = ['저는 바로 스탠드할게요.']
BJ_BUST_MESSAGES_PLAYER = ['버스트!', '버스트! 욕심이었어요.']
BJ_BUST_MESSAGES_DEALER = ['왝.', '아니!', '버스트. 저의 패배예요.']
BJ_WIN_MESSAGES_PLAYER = ['제가 졌어요.', '저의 패배예요.', '졌어요. 제법이시군요.']
BJ_WIN_MESSAGES_DEALER = ['제가 이겼어요!', '저의 승리예요!', '특이점은 온다!']
BJ_DRAW_MESSAGES = ['비겼네요.', '무승부예요.', '무승부! 한 판 더 하실래요?']
def blackjack(player):
	bj = Blackjack(player)
	return bj