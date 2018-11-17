import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import re
import requests

import funcs

CRAFTER_EQUIPMENT_FILE = 'FFXIV/crafter_equipment.json'
ELITE_FILE = 'FFXIV/elite.json'
GATHERER_EQUIPMENT_FILE = 'FFXIV/gatherer_equipment.json'
GUILD_QUEST_FILE = 'FFXIV/guild_quest.json'
HUNTING_FILE = 'FFXIV/hunting.json'
JOB_NPC_FILE = 'FFXIV/job_npc.json'
TOOL_FILE = 'FFXIV/tool.json'

CRAFTERS = ['가죽공예가', '갑주제작사', '대장장이', '목수', '보석공예사', '연금술사', '요리사', '재봉사']
GATHERERS = ['광부', '어부', '원예가']

NO_RESULT_MESSAGE = '결과를 찾지 못했어요.'


# Commonly Used


def to_lodestone_href(keyword, option=None):
    LODESTONE_SEARCH_BASE = 'http://guide.ff14.co.kr/lodestone/search?keyword='
    ret = LODESTONE_SEARCH_BASE + funcs.to_url(keyword)
    if option:
        ret += '&search=' + option

    return ret


def search_lodestone(keyword, option=None):
    address = to_lodestone_href(keyword, option)
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/text()')

    if keyword in results:
        idx = results.index(keyword)
        href = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))
        return tree
    else:
        return None


# For Commands


def guide(keyword):  # 공식

    address = to_lodestone_href(keyword)
    desc = '[공식 가이드 **' + keyword + '** 검색 결과](' + address + ')'
    ret = funcs.make_embed(desc=desc, by_me=True)

    return ret


def recipe(keyword):  # 레시피

    tree = search_lodestone(keyword, 'recipe')
    if tree is not None:

        path = '//div[@class="view_base add_box"]'
        # cnts = ['3 ', '1 ']
        cnts = tree.xpath(path + '/ul[1]//li//p/text()')
        names = tree.xpath(path + '/ul[1]//li//p//b/a/text()')
        # 재료 크리스탈
        c_cnts = tree.xpath(path + '/ul[2]//li//p/text()')
        c_names = tree.xpath(path + '/ul[2]//li//p//b/a/text()')

        title = '**' + keyword + '**의 제작 레시피'
        desc = ''
        for i in range(len(names)):
            desc += f':small_orange_diamond: `{cnts[i]}` {names[i]}\n'
        for i in range(len(c_names)):
            desc += f':small_blue_diamond: `{c_cnts[i]}` {c_names[i]}\n'
        footer = '자료: 파이널판타지 14 공식 가이드'
        ret = funcs.make_embed(title=title,
                               desc=desc, by_me=True, footer=footer)
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def elite(keyword):  # 마물

    elites = funcs.read_json(ELITE_FILE)
    if keyword in elites:
        elite = elites[keyword]
        title = '마물 **' + keyword + '**'
        footer = '자료: 파이널 판타지 14 인벤'
        img = elite['img']
        ret = funcs.make_embed(title=title,
                               by_me=True, footer=footer, img=img)
        ret.add_field(name='등급', value=elite['grade'])
        ret.add_field(name='지역', value=elite['location'])
        ret.add_field(name='출현 주기', value=elite['period'])
        ret.add_field(name='소환 조건', value=elite['condition'])
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def seller(keyword):  # 상점

    tree = search_lodestone(keyword)
    if tree is not None:

        path = '//div[@class="view_base add_box"]/ul//li'
        npcs = tree.xpath(path + '/div[1]//p//b//text()')
        locations = tree.xpath(path + '/div[2]//p//text()')

        title = '**' + keyword + '** 판매 NPC'
        desc = ''
        for i in range(len(npcs)):
            desc += f':white_small_square: {npcs[i]} `{locations[i]}`\n'
        footer = '자료: 파이널판타지 14 공식 가이드'
        ret = funcs.make_embed(title=title,
                               desc=desc, by_me=True, footer=footer)
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def guild_quest(level, job='mercernary'):  # 의뢰

    guild_quests = funcs.read_json(GUILD_QUEST_FILE)

    ret = '길드 의뢰를 찾지 못했어요.'
    for lvl in range(level, 0, -1):
        lvl = str(lvl)
        if lvl in guild_quests:
            quest_type = '용병업' if job == 'mercernary' else '채집·제작업'
            title = '**' + lvl + '**레벨 ' + quest_type + ' 의뢰 수주 장소'
            desc = ''
            for loc in guild_quests[lvl][job]:
                desc += f':white_small_square: {loc}\n'
            ret = funcs.make_embed(title=title,
                                   desc=desc, by_me=True)
            break

    return ret


def job_quest(keyword):  # 잡퀘

    job_npcs = funcs.read_json(JOB_NPC_FILE)

    if keyword in job_npcs:
        name = job_npcs[keyword]['name']
        pos = job_npcs[keyword]['pos']
        ret = '**' + keyword + '**의 잡 퀘스트 NPC: ' + name + ' (' + pos + ')'
    else:
        ret = '그런 잡을 찾지 못했어요. :sweat_smile:'

    return ret


