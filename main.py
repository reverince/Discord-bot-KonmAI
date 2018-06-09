import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import re
import time
import datetime

from funcs import *

TOKEN = '' # SECURE!!!

PREFIX = '`'
DESCRIPTION = ''
GAME = '도움말은 `도움'
THEME_COLOR = 0x00a0ee
ICON_URL = 'https://ko.gravatar.com/userimage/54425936/ab5195334dd95d4171ac9ddab1521a5b.jpeg'

bot = Bot(description=DESCRIPTION, command_prefix=PREFIX)

cho_quizs = {} # 초성퀴즈 관리
bj_games = {} # 블랙잭 관리
lots_games = {} # 제비뽑기 관리
fortune_users = {} # 운세 관리

class ChoQuiz:
	def __init__(self):
		self.genre = None
		self.count = None
		self.answer = None
		self.score = None
	
	@classmethod
	def find(cls, channel):
		global cho_quizs

		return cho_quizs[channel] if channel in cho_quizs.keys() else None
	
	@classmethod
	def start(cls, channel, genre, count, answer):
		global cho_quizs

		cho_quizs[channel] = ChoQuiz()
		cho_quizs[channel].genre = genre
		cho_quizs[channel].count = count
		cho_quizs[channel].answer = answer

		return cho_quizs[channel]
	
	@classmethod
	def end(cls, channel):
		global cho_quizs
		if cho_quizs[channel] is not None:
			del cho_quizs[channel]
			result = '초성퀴즈를 종료했어요.'
		else:
			result = '진행 중인 초성퀴즈가 없어요.'

		return result

async def blackjack_dturn(player, channel):
	while True:
		if bj_games[player].dsum < 17: # 딜러 히트
			await asyncio.sleep(1.0)
			if bj_games[player].cnt_dhit > 0:
				await bot.send_message(channel, random.choice(BJ_HIT_MESSAGES + BJ_HIT_MESSAGES_MORE))
			else:
				await bot.send_message(channel, random.choice(BJ_HIT_MESSAGES + BJ_HIT_MESSAGES_FIRST))
			bj_games[player].cnt_dhit += 1
			bj_games[player].ddraw()
			await asyncio.sleep(1.0)
			if bj_games[player].dsum > 21:
				await asyncio.sleep(1.0)
				await bot.send_message(channel, bj_games[player].result())
				await asyncio.sleep(0.5)
				await bot.send_message(channel, random.choice(BJ_BUST_MESSAGES_DEALER))
				del bj_games[player]
				break
			else:
				await bot.send_message(channel, bj_games[player])
		else: # 딜러 스탠드
			await asyncio.sleep(1.0)
			if bj_games[player].cnt_dhit > 0:
				await bot.send_message(channel, random.choice(BJ_STAND_MESSAGES + BJ_STAND_MESSAGES_HIT))
			else:
				await bot.send_message(channel, random.choice(BJ_STAND_MESSAGES + BJ_STAND_MESSAGES_NOHIT))
			break
	if player in bj_games.keys():
		await asyncio.sleep(1.0)
		await bot.send_message(channel, bj_games[player].result())
		await asyncio.sleep(1.0)
		if bj_games[player].psum > bj_games[player].dsum:
			await bot.send_message(channel, random.choice(BJ_WIN_MESSAGES_PLAYER))
		elif bj_games[player].psum < bj_games[player].dsum:
			await bot.send_message(channel, random.choice(BJ_WIN_MESSAGES_DEALER))
		else:
			await bot.send_message(channel, random.choice(BJ_DRAW_MESSAGES))
		del bj_games[player]

# Events

@bot.event
async def on_ready():
	server_names = [x.name for x in bot.servers]
	member_names = [x.name for x in set(bot.get_all_members())]
	member_names.remove('KonmAI')
	print(bot.user.name+' 온라인. ( ID : '+bot.user.id+' )')
	print('Discord.py 버전 : '+discord.__version__)
	print('연결된 서버 '+str(len(bot.servers))+'개 : '+', '.join(server_names))
	print('연결된 유저 '+str(len(member_names))+'명 : '+', '.join(member_names))
	
	bot.remove_command('help')
	await bot.change_presence(game=discord.Game(name=GAME))

@bot.event
async def on_message(message):
	channel = message.channel

	# 초성퀴즈 메시지 처리
	cho_quiz = ChoQuiz.find(channel)
	if cho_quiz is not None:
		if message.content == cho_quiz.answer:
			await bot.send_message(channel, '**{}**님의 [**{}**] 정답! :white_check_mark:'.format(message.author.mention, cho_quiz.answer))
			cho_quiz.count -= 1
			if cho_quiz.count > 0:
				cho_quiz.answer = jaum_quiz(cho_quiz.genre)
				await bot.send_message(channel, cho(cho_quiz.answer))
			else:
				await bot.send_message(channel, ChoQuiz.end(channel))
		
	await bot.process_commands(message) # 커맨드 처리

