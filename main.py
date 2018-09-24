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
import ffxiv


# Events


@bot.event
async def on_ready():
    server_names = [s.name for s in bot.servers]
    member_names = [m.name for m in set(bot.get_all_members())]
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
        if re.sub(' ', '', message.content) == re.sub(' ', '', cho_quiz.answer):
            await bot.send_message(channel, '**{}**님의 [**{}**] 정답! :white_check_mark:'.format(message.author.mention, cho_quiz.answer))
            result = cho_quiz.correct(channel)
            await bot.send_message(channel, result)

    await bot.process_commands(message)  # 커맨드 처리


# Commands


@bot.command()
async def 도움(*args):
    """ㄴㄱ ㄴㄱㄴㄱ?"""

    if len(args) > 0:
        if args[0] == '파판':
            result = discord.Embed(description='FFXIV 관련 명령어를 모아 놓았어요쿠뽀.', color=THEME_COLOR)
            result.set_author(name=BOTNAME, url=URL, icon_url=ICON_URL)
            result.add_field(name='`공식',
                             value='[공식 가이드](http://guide.ff14.co.kr/lodestone) 검색 링크를 만들어요. ` `공식 제멜 토마토 `')
            result.add_field(name='`레시피',
                             value='공식 가이드에서 아이템 제작 레시피를 검색해요. ` `레시피 고리갑옷 `')
            result.add_field(name='`마물',
                             value='[인벤](http://ff14.inven.co.kr)에서 마물 정보를 검색해요. ` `마물 아스왕 `')
            result.add_field(name='`상점',
                             value='공식 가이드에서 아이템 판매 NPC를 검색해요. ` `상점 질긴 가죽 `')
            result.add_field(name='`의뢰',
                             value='해당 레벨의 용병업 의뢰를 받을 수 있는 곳을 알려 드려요. ` `의뢰 35 `')
            result.add_field(name='`잡퀘',
                             value='잡 퀘스트 NPC 위치를 알려 드려요. ` `잡퀘 전사`\n창천, 홍련 추가 직업은 아직 지원되지 않아요.')
            result.add_field(name='`채집',
                             value='공식 가이드에서 채집 위치정보를 검색해요. ` `채집 황혼비취 `')
            result.add_field(name='`토벌',
                             value='인벤에서 토벌수첩 몬스터가 어디 있는지 찾아 드려요. ` `토벌 무당벌레 `')
            result.add_field(name='`풍맥',
                             value='공식 가이드에서 풍맥의 샘 위치를 검색해요. ` `풍맥 홍옥해 `\n풍맥 퀘스트는 아직이에요.')

        else:
            result = '그런 도움말은 없어요.'

    else:
        result = discord.Embed(description='만나서 반가워요.', color=THEME_COLOR)
        result.set_author(name=BOTNAME, url=URL, icon_url=ICON_URL)
        result.add_field(name='`더해',
                         value='주어진 수들을 덧셈해 드려요. (무료)', inline=True)
        result.add_field(name='`빼',
                         value='처음 수에서 나머지 수를 뺄셈해요.', inline=True)
        result.add_field(name='`계산',
                         value='(이 정도 쯤이야.)', inline=True)
        result.add_field(name='`골라',
                         value='배그할까 레식할까? ` `골라 배그 레식 `', inline=True)
        result.add_field(name='`초성',
                         value='초성퀴즈를 할 수 있어요. (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)\n` `초성 게임 5 `처럼 사용하세요. 끝내려면 ` `초성 끝 `을 입력하세요.\n(유저 등록 개발중)', inline=True)
        result.add_field(name='`배그',
                         value='[dak.gg](https://dak.gg)에서 배틀그라운드 전적을 찾아요.', inline=True)
        result.add_field(name='`소전',
                         value='제조 시간을 입력하시면 등장하는 전술인형 종류를 알려 드려요.\n` `소전 03:40 `처럼 사용하세요.', inline=True)
        result.add_field(name='`주사위',
                         value='주사위를 던져요.\n` `주사위 2d6 `처럼 사용하세요.', inline=True)
        result.add_field(name='`제비',
                         value='당첨이 한 개 들어 있는 제비를 준비해요.\n` `제비 3 `처럼 시작하고 ` `제비 `로 뽑으세요.\n취소하려면 ` `제비 끝 `을 입력하세요.', inline=True)
        #result.add_field(name='`알람',
        #                 value='특정 시각 혹은 일정 시간 후에 메시지와 함께 멘션해 드려요. ` `알람 23:59 자라 ` ` `알람 240 컵라면 `')
        result.add_field(name='`기억',
                         value='키워드에 관한 내용을 DB에 기억해요.\n` `기억 원주율 3.14159265 `로 기억에 남기고 ` `기억 원주율 `로 불러오세요.\n` `기억 랜덤 `을 입력하면 아무 기억이나 불러와요.\n` `기억 삭제 원주율`로 기억을 지울 수 있어요.', inline=True)
        '''
        result.add_field(name='`게이머 (WIP)',
                         value='게이머 관련 업무를 수행해요. `등록` / `나`', inline=True)
        result.add_field(name='`코인 (WIP)',
                         value='게이머 코인 관련 업무를 수행해요. `초기화` / `이체`', inline=True)
        '''
        result.add_field(name='`블랙잭',
                         value='저와 블랙잭 승부를 겨루실 수 있어요. 히트는 ` `H `, 스탠드는 ` `S `를 입력하세요.\n코인을 걸 수 있어요.', inline=True)
        # 빈칸
        result.add_field(name='\u200B', value='\u200B')
        # 파판 명령어 도움
        result.add_field(name='`도움 파판',
                         value='FFXIV 관련 명령어를 알려드려요.')

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command(pass_context=True)
async def 더해(ctx, *args):
    try:
        result = sum(list(map(int, args)))
        result = ' + '.join(args) + ' = **' + str(result) + '**'
    except ValueError:
        result = ENTER_DIGIT_MESSAGE

    await delete_message(ctx.message)
    await bot.say(ctx.message.author.mention+'님, '+result)