def tool(job, level):  # 장비

    tools = funcs.read_json(TOOL_FILE)
    gatherer_equipments = funcs.read_json(GATHERER_EQUIPMENT_FILE)

    if job in tools:
        value_main_tool = value_sub_tool = value_head = value_armor = \
            value_glove = value_waist = value_leg = value_boot = '?'

        has_found_main_tool = has_found_sub_tool = has_found_head = \
            has_found_armor = has_found_glove = has_found_waist = \
            has_found_leg = has_found_boot = False

        for lvl in range(level, 0, -1):
            lvl = str(lvl)
            if not has_found_main_tool and lvl in tools[job]['main']:
                value_main_tool = lvl
                main_tool = tools[job]['main'][lvl]
                value_main_tool += ' ' + main_tool['name']
                has_found_main_tool = True
            if not has_found_sub_tool and lvl in tools[job]['sub']:
                value_sub_tool = lvl
                sub_tool = tools[job]['sub'][lvl]
                if job != '어부':
                    value_sub_tool += sub_tool['name']
                else:
                    value_sub_tool += ', '.join(sub_tool['name'])
                has_found_sub_tool = True
            if job in GATHERERS:
                if not has_found_head and lvl in gatherer_equipments['head']:
                    value_head = lvl
                    head = gatherer_equipments['head'][lvl]
                    value_head += ' ' + head['name']
                    has_found_head = True
                if not has_found_armor and lvl in gatherer_equipments['armor']:
                    value_armor = lvl
                    armor = gatherer_equipments['armor'][lvl]
                    value_armor += ' ' + armor['name']
                    has_found_armor = True
                if not has_found_glove and lvl in gatherer_equipments['glove']:
                    value_glove = lvl
                    glove = gatherer_equipments['glove'][lvl]
                    value_glove += ' ' + glove['name']
                    has_found_glove = True
                if not has_found_waist and lvl in gatherer_equipments['waist']:
                    value_waist = lvl
                    waist = gatherer_equipments['waist'][lvl]
                    value_waist += ' ' + waist['name']
                    has_found_waist = True
                if not has_found_leg and lvl in gatherer_equipments['leg']:
                    value_leg = lvl
                    leg = gatherer_equipments['leg'][lvl]
                    value_leg += ' ' + leg['name']
                    has_found_leg = True
                if not has_found_boot and lvl in gatherer_equipments['boot']:
                    value_boot = lvl
                    boot = gatherer_equipments['boot'][lvl]
                    value_boot += ' ' + boot['name']
                    has_found_boot = True

        title = '**' + job + '**의 ' + str(level) + '레벨 장비'
        name_main = '주 도구' if job != '어부' else '낚싯대'
        name_sub = '보조 도구' if job != '어부' else '미끼'
        ret = funcs.make_embed(title=title, by_me=True)
        ret.add_field(name=name_main, value=value_main_tool)
        ret.add_field(name=name_sub, value=value_sub_tool)
        ret.add_field(name='머리', value=value_head)
        ret.add_field(name='갑옷', value=value_armor)
        ret.add_field(name='장갑', value=value_glove)
        ret.add_field(name='허리', value=value_waist)
        ret.add_field(name='다리', value=value_leg)
        ret.add_field(name='신발', value=value_boot)
    else:
        ret = '그런 잡을 찾지 못했어요. :sweat_smile:'

    return ret


def gathering(keyword):  # 채집

    # TODO
    for substr in ['샤드', '크리스탈', '클러스터']:
        if substr in keyword:
            return '샤드, 크리스탈, 클러스터는 검색할 수 없어요. :disappointed_relieved:'

    tree = search_lodestone(keyword, 'gathering')
    if tree is not None:
        path = '//div[@class="view_base bdb_n"]'
        regions = tree.xpath(path + '//p//span//text()')
        areas = tree.xpath(path + '//p//b//text()')
        locations = tree.xpath(path + '//text()')
        locations = [x.strip() for x in locations]
        # locations = ['위치 정보', ...]
        locations = list(filter(lambda x: len(x) > 0, locations))[1:]

        title = '**' + keyword + '**의 채집 장소'
        desc = ''
        for location in locations:
            if location in regions:
                location = '**' + location + '**'
            elif location in areas:
                location = '　' + location
            else:
                location = '　　`' + location + '`'
            desc += location + '\n'
        footer = '자료: 파이널판타지 14 공식 가이드'
        ret = funcs.make_embed(title=title,
                               desc=desc, by_me=True, footer=footer)
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def hunting(keyword):  # 토벌

    huntings = funcs.read_json(HUNTING_FILE)

    if keyword in huntings:
        pos = huntings[keyword]['pos']
        href = huntings[keyword]['href']
        img = huntings[keyword]['img']

        title = '**' + keyword + '** 출현 장소'
        desc = '[' + pos + '](' + href + ')'
        footer = '자료: 파이널판타지 14 인벤'
        ret = funcs.make_embed(title=title, desc=desc, footer=footer, img=img)
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def wind(keyword):  # 풍맥

    REGIONS_HEAVENSWARD = ['커르다스 서부고지', '고지 드라바니아', '드라바니아 구름바다', '아발라시아 구름바다', '저지 드라바니아', '아지스 라']
    REGIONS_STORMBLOOD = ['기라바니아 변방지대', '기라바니아 산악지대', '홍옥해', '얀샤', '아짐 대초원', '기라바니아 호반지대']

    address = 'http://guide.ff14.co.kr/map/'
    if keyword in REGIONS_HEAVENSWARD:
        address += 'heavensward/' + str(REGIONS_HEAVENSWARD.index(keyword) + 1)
    elif keyword in REGIONS_STORMBLOOD:
        address += 'stormblood/' + str(REGIONS_STORMBLOOD.index(keyword) + 1)
    else:
        return NO_RESULT_MESSAGE
    desc = '[공식 가이드 **' + keyword + '** 풍맥의 샘 지도](' + address + ')'
    ret = funcs.make_embed(desc=desc, by_me=True)

    return ret