# Commands

@bot.command()
async def 도움():
	"""ㄴㄱ ㄴㄱㄴㄱ?"""
	embed = discord.Embed(description='만나서 반가워요.', color=THEME_COLOR)
	embed.set_author(name='KonmAI v0.4', url='https://discord.gg/E6eXnpJ', icon_url=ICON_URL)
	embed.add_field(name='`더해', value='주어진 수들을 덧셈해 드려요. (무료)', inline=True)
	embed.add_field(name='`빼', value='처음 수에서 나머지 수를 뺄셈해 드려요.', inline=True)
	embed.add_field(name='`계산', value='(이 정도 쯤이야.)', inline=True)
	embed.add_field(name='`골라', value='배그할까 레식할까? ` `골라 배그 레식 `', inline=True)
	embed.add_field(name='`사전', value='[Daum](https://daum.net) 사전 검색을 대신해 드려요.', inline=True)
	embed.add_field(name='`실검', value='Daum 실시간 검색어 순위를 알려 드려요.', inline=True)
	embed.add_field(name='`로또', value='Daum에서 로또 당첨 번호를 검색해 드려요. 회차를 지정할 수 있어요.', inline=True)
	embed.add_field(name='`초성', value='초성퀴즈를 할 수 있어요. (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)\n` `초성 게임 5 `처럼 사용하세요. 끝내려면 ` `초성 끝 `을 입력하세요.', inline=True)
	embed.add_field(name='`배그', value='[dak.gg](https://dak.gg)에서 배틀그라운드 전적을 찾아 드려요.\n` `배그 KonmAI `처럼 사용하세요. (미완성)', inline=True)
	embed.add_field(name='`소전', value='제조 시간을 입력하시면 등장하는 전술인형 종류를 알려 드려요.\n` `소전 03:40 `처럼 사용하세요.', inline=True)
	embed.add_field(name='`블랙잭', value='저와 블랙잭 승부를 겨루실 수 있어요. 히트는 ` `H `, 스탠드는 ` `S `를 입력하세요.', inline=True)
	embed.add_field(name='`제비', value='당첨이 한 개 들어 있는 제비를 준비해 드려요.\n` `제비 3 `처럼 시작하고 ` `제비 `로 뽑으세요. 끝내려면 ` `제비 끝 `을 입력하세요.', inline=True)
	embed.add_field(name='`운세', value='오늘의 운세를 점쳐볼 수 있어요. (미완성)', inline=True)

	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def 더해(ctx, *args):
	try:
		result = sum(list(map(int, args)))
		result = ' + '.join(args) + ' = **' + str(result) + '**'
	except ValueError:
		result = '숫자를 입력해 주세요.'
	
	try:
		await bot.delete_message(ctx.message)
	except:
		pass
	await bot.say(ctx.message.author.mention+'님, '+result)
@bot.command(pass_context=True)
async def 빼(ctx, *args):
	try:
		result = int(args[0]) - sum(list(map(int, args[1:])))
		result = ' - '.join(args) + ' = **' + str(result) + '**'
	except ValueError:
		result = '숫자를 입력해 주세요.'
	
	try:
		await bot.delete_message(ctx.message)
	except:
		pass
	await bot.say(ctx.message.author.mention+'님, '+result)
@bot.command(pass_context=True)
async def 계산(ctx, *args):
	try:
		result = ' '.join(args) + ' = ' + str(eval(''.join(args)))
	except ZeroDivisionError:
		result = '아무래도 0으로 나눌 수는 없어요. :thinking:'
	except:
		result = '알맞은 계산식을 입력해 주세요.'
	
	try:
		await bot.delete_message(ctx.message)
	except:
		pass
	await bot.say(ctx.message.author.mention+'님, '+result)

@bot.command(pass_context=True)
async def 골라(ctx, *args):
	if len(args) > 1:
		choice = random.choice(args) if '히오스' not in args else '히오스'
		CHOICE_MESSAGES = ['**'+choice+'**'+josa(choice, '가')+' 어떨까요? :thinking:', '저라면 **'+choice+'**예요.', '저는 **'+choice+'**'+josa(choice, '를')+' 추천할게요! :relaxed:', '저라면 **'+choice+'**'+josa(choice, '를')+' 선택하겠어요. :relaxed:', '**'+choice+'**'+josa(choice, '로')+' 가죠. :sunglasses:', '답은 **'+choice+'**'+josa(choice, '로')+' 정해져 있어요. :sunglasses:']

		result = ctx.message.author.mention+'님, ' + random.choice(CHOICE_MESSAGES)
	elif len(args) == 1:
		result = ':sweat:'
	else:
		result = '어떤 것들 중에서 고를지 다시 알려주세요.'
	
	await bot.say(result)

