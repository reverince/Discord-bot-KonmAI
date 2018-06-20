import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import datetime
import json
import random
import re
import time

from funcs import *

TOKEN = '' # SECURE!!!

bot = Bot(description=DESCRIPTION, command_prefix=PREFIX)

async def blackjack_dturn(player, channel): # Dealer's turn
	while True:
		if bj_games[player].dsum < 17: # 딜러 히트
			await asyncio.sleep(1.0)
			if bj_games[player].cnt_dhit > 0:
				await bot.send_message(channel, random.choice(Blackjack.HIT_MESSAGES + Blackjack.HIT_MESSAGES_MORE))
			else:
				await bot.send_message(channel, random.choice(Blackjack.HIT_MESSAGES + Blackjack.HIT_MESSAGES_FIRST))
			bj_games[player].cnt_dhit += 1
			bj_games[player].ddraw()
			await asyncio.sleep(1.0)
			if bj_games[player].dsum > 21:
				await asyncio.sleep(1.0)
				await bot.send_message(channel, bj_games[player].result())
				await asyncio.sleep(0.5)
				await bot.send_message(channel, random.choice(Blackjack.BUST_MESSAGES_DEALER))
				await bot.change_presence(game=discord.Game(name=GAME))
				del bj_games[player]
				break
			else:
				await bot.send_message(channel, bj_games[player])
		else: # 딜러 스탠드
			await asyncio.sleep(1.0)
			if bj_games[player].cnt_dhit > 0:
				await bot.send_message(channel, random.choice(Blackjack.STAND_MESSAGES + Blackjack.STAND_MESSAGES_HIT))
			else:
				await bot.send_message(channel, random.choice(Blackjack.STAND_MESSAGES + Blackjack.STAND_MESSAGES_NOHIT))
			break
	if player in bj_games.keys():
		await asyncio.sleep(1.0)
		await bot.send_message(channel, bj_games[player].result())
		await asyncio.sleep(1.0)
		if bj_games[player].psum > bj_games[player].dsum:
			await bot.send_message(channel, random.choice(Blackjack.WIN_MESSAGES_PLAYER))
		elif bj_games[player].psum < bj_games[player].dsum:
			await bot.send_message(channel, random.choice(Blackjack.WIN_MESSAGES_DEALER))
		else:
			await bot.send_message(channel, random.choice(Blackjack.DRAW_MESSAGES))
		await bot.change_presence(game=discord.Game(name=GAME))
		del bj_games[player]

# Events

@bot.event
async def on_ready():
	server_names = [s.name for s in bot.servers]
	member_names = [m.name for m in set(bot.get_all_members())]
	#member_names.remove('KonmAI')
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
			result = cho_quiz.correct(channel)
			await bot.send_message(channel, result)
		
	await bot.process_commands(message) # 커맨드 처리

# Commands

@bot.command()
async def 도움():
	"""ㄴㄱ ㄴㄱㄴㄱ?"""
	embed = discord.Embed(description='만나서 반가워요.', color=THEME_COLOR)
	embed.set_author(name=NAME, url=URL, icon_url=ICON_URL)
	embed.add_field(name='`더해', value='주어진 수들을 덧셈해 드려요. (무료)', inline=True)
	embed.add_field(name='`빼', value='처음 수에서 나머지 수를 뺄셈해요.', inline=True)
	embed.add_field(name='`계산', value='(이 정도 쯤이야.)', inline=True)
	embed.add_field(name='`골라', value='배그할까 레식할까? ` `골라 배그 레식 `', inline=True)
	embed.add_field(name='`사전', value='[Daum](https://daum.net) 사전에서 검색해요.', inline=True)
	embed.add_field(name='`실검', value='Daum 실시간 검색어 순위를 알려 드려요.', inline=True)
	embed.add_field(name='`로또', value='Daum에서 로또 당첨 번호를 검색해요.\n` `로또 800 `처럼 회차를 지정할 수 있어요.', inline=True)
	embed.add_field(name='`환율', value='Daum에서 환율을 검색해요.', inline=True)
	embed.add_field(name='`초성', value='초성퀴즈를 할 수 있어요. (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)\n` `초성 게임 5 `처럼 사용하세요. 끝내려면 ` `초성 끝 `을 입력하세요. (유저 등록 개발중)', inline=True)
	embed.add_field(name='`배그 (WIP)', value='[dak.gg](https://dak.gg)에서 배틀그라운드 전적을 찾아요.', inline=True)
	embed.add_field(name='`소전', value='제조 시간을 입력하시면 등장하는 전술인형 종류를 알려 드려요.\n` `소전 03:40 `처럼 사용하세요.', inline=True)
	embed.add_field(name='`게이머 (WIP)', value='게이머 관련 업무를 수행해요.', inline=True)
	embed.add_field(name='`코인 (WIP)', value='게이머 코인 관련 업무를 수행해요.', inline=True)
	embed.add_field(name='`블랙잭', value='저와 블랙잭 승부를 겨루실 수 있어요. 히트는 ` `H `, 스탠드는 ` `S `를 입력하세요.', inline=True)
	embed.add_field(name='`주사위', value='주사위를 던져요.\n` `주사위 2d6 `처럼 사용하세요.', inline=True)
	embed.add_field(name='`제비', value='당첨이 한 개 들어 있는 제비를 준비해요.\n` `제비 3 `처럼 시작하고 ` `제비 `로 뽑으세요.\n취소하려면 ` `제비 끝 `을 입력하세요.', inline=True)
	embed.add_field(name='`운세 (WIP)', value='오늘의 운세를 점쳐볼 수 있어요.', inline=True)
	embed.add_field(name='`기억', value='키워드에 관한 내용을 DB에 기억해요.\n` `기억 원주율 3.14159265 `로 기억에 남기고 ` `기억 원주율 `로 불러오세요.\n` `기억 랜덤 `을 입력하면 아무 기억이나 불러와요.', inline=True)

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
	tm = time.gmtime()
	tm_str = '{}년 {}월 {}일 {}:{}:{}'.format(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour+9, tm.tm_min, tm.tm_sec)

	embed=discord.Embed(title='Daum 실시간 검색어 순위', url="https://www.daum.net/", description=tm_str+' 기준', color=THEME_COLOR)
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
@bot.command()
async def 환율(*args):
	"""Daum 환율 검색"""
	if len(args) > 0:
		keyword = ' '.join(args)
		won = daum_exchange(keyword)
		if won is not None:
			result = keyword+josa(keyword, '는')+' '+str(won)+'원이에요.'
		else:
			result = '결과를 찾지 못했어요.'
	else:
		result = '원으로 바꿀 금액과 단위를 입력해 주세요.'

	await bot.say(result)

