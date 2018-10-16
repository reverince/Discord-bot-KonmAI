import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import datetime
import json
import random
import re

from funcs import *
import helps
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
            result = helps.ffxiv()
        else:
            result = '그런 도움말은 없어요.'

    else:
        result = helps.default()

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command(pass_context=True)
async def 더해(ctx, *args):
    try:
        result = sum(list(map(int, args)))
        result = ' + '.join(args) + ' = **' + str(result) + '**'
    except ValueError:
        result = please_enter_right()

    await delete_message(ctx.message)
    await bot.say(ctx.message.author.mention+'님, '+result)


@bot.command(pass_context=True)
async def 빼(ctx, *args):
    try:
        result = int(args[0]) - sum(list(map(int, args[1:])))
        result = ' - '.join(args) + ' = **' + str(result) + '**'
    except ValueError:
        result = please_enter_right()

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
            result = '정답은 [**' + cho_quiz.answer + '**]였어요. :hugging:'
            result += '\n' + cho_quiz.correct(channel)
        else:
            result = '진행중인 초성퀴즈가 없어요.'
    else:
        if cho_quiz is not None:
            result = '이미 진행중인 초성퀴즈가 있어요.'
        else:
            genre = args[0] if len(args) > 0 else None
            count = int(args[1]) if len(args) > 1 else 10

            answer = jaum_quiz(genre)  # 정답 생성
            if answer is not None:
                cho_quiz = ChoQuiz.start(channel, genre, count, answer)
                result = cho(answer)  # 초성 공개
            else:
                result = '장르는 `영화`, `음악`, `동식물`, `사전`, `게임`, `인물`, `책`이 있어요.'

    await bot.say(result)


'''
@bot.command()
async def 배그(*args):
    """dak.gg PUBG 프로필 검색"""
    if len(args) > 0:
        name = args[0]
        result = pubg_profile(name)
    else:
        result = please_enter_keyword('아이디')

    if type(result) is str:
        await bot.say(result)
    else:  # embed
        await bot.say(embed=result)
'''


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
        result = please_enter_keyword('제조시간')

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
        if args[0].isdigit() and int(args[0]) > 0:
            if channel not in lots_games.keys():
                lots_cnt = int(args[0])
                lots_games[channel] = [True] + [False] * (lots_cnt - 1)
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
            result = please_enter_right()
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
async def 리볼버(ctx, *args):
    """Credit for Floppy Disk Bot(💾❗)"""
    BEFORE_FACES = [':confounded:', ':grimacing:', ':persevere:', ':tired_face:']
    AFTER_FACES = [':disappointed:', ':relieved:', ':smirk:', ':sweat_smile:', ':wink:']

    result = None
    channel = ctx.message.channel
    if len(args) > 0:
        if args[0].isdigit() and int(args[0]) > 0:
            if channel not in revolvers.keys():
                bullet_cnt = int(args[0])
                revolvers[channel] = [True] * bullet_cnt + \
                                     [False] * (6 - bullet_cnt)
                random.shuffle(revolvers[channel])
                result = '리볼버를 장전했어요. :gun::gear:'
            else:
                result = '이미 장전된 리볼버가 있어요. :gun:' + bignumrize(len(revolvers[channel]))
        elif args[0] == '끝':
            if channel in revolvers.keys():
                del revolvers[channel]
                result = '리볼버 장전을 해제했어요.'
            else:
                result = '장전된 리볼버가 없어요.'
        else:
            result = please_enter_right()
    else:
        if channel not in revolvers.keys():
            result = '먼저 리볼버를 장전해 주세요.'
        else:
            shot = revolvers[channel].pop()
            mention = ctx.message.author.mention
            shot_msg = await bot.say(mention + ' → ' + random.choice(BEFORE_FACES) + ':gun:')
            await asyncio.sleep(1)
            if shot:
                del revolvers[channel]
                message = mention + ' → :skull::gun::boom:'
            else:
                message = mention + ' → ' + random.choice(AFTER_FACES) + ':gun::speech_balloon:'
            await bot.edit_message(shot_msg, message)

    if result is not None:
        await bot.say(result)


@bot.command(pass_context=True)
async def 알람(ctx, *args):
    """특정 시각 혹은 일정 시간 후 멘션"""
    if len(args) > 0:
        channel = ctx.message.channel
        author = ctx.message.author
        msg = None
        if len(args) > 1:
            msg = ' '.join(args[1:])
        if args[0].isdigit():
            time_sec = int(args[0])
            await alarm_after(time_sec, channel, author, msg)
        elif ':' in args[0]:
            search = re.search('(.+):(.+)', args[0])
            try:
                hour = int(search.group(1))
                minute = int(search.group(2))
                if hour < 0 or minute < 0 or hour >= 24 or minute >= 60:
                    raise ValueError
                await alarm_at(hour, minute, channel, author, msg)
            except (ValueError, AttributeError):
                await bot.say(please_enter_right())
        else:
            await bot.say(please_enter_right())
    else:
        await bot.say('시간을 입력해 주세요.')