@bot.command(pass_context=True)
async def 빼(ctx, *args):
    try:
        result = int(args[0]) - sum(list(map(int, args[1:])))
        result = ' - '.join(args) + ' = **' + str(result) + '**'
    except ValueError:
        result = ENTER_DIGIT_MESSAGE

    await delete_message(ctx.message)
    await bot.say(ctx.message.author.mention+'님, '+result)


@bot.command(pass_context=True)
async def 계산(ctx, *args):
    try:
        result = ' '.join(args) + ' = **' + str(eval(''.join(args))) + '**'
    except ZeroDivisionError:
        result = '아무래도 0으로 나눌 수는 없어요. :thinking:'
    except SyntaxError:
        result = '알맞은 계산식을 입력해 주세요.'

    await delete_message(ctx.message)
    await bot.say(ctx.message.author.mention+'님, '+result)


@bot.command(pass_context=True)
async def 골라(ctx, *args):
    CHOICE_MESSAGES = ['**'+choice+'**'+josa(choice, '가')+' 어떨까요? :thinking:',
                       '저라면 **'+choice+'**예요.',
                       '저는 **'+choice+'**'+josa(choice, '를')+' 추천할게요! :relaxed:',
                       '저라면 **'+choice+'**'+josa(choice, '를')+' 선택하겠어요. :relaxed:',
                       '**'+choice+'**'+josa(choice, '로')+' 가죠. :sunglasses:',
                       '답은 **'+choice+'**'+josa(choice, '로')+' 정해져 있어요. :sunglasses:']
    if len(args) > 1:
        choice = random.choice(args) if '히오스' not in args else '히오스'
        msg = random.choice(CHOICE_MESSAGES)
        result = ctx.message.author.mention+'님, ' + msg
    elif len(args) == 1:
        result = ':sweat:'
    else:
        result = '어떤 것들 중에서 고를지 다시 알려주세요.'

    await bot.say(result)