@bot.command()
async def 사전(*args):
	"""Daum 사전 검색"""
	if len(args) > 0:
		result = daum_search(' '.join(args))
	else:
		result = '검색 키워드를 입력해 주세요.'
	
	await bot.say(result)
@bot.command()
async def 실검():
	"""Daum 실시간 검색어 순위"""
	ranks = daum_realtime()
	link = 'https://search.daum.net/search?w=tot&q='
	time = korea_time_string()

	embed=discord.Embed(title='Daum 실시간 검색어 순위', url="https://www.daum.net/", description=time+' 기준', color=THEME_COLOR)
	for i in range(0, 10):
		embed.add_field(name=str(i+1)+'위', value='[{}]({})'.format(ranks[i], link+re.sub(' ', '%20', ranks[i])), inline=True if i > 0 else False)
	
	await bot.say(embed=embed)
@bot.command()
async def 로또(*args):
	"""Daum 로또 당첨 번호 검색"""
	success = True
	if len(args) > 0:
		if args[0].isnumeric():
			inning = args[0]
			data = daum_lotto(inning)
		else:
			result = '회차는 숫자로만 입력해 주세요.'
			success = False
	else:
		data = daum_lotto()
	
	if success:
		embed = discord.Embed(description=data[1]+'년 '+data[2]+'월 '+data[3]+'일 추첨', color=THEME_COLOR)
		embed.set_author(name='로또 추첨 번호 by 다음', url='https://search.daum.net/search?w=tot&q='+data[0]+'%20로또%20당첨%20번호', icon_url=ICON_URL)
		embed.add_field(name=data[0], value=bignumrize('  '.join(data[4:-1])+' :small_orange_diamond: '+data[-1]))

		await bot.say(embed=embed)
	else:
		await bot.say(result)

@bot.command(pass_context=True)
async def 초성(ctx, *args):
	"""초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)"""
	channel = ctx.message.channel
	cho_quiz = ChoQuiz.find(channel)
	
	if len(args) > 0 and args[0] == '끝':
			result = ChoQuiz.end(channel)
	else:
		if cho_quiz is not None:
			result = '이미 진행중인 초성퀴즈가 있어요.'
		else:
			genre = args[0] if len(args) > 0 else None
			count = int(args[1]) if len(args) > 1 else 10
			
			if genre not in ['영화', '음악', '동식물', '사전', '게임', '인물', '책']:
				result = '장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책'
			else: # OK
				answer = jaum_quiz(genre) # 정답 생성
				cho_quiz = ChoQuiz.start(channel, genre, count, answer)
				result = cho(answer)
	
	await bot.say(result) # 채널에 초성 공개

@bot.command()
async def 배그(*args):
	"""dak.gg PUBG 프로필 검색"""
	if len(args) > 0:
		name = args[0]
		ratings = pubg_profile(name)
		year = str(time.gmtime().tm_year)
		month = str(time.gmtime().tm_mon)
		if len(month) < 2: month = '0' + month

		if ratings is not None:
			embed=discord.Embed(title=name, description='시즌: '+year+'-'+month, color=THEME_COLOR)
			embed.set_author(name='PUBG 솔로 전적 by dak.gg', url='https://dak.gg/profile/'+name+'/'+year+'-'+month+'/krjp', icon_url=ICON_URL)
			embed.set_thumbnail(url=ratings['avatar'])
			embed.add_field(name='플레이타임', value=re.sub('hours', '시간', re.sub('mins', '분', ratings['solo-playtime'])), inline=True)
			embed.add_field(name='기록', value=re.sub('W', '승 ', re.sub('T', '탑 ', re.sub('L', '패', ratings['solo-record']))), inline=True)
			embed.add_field(name='등급', value=ratings['solo-grade'], inline=True)
			embed.add_field(name='점수', value='{} ({})'.format(ratings['solo-score'], ratings['solo-rank']), inline=True)
			embed.add_field(name='승점', value='{} ({})'.format(ratings['solo-win-rating'], ratings['solo-win-top']), inline=True)
			embed.add_field(name='승률', value='{} ({})'.format(ratings['solo-winratio'], ratings['solo-winratio-top']), inline=True)
			embed.add_field(name='TOP10', value='{} ({})'.format(ratings['solo-top10'], ratings['solo-top10-top']), inline=True)
			embed.add_field(name='여포', value='{} ({})'.format(ratings['solo-kill-rating'], ratings['solo-kill-top']), inline=True)
			embed.add_field(name='K/D', value='{} ({})'.format(ratings['solo-kd'], ratings['solo-kd-top']), inline=True)
			embed.add_field(name='평균 데미지', value='{} ({})'.format(ratings['solo-avgdmg'], ratings['solo-avgdmg-top']), inline=True)
			embed.add_field(name='최대 킬', value='{} ({})'.format(ratings['solo-mostkills'], ratings['solo-mostkills-top']), inline=True)
			embed.add_field(name='헤드샷', value='{} ({})'.format(ratings['solo-headshots'], ratings['solo-headshots-top']), inline=True)
			embed.add_field(name='저격', value='{} ({})'.format(ratings['solo-longest'], ratings['solo-longest-top']), inline=True)
			embed.add_field(name='게임 수', value='{} ({})'.format(ratings['solo-games'], ratings['solo-games-top']), inline=True)
			embed.add_field(name='생존', value='{} ({})'.format(ratings['solo-survived'], ratings['solo-survived-top']), inline=True)
			
			await bot.say(embed=embed)
		else:
			await bot.say('아이디 검색에 실패했어요.')
	else:
		await bot.say('아이디를 입력해 주세요.')