@bot.command(pass_context=True)
async def 기억(ctx, *args):
    """MEMORY_FILE에 입력값 기억."""
    result = memory(ctx.message.author, *args)

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 포네틱(*args):
    """포네틱 코드로 변환"""
    result = phonetic(*args)

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command(pass_context=True)
async def 결투(ctx, *args):
    """BANG"""
    global duels
    server = ctx.message.server
    channel = ctx.message.channel
    author = ctx.message.author
    if type(channel) is discord.PrivateChannel:
        result = '개인 메시지에서는 실행할 수 없어요.'
    elif len(args) > 0:
        target = ' '.join(args)
        members = list(server.members)
        member_names = [m.name for m in members]
        if target in member_names:
            idx = member_names.index(target)
            target = members[idx]
            duels[target] = {'vs': author, 'status': 'request'}
            await delete_message(ctx.message)
            result = author.mention + '님이 ' + target.mention + \
                '님에게 결투를 신청했어요! 도전에 응하시겠어요? (`~Y`/`~N`)'
        else:
            result = '상대를 찾지 못했어요.'
    else:
        result = '듀얼 상대를 정해 주세요.'

    await bot.say(result)


@bot.command(pass_context=True)
async def Y(ctx):
    global duels
    result = None
    channel = ctx.message.channel
    author = ctx.message.author
    if author in duels:
        # TODO: 오래 지난 결투 도전 무시
        await delete_message(ctx.message)
        msg = author.mention + '님이 ' + duels[author]['vs'].mention + \
            '님의 결투 도전에 응했어요!\n제가 셋을 세면 `~BANG`하세요!'
        await bot.send_message(channel, msg)
        await duel_game(channel, author)
    else:
        result = ':question:'

    if result is not None:
        await bot.say(result)


@bot.command(pass_context=True)
async def N(ctx):
    global duels
    author = ctx.message.author
    if author in duels:
        await delete_message(ctx.message)
        result = author.mention + '님이 ' + duels[author]['vs'].mention + \
            '님의 결투 도전을 받아들이지 않았어요. :unamused:'
        del duels[author]
    else:
        result = ':question:'

    await bot.say(result)


@bot.command(pass_context=True)
async def BANG(ctx):
    global duels
    duel = None
    channel = ctx.message.channel
    author = ctx.message.author
    challengers = [dv['vs'] for dv in duels.values()]
    if author in duels:
        duel = duels[author]
        target = duel['vs']
        is_author_challenger = False
    elif author in challengers:
        target = [k for k, v in duels.items() if v['vs'] == author][0]
        duel = duels[target]
        is_author_challenger = True
    else:
        result = author.mention + '님, 아무데서나 총을 쏘면 못 써요. :triumph:'

    if duel is not None:
        if duel['status'] == 'request':
            result = 'request'
        elif duel['status'] == 'ready':
            result = author.mention + '님의 총알이 빗나갔어요!'
        elif duel['status'] == 'start':
            result = author.mention + '님의 총알이 ' + target.mention + '님을 관통했어요! :confetti_ball:'
            await duel_end(channel, target if is_author_challenger else author)
        elif duel['status'] == 'end':
            result = author.mention + '님이 늦었어요!'

    await bot.say(result)


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
            result = NO_SUCH_COMMAND_MESSAGE
    else:
        result = WHAT_TO_DO_MESSAGE

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
                result = '` ~코인 이체 [상대방] [금액] `처럼 입력해 주세요.'
        else:
            result = NO_SUCH_COMMAND_MESSAGE
    else:
        result = WHAT_TO_DO_MESSAGE

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
        result = please_enter_keyword

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 레시피(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.recipe(keyword)
    else:
        result = please_enter_keyword

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 마물(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.elite(keyword)
    else:
        result = please_enter_keyword

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 상점(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.seller(keyword)
    else:
        result = please_enter_keyword

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 의뢰(*args):
    if len(args) > 0:
        if args[-1].isdigit():
            job = 'mercernary'
            level = int(args[-1])
            if len(args) == 2:
                if args[0] in ffxiv.CRAFTERS + ffxiv.GATHERERS + ['채집', '제작']:
                    job = 'gathering'
            result = ffxiv.guild_quest(level, job)
        else:
            result = please_enter_right()
    else:
        result = please_enter_keyword('레벨')

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 잡퀘(*args):
    if len(args) == 1:
        keyword = args[0]
        result = ffxiv.job_quest(keyword)
    else:
        result = please_enter_keyword('잡 이름')

    await bot.say(result)


@bot.command()
async def 장비(*args):
    if len(args) == 2:
        job = args[0]
        if args[1].isdigit():
            level = int(args[1])
            result = ffxiv.tool(job, level)
        else:
            result = please_enter_right()
    else:
        result = please_enter_keyword('잡 이름과 레벨')

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 채집(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.gathering(keyword)
    else:
        result = please_enter_keyword()

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 토벌(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.hunting(keyword)
    else:
        result = please_enter_keyword('몬스터 이름')

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


@bot.command()
async def 풍맥(*args):
    if len(args) > 0:
        keyword = ' '.join(args)
        result = ffxiv.wind(keyword)
    else:
        result = please_enter_keyword('지역 이름')

    await (bot.say(result) if type(result) is str else bot.say(embed=result))


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
            await bot.say('Not Found')
    else:
        await bot.say(ctx.message.author.id)


@bot.command()
async def find_name(*args):
    result = find_name_by_id(args[0])
    if result:
        await bot.say(result)
    else:
        await bot.say('Not Found')


@bot.command(pass_context=True)
async def print_log(ctx, *args):
    channel = ctx.message.channel
    limit = int(args[0]) if len(args) > 0 and args[0].isdigit() else 10
    result = []
    async for message in bot.logs_from(channel, limit=limit):
        if message.author != bot:
            result.append(message.author.name + ': ' + message.content)
    result = '\n'.join(result[::-1])
    await bot.say(result)


# End of commands


bot.run(TOKEN)