@bot.command(pass_context=True)
async def 초성(ctx, *args):
    """초성퀴즈 (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)"""
    channel = ctx.message.channel
    cho_quiz = ChoQuiz.find(channel)

    if len(args) == 1 and args[0] == '끝':
        result = ChoQuiz.end(channel)
    elif len(args) == 1 and args[0] == '패스':
        if cho_quiz is not None:
            result = '정답은 [**' + cho_quiz.answer + '**]였어요. :hugging:\n' + cho_quiz.correct(channel)
        else:
            result = '진행중인 초성퀴즈가 없어요.'
    elif len(args) > 0 and args[0] == '등록':  # 사용자 초성퀴즈 등록
        result = ChoQuiz.add_custom(ctx.message.author, args[1:])
    else:
        if cho_quiz is not None:
            result = '이미 진행중인 초성퀴즈가 있어요.'
        else:
            genre = args[0] if len(args) > 0 else None
            count = int(args[1]) if len(args) > 1 else 10

            if genre not in ['영화', '음악', '동식물', '사전', '게임', '인물', '책']:
                result = '장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책'
            else:  # OK
                answer = jaum_quiz(genre)  # 정답 생성
                cho_quiz = ChoQuiz.start(channel, genre, count, answer)
                result = cho(answer)  # 초성 공개

    await bot.say(result)


@bot.command()
async def 배그(*args):
    """dak.gg PUBG 프로필 검색"""
    if len(args) > 0:
        name = args[0]
        ratings = pubg_profile(name)
        year = str(time.gmtime().tm_year)
        month = str(time.gmtime().tm_mon)
        if len(month) < 2:
            month = '0' + month

        if ratings is not None:
            result = discord.Embed(title=name,
                                   description='시즌: '+year+'-'+month, color=THEME_COLOR)
            result.set_author(name='PUBG 솔로 전적 by dak.gg',
                              url='https://dak.gg/profile/'+name+'/'+year+'-'+month+'/krjp', icon_url=ICON_URL)
            result.set_thumbnail(url=ratings['avatar'])
            result.add_field(name='플레이타임',
                             value=re.sub('hours', '시간', re.sub('mins', '분', ratings['solo-playtime'])), inline=True)
            result.add_field(name='기록',
                             value=re.sub('W', '승 ', re.sub('T', '탑 ', re.sub('L', '패', ratings['solo-record']))), inline=True)
            result.add_field(name='등급',
                             value=ratings['solo-grade'], inline=True)
            result.add_field(name='점수',
                             value=f'{ratings["solo-score"]} ({ratings["solo-rank"]})', inline=True)
            result.add_field(name='승점',
                             value=f'{ratings["solo-win-rating"]} ({ratings["solo-win-top"]})', inline=True)
            result.add_field(name='승률',
                             value=f'{ratings["solo-winratio"]} ({ratings["solo-winratio-top"]})', inline=True)
            result.add_field(name='TOP10',
                             value=f'{ratings["solo-top10"]} ({ratings["solo-top10-top"]})', inline=True)
            result.add_field(name='여포',
                             value=f'{ratings["solo-kill-rating"]} ({ratings["solo-kill-top"]})', inline=True)
            result.add_field(name='K/D',
                             value=f'{ratings["solo-kd"]} ({ratings["solo-kd-top"]})', inline=True)
            result.add_field(name='평균 데미지',
                             value=f'{ratings["solo-avgdmg"]} ({ratings["solo-avgdmg-top"]})', inline=True)
            result.add_field(name='최대 킬',
                             value=f'{ratings["solo-mostkills"]} ({ratings["solo-mostkills-top"]})', inline=True)
            result.add_field(name='헤드샷',
                             value=f'{ratings["solo-headshots"]} ({ratings["solo-headshots-top"]})', inline=True)
            result.add_field(name='저격',
                             value=f'{ratings["solo-longest"]} ({ratings["solo-longest-top"]})', inline=True)
            result.add_field(name='게임 수',
                             value=f'{ratings["solo-games"]} ({ratings["solo-games-top"]})', inline=True)
            result.add_field(name='생존',
                             value=f'{ratings["solo-survived"]} ({ratings["solo-survived-top"]})', inline=True)

            await bot.say(embed=result)
        else:
            await bot.say('아이디 검색에 실패했어요.')
    else:
        await bot.say('아이디를 입력해 주세요.')


@bot.command()
async def 소전(*args):
    """소녀전선 제조시간 검색"""
    if len(args) > 0:
        if len(args[0]) in [3, 4]:
            pd_time = args[0]
            result = gf_time(pd_time)
        else:
            result = '제조시간을 `340` 혹은 `0340`처럼 입력해 주세요.'
    else:
        result = enter_message('제조시간')

    await bot.say(result)