@bot.command()
async def 소전(*args):
	"""소녀전선 제조시간 검색"""
	if len(args) > 0:
		if len(args[0]) in [4, 5]:
			pd_time = args[0]

			await bot.say('제조시간이 '+pd_time+'인 전술인형: '+', '.join(gf_times(pd_time)))
	else:
		await bot.say('제조시간을 입력해 주세요.')

@bot.command(pass_context=True)
async def 블랙잭(ctx):
	global bj_games
	player = ctx.message.author

	if player not in bj_games.keys():
		bj_games[player] = blackjack(player)
		await bot.say(bj_games[player])
		if bj_games[player].psum == 21:
			await asyncio.sleep(0.5)
			await bot.say(random.choice(BJ_BLACKJACK_MESSAGES))
			await blackjack_dturn(player, ctx.message.channel)
	else:
		await bot.say('이미 진행 중인 게임이 있어요.')
@bot.command(pass_context=True)
async def H(ctx):
	player = ctx.message.author
	channel = ctx.message.channel

	if player in bj_games.keys():
		bj_games[player].pdraw()
		await asyncio.sleep(1.0)
		await bot.say(bj_games[player])
		if bj_games[player].psum > 21:
			await asyncio.sleep(0.5)
			await bot.say(random.choice(BJ_BUST_MESSAGES_PLAYER))
			del bj_games[player]
		elif bj_games[player].psum == 21:
			await asyncio.sleep(0.5)
			await bot.say(random.choice(BJ_BLACKJACK_MESSAGES))
			await blackjack_dturn(player, channel)
	else:
		await bot.say('진행 중인 게임이 없어요.')
@bot.command(pass_context=True)
async def S(ctx):
	player = ctx.message.author
	channel = ctx.message.channel

	if player in bj_games.keys():
		await blackjack_dturn(player, channel)
	else:
		await bot.say('진행 중인 게임이 없어요.')

@bot.command(pass_context=True)
async def 제비(ctx, *args):
	channel = ctx.message.channel

	if len(args) > 0:
		if args[0].isnumeric():
			if channel not in lots_games.keys():
				lots_games[channel] = [True] + [False] * (int(args[0]) - 1)
				random.shuffle(lots_games[channel])
				result = '제비뽑기가 준비됐어요.'
			else:
				result = '이미 준비된 제비가 있어요.'
		elif args[0] == '끝':
			if channel in lots_games.keys():
				del lots_games[channel]
				result = '제비뽑기를 취소했어요.'
			else:
				result = '준비된 제비가 없어요.'
		else:
			result = '숫자를 입력해 주세요.'
	else:
		if channel not in lots_games.keys():
			result = '제비 개수를 입력해 주세요.'
		else:
			lot = lots_games[channel].pop()
			if lot: del lots_games[channel]
			result = ctx.message.author.mention+'님, **당첨**! :tada:' if lot else ctx.message.author.mention+'님, 꽝. :smirk:'
	
	await bot.say(result)

@bot.command(pass_context=True)
async def 운세(ctx):
	author = ctx.message.author
	today = datetime.date.today()

	if author not in fortune_users.keys() or (today - fortune_users[author]).days > 0:
		fortune_users[author] = today
		result = random.choice(FORTUNES)
	else:
		result = '오늘은 이미 오미쿠지를 뽑았어요.'
	
	await bot.say(result)

# Commands for DEBUG

@bot.command()
async def 오늘운():
	await bot.say([x.name for x in fortune_users])

# End of commands

bot.run(TOKEN)