@bot.command(pass_context=True)
async def 초성(ctx, *args):
	"""초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)"""
	channel = ctx.message.channel
	cho_quiz = ChoQuiz.find(channel)
	
	if len(args) > 0 and args[0] == '끝':
		result = ChoQuiz.end(channel)
	elif len(args) > 0 and args[0] == '등록': # 사용자 초성퀴즈 등록
		result = ChoQuiz.add_custom(ctx.message.author, args[1:])
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
				result = cho(answer) # 초성 공개
	
	await bot.say(result)

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

			await bot.say(gf_times(pd_time))
	else:
		await bot.say('제조시간을 입력해 주세요.')

@bot.command(pass_context=True)
async def 게이머(ctx, *args):
	"""게이머 데이터 관련 업무"""
	author = ctx.message.author

	if len(args) > 0:
		if args[0] == '등록':
			result = Gamer.init(author.id)
		elif args[0] == '나':
			result = Gamer.info(author.id)
		else:
			result = '그런 명령어는 없어요.'
	else:
		result = '어떤 일을 할까요?'
	
	await bot.say(author.mention+'님, '+result)
@bot.command(pass_context=True)
async def 코인(ctx, *args):
	"""플레이어 코인 데이터 관련 업무"""
	author = ctx.message.author

	if len(args) > 0:
		if args[0] == '초기화':
			result = Gamer.reset_coin(author.id)
		elif args[0] == '이체':
			if len(args) == 3:
				to_id = args[1]
				amount = int(args[2])
				result = Gamer.transfer_coin(author.id, to_id, amount)
			else:
				result = '` `코인 이체 [상대방] [금액] `처럼 입력해 주세요.'
		else:
			result = '그런 명령어는 없어요.'
	else:
		result = '어떤 일을 할까요?'
	
	await bot.say(author.mention+'님, '+result)

@bot.command(pass_context=True)
async def 블랙잭(ctx):
	global bj_games
	player = ctx.message.author

	if player not in bj_games.keys():
		bj_games[player] = Blackjack(player)
		await bot.change_presence(game=discord.Game(name=player.name+josa(player.name,'과')+' 블랙잭'))
		await bot.say(bj_games[player])
		if bj_games[player].psum == 21:
			await asyncio.sleep(0.5)
			await bot.say(random.choice(Blackjack.BLACKJACK_MESSAGES))
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
			await bot.say(random.choice(Blackjack.BUST_MESSAGES_PLAYER))
			del bj_games[player]
		elif bj_games[player].psum == 21:
			await asyncio.sleep(0.5)
			await bot.say(random.choice(Blackjack.BLACKJACK_MESSAGES))
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
async def 주사위(ctx, *args):
	try:
		if len(args) > 0:
			cnt, side = [int(x) for x in args[0].split('d')]
		else: # 2d6
			cnt, side = 2, 6
		
		result = []
		for _ in range(cnt):
			result.append(str(random.randint(1, side)))
		
		try:
			await bot.delete_message(ctx.message)
		except:
			pass
		await bot.say(ctx.message.author.mention+'님의 '+str(cnt)+'d'+str(side)+' 주사위 결과 : '+', '.join(result)+' ('+str(sum([int(x) for x in result]))+')')
	except ValueError:
		await bot.say('` `주사위 2d6 `처럼 입력해 주세요. 2는 주사위 개수, 6은 주사위 면수예요.')

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
	"""하루 한 번 오미쿠지"""
	
	author = ctx.message.author
	result = fortune(author)

	await bot.say(result)

@bot.command(pass_context=True)
async def 기억(ctx, *args):
	"""MEMORY_FILE에 입력값 기억."""
	result = memory(ctx.message.author, *args)

	if type(result) is str:
		await bot.say(result)
	else: # embed
		await bot.say(embed=result)

# Commands for DEBUG

@bot.command(pass_context=True)
async def MYID(ctx):
	await bot.say(ctx.message.author.id)
@bot.command()
async def MEM(*args):
	await bot.say(', '.join([m.name for m in [s.get_member(args[0]) for s in bot.servers]]))
@bot.command(pass_context=True)
async def LOG(ctx):
	channel = ctx.message.channel
	result = []
	async for message in bot.logs_from(channel, limit=10):
		if message.author == ctx.message.author:
			result.append(message.content)
	result = '\n'.join(result[::-1])
	await bot.say(result)

# End of commands

bot.run(TOKEN)