@bot.command(pass_context=True)
async def 주사위(ctx, *args):
    if len(args) > 0:
        cnt, side = [int(x) for x in args[0].split('d')]
    else:  # 2d6
        cnt, side = 2, 6
    result = roll_dice(cnt, side, ctx.message.author.mention)

    await delete_message(ctx.message)
    await bot.say(result)


@bot.command(pass_context=True)
async def 제비(ctx, *args):
    channel = ctx.message.channel

    if len(args) > 0:
        if args[0].isdigit():
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
            result = ctx.message.author.mention + '님, '
            if lot:
                del lots_games[channel]
                result += '**당첨**! :tada:'
            else:
                result += '꽝. :smirk:'

    await bot.say(result)


@bot.command(pass_context=True)
async def 기억(ctx, *args):
    """MEMORY_FILE에 입력값 기억."""
    result = memory(ctx.message.author, *args)

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


# Commands for GAMER


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
    """게이머 코인 데이터 관련 업무"""
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
async def 블랙잭(ctx, *args):
    global bj_games
    player = ctx.message.author
    game_started = True
    if player not in bj_games.keys():
        if len(args) > 0 and args[0].isnumeric():
            bet = int(args[0])
            if Gamer.find(player.id):
                if Gamer.check_coin(player.id, bet):
                    Gamer.remove_coin(player.id, bet)
                    bj_games[player] = Blackjack(player, bet)
                else:
                    await bot.say('등록되지 않은 게이머거나 잔액이 부족해요.')
            else:
                game_started = False
                await bot.say('등록되지 않은 게이머예요.')
        else:
            bj_games[player] = Blackjack(player)

        if game_started:
            game = discord.Game(name=player.name+josa(player.name, '과')+' 블랙잭')
            await bot.change_presence(game=game)
            bj_msgs[player] = await bot.say(bj_games[player])
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
        await delete_message(ctx.message)

        bj_games[player].p_draw()
        await asyncio.sleep(1.0)
        await bot.edit_message(bj_msgs[player], bj_games[player])

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
        await delete_message(ctx.message)

        await blackjack_dturn(player, channel)
    else:
        await bot.say('진행 중인 게임이 없어요.')


# Commands for FFXIV


@bot.command()
async def 공식(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.guide(keyword)
    else:
        result = ENTER_KEYWORD_MESSAGE

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 레시피(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.recipe(keyword)
    else:
        result = ENTER_KEYWORD_MESSAGE

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 마물(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.elite(keyword)
    else:
        result = ENTER_KEYWORD_MESSAGE

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 상점(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.seller(keyword)
    else:
        result = ENTER_KEYWORD_MESSAGE

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 의뢰(*args):
    if len(args) > 0:
        if len(args) == 1:
            if args[0].isdigit():
                level = int(args[0])
                result = ffxiv.guild_quest(level)
            else:
                result = ENTER_DIGIT_MESSAGE
        else:
            result = ':confused:'
    else:
        result = enter_message('레벨')

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 잡퀘(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.job_quest(keyword)
    else:
        result = enter_message('잡 이름')

    await bot.say(result)


@bot.command()
async def 채집(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.gathering(keyword)
    else:
        result = ENTER_KEYWORD_MESSAGE

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 토벌(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.hunting(keyword)
    else:
        result = enter_message('몬스터 이름')

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


@bot.command()
async def 풍맥(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.wind(keyword)
    else:
        result = enter_message('지역 이름')

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)


# Commands for DEBUG


@bot.command(pass_context=True)
async def find_id(ctx, target=None):
    if target:
        members = list(bot.get_all_members())
        member_names = list(map(lambda x: x.name, members))
        if target in member_names:
            i = member_names.index(target)
            await bot.say(members[i].id)
        else:
            await bot.say('not found')
    else:
        await bot.say(ctx.message.author.id)


@bot.command()
async def find_name(*args):
    result = find_name_by_id(args[0])
    if result:
        await bot.say(result)


@bot.command(pass_context=True)
async def print_log(ctx):
    channel = ctx.message.channel
    result = []
    async for message in bot.logs_from(channel, limit=10):
        if message.author == ctx.message.author:
            result.append(re.sub('`', '', message.content))
    result = '```' + '\n'.join(result[::-1]) + '```'
    await bot.say(result)


# End of commands


bot.run(TOKEN)
