import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import re

import funcs

TOKEN = '' # SECURE!!!

PREFIX = '`'
DESCRIPTION = ''
GAME = '도움말은 `도움'
THEME_COLOR = 0x00a0ee

bot = Bot(description=DESCRIPTION, command_prefix=PREFIX)

cho_quizs = {} # 초성퀴즈 관리

class ChoQuiz:
	def __init__(self):
		self.genre = None
		self.answer = None
		self.count = None
		self.score = None
	
	@classmethod
	def find(cls, channel):
		global cho_quizs

		return cho_quizs[channel] if channel in list(cho_quizs.keys()) else None
	@classmethod
	def start(cls, channel):
		global cho_quizs

		cho_quizs[channel] = ChoQuiz()

		return cho_quizs[channel]
	@classmethod
	def end(cls, channel):
		cho_quiz = cls.find(channel)
		if cho_quiz is None or cho_quiz.answer is None:
			result = '진행 중인 초성퀴즈가 없어요.'
		else:
			cho_quiz.__init__()
			result = '초성퀴즈를 종료했어요.'

		return result

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
	
	bot.remove_command('help') # `help 명령어 제거
	await bot.change_presence(game=discord.Game(name=GAME))

@bot.event
async def on_message(message):
	cho_quiz = ChoQuiz.find(message.channel)
	if cho_quiz is not None and cho_quiz.answer is not None:
		if message.content == cho_quiz.answer:
			await bot.send_message(message.channel, '**{}**님의 [**{}**] 정답! '.format(message.author.mention, cho_quiz.answer))
			cho_quiz.count -= 1
			if cho_quiz.count > 0:
				cho_quiz.answer = funcs.jaum_quiz(cho_quiz.genre)
				await bot.send_message(message.channel, funcs.cho(cho_quiz.answer))
			else:
				await bot.send_message(message.channel, ChoQuiz.end(message.channel))
	
	await bot.process_commands(message) # 커맨드 처리

# Commands

@bot.command()
async def 도움():
	"""ㄴㄱ ㄴㄱㄴㄱ?"""
	embed = discord.Embed(description='만나서 반가워요.', color=THEME_COLOR)
	embed.set_author(name="KonmAI v0.3", url="https://discord.gg/E6eXnpJ", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
	embed.add_field(name='`더해', value='주어진 수들을 덧셈해 드려요. (무료)', inline=True)
	embed.add_field(name='`빼', value='처음 수에서 나머지 수를 뺄셈해 드려요.', inline=True)
	embed.add_field(name='`계산', value='(이 정도 쯤이야.)', inline=True)
	embed.add_field(name='`골라', value='배그할까 레식할까? ` `골라 배그 레식 `', inline=True)
	embed.add_field(name='`검색', value='Daum 검색을 대신해 드려요.', inline=True)
	embed.add_field(name='`실검', value='Daum 실시간 검색어 순위를 알려 드려요.', inline=True)
	embed.add_field(name='`초성', value='초성퀴즈를 할 수 있어요. (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)\n` `초성 게임 5 `처럼 사용하세요. 끝내려면 ` `초성끝 `을 입력하세요.', inline=True)

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
		result = '아무래도 0으로 나눌 수는 없어요.'
	except:
		result = '알맞은 계산식을 입력해 주세요.'
	
	try:
		await bot.delete_message(ctx.message)
	except:
		pass
	await bot.say(ctx.message.author.mention+'님, '+result)

@bot.command(pass_context=True)
async def 골라(ctx, *args):
	result = random.choice(args)

	await bot.say(ctx.message.author.mention+'님, 저라면 **'+result+'**예요.')

@bot.command(pass_context=True)
async def 검색(ctx, *args):
	"""Daum 검색"""
	if len(args) > 0:
		result = funcs.daum_search(' '.join(args))
	else:
		result = '검색 키워드를 입력해 주세요.'
	
	await bot.say(ctx.message.author.mention+'님, 검색 결과예요!'+result)
@bot.command()
async def 실검():
	"""Daum 실시간 검색어 순위"""
	ranks = funcs.daum_realtime()
	link = 'https://search.daum.net/search?w=tot&q='
	time = funcs.korea_time_string()

	embed=discord.Embed(title="Daum 실시간 검색어 순위", url="https://www.daum.net/", description=time+' 기준', color=THEME_COLOR)
	for i in range(0, 10):
		embed.add_field(name=str(i+1)+'위', value='[{}]({})'.format(ranks[i], link+re.sub(' ', '%20', ranks[i])), inline=True if i > 0 else False)
	
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def 초성(ctx, *args):
	"""초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)"""
	cho_quiz = ChoQuiz.find(ctx.message.channel)
	
	if cho_quiz is not None and cho_quiz.answer is not None:
		result = '이미 진행중인 초성퀴즈가 있어요.'
	else:
		cho_quiz = ChoQuiz.start(ctx.message.channel)
		cho_quiz.genre = args[0] if len(args) > 0 else None
		cho_quiz.count = int(args[1]) if len(args) > 1 else 10
		
		if cho_quiz.genre not in ['영화', '음악', '동식물', '사전', '게임', '인물', '책']:
			result = '장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책'
		else: # 정상
			cho_quiz.answer = funcs.jaum_quiz(cho_quiz.genre) # 정답 생성
			result = funcs.cho(cho_quiz.answer)
	
	await bot.say(result) # 채널에 초성 공개
@bot.command(pass_context=True)
async def 초성끝(ctx):
	await bot.say(ChoQuiz.end(ctx.message.channel))

# End of commands

bot.run(TOKEN)
