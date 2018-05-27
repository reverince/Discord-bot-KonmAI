import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import re

import funcs

TOKEN = 'NDQ3NTMxNTQ5MDMwODc1MTQw.DeI77g.05xLkyxDACaMkziyn3ZTwab6Lbs'
PREFIX = '`'
DESCRIPTION = ''
GAME = '도움말은 `help'
THEME_COLOR = 0x00a0ee

bot = Bot(description=DESCRIPTION, command_prefix=PREFIX, pm_help = True)

cho_genre = None
cho_answer = None
cho_cnt = None

def cho_end():
	global cho_genre, cho_answer, cho_cnt
	
	if cho_genre == None:
		result = '진행 중인 초성퀴즈가 없습니다.'
	else:
		cho_genre = None
		cho_answer = None
		cho_cnt = None
		result = '초성퀴즈를 종료했습니다.'

	return result

# Events

@bot.event
async def on_ready():
	print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ')')
	print('Connected to ' + str(len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
	print('Current Discord.py Version: {}'.format(discord.__version__))

	await bot.change_presence(game=discord.Game(name = GAME))

@bot.event
async def on_message(message):
	global cho_genre, cho_answer, cho_cnt
	if cho_genre is not None and cho_answer is not None:
		if message.content == cho_answer:
			await bot.send_message(message.channel, '**{}**님의 [**{}**] 정답! '.format(message.author.mention, cho_answer))
			cho_cnt -= 1
			if cho_cnt > 0:
				cho_answer = funcs.jaum_quiz(cho_genre)
				await bot.send_message(message.channel, funcs.cho(cho_answer))
			else:
				await bot.send_message(message.channel, cho_end())
	
	await bot.process_commands(message) # 커맨드 처리

# Commands

@bot.command()
async def 도움():
	"""ㄴㄱ ㄴㄱㄴㄱ?"""
	embed = discord.Embed(description='만나서 반갑습니다. 여기는 아직 만드는 중입니다...', color=THEME_COLOR)
	embed.set_author(name="KonmAI v0.3", url="https://daum.net", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
	embed.add_field(name='더해', value='주어진 수들을 덧셈해 드립니다. (무료)', inline=False)

	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def 더해(ctx, *args):
	"""주어진 수들을 덧셈해 드립니다. (무료)"""
	try:
		result = sum(list(map(int, args)))
		result = ' + '.join(args) + ' = **' + str(result) + '**'
	except ValueError:
		result = '숫자를 입력해 주시기 바랍니다.'
	
	await bot.delete_message(ctx.message)
	await bot.say(ctx.message.author.mention+'님, '+result)
@bot.command(pass_context=True)
async def 빼(ctx, *args):
	"""처음 수에서 나머지 수를 뺄셈해 드립니다."""
	try:
		result = int(args[0]) - sum(list(map(int, args[1:])))
		result = ' - '.join(args) + ' = **' + str(result) + '**'
	except ValueError:
		result = '숫자를 입력해 주시기 바랍니다.'
	
	await bot.delete_message(ctx.message)
	await bot.say(ctx.message.author.mention+'님, '+result)

@bot.command(pass_context=True)
async def 골라(ctx, *args):
	"""배그할까 레식할까?"""
	result = random.choice(args)

	await bot.say(ctx.message.author.mention+'님, 저라면 **'+result+'**입니다.')

@bot.command(pass_context=True)
async def 검색(ctx, *args):
	"""Daum 검색을 대신해 드립니다."""
	if len(args) > 0:
		result = funcs.daum_search(' '.join(args))
	else:
		result = '검색 키워드를 입력해 주시기 바랍니다.'
	
	await bot.say(ctx.message.author.mention+'님, '+result)

@bot.command()
async def 실검():
	"""Daum 실시간 검색어 순위를 알려드립니다."""
	ranks = funcs.daum_realtime()
	link = 'https://search.daum.net/search?w=tot&q='
	time = funcs.korea_time_string()

	embed=discord.Embed(title="Daum 실시간 검색어 순위", url="https://www.daum.net/", description=time+' 기준', color=THEME_COLOR)
	for i in range(0, 10):
		embed.add_field(name=str(i+1)+'위', value='[{}]({})'.format(ranks[i], link+re.sub(' ', '%20', ranks[i])), inline=True if i > 0 else False)
	
	await bot.say(embed=embed)

@bot.command()
async def 초성(*args):
	"""초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책) `초성 게임 5"""
	global cho_genre, cho_answer, cho_cnt
	
	if len(args) > 0:
		cho_genre = args[0]
	if len(args) > 1:
		cho_cnt = int(args[1])
	
	if cho_genre not in ['영화', '음악', '동식물', '사전', '게임', '인물', '책']:
		cho_genre = None
		await bot.say('장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책')
	else: # 정상
		cho_answer = funcs.jaum_quiz(cho_genre) # 정답 생성
		await bot.say(funcs.cho(cho_answer)) # 채널에 초성 공개

@bot.command()
async def 초성끝():
	"""초성퀴즈를 종료합니다."""
	cho_end()

	await bot.say(result)

# End of commands

bot.run(TOKEN)
