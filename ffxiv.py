import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import re
import requests

import funcs

JOB_NPC_FILE = 'FFXIV/job_npc.json'
HUNTING_FILE = 'FFXIV/hunting.json'

NO_RESULT_MESSAGE = '결과를 찾지 못했어요.'


# Commonly Used


def to_lodestone_href(keyword, option=None):
    LODESTONE_SEARCH_BASE = 'http://guide.ff14.co.kr/lodestone/search?keyword='
    ret = LODESTONE_SEARCH_BASE + funcs.to_url(keyword)
    if option:
        ret += '&search=' + option

    return ret


# For Commands


def guide(keyword):  # 공식

    address = to_lodestone_href(keyword)
    markdown = '[공식 가이드 **' + keyword + '** 검색 결과](' + address + ')'
    ret = discord.Embed(description=markdown, color=funcs.THEME_COLOR)
    ret.set_author(name=funcs.BOTNAME, url=funcs.URL, icon_url=funcs.ICON_URL)

    return ret


def recipe(keyword):  # 레시피

    address = to_lodestone_href(keyword, 'recipe')
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/text()')
    if keyword in results:
        idx = results.index(keyword)
        href = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))

        path = '//div[@class="view_base add_box"]'
        # cnts = ['3 ', '1 ']
        cnts = tree.xpath(path + '/ul[1]//li//p/text()')
        names = tree.xpath(path + '/ul[1]//li//p//b/a/text()')
        # 재료 크리스탈
        c_cnts = tree.xpath(path + '/ul[2]//li//p//text()')
        c_names = tree.xpath(path + '/ul[2]//li//p//b/a/text()')

        title = '**' + keyword + '**의 제작 레시피'
        desc = ''
        for i in range(len(names)):
            desc += ':small_orange_diamond: `' + cnts[i] + '` ' + names[i] + '\n'
        for i in range(len(c_names)):
            desc += ':small_blue_diamond: `' + c_cnts[i] + '` ' + c_names[i] + '\n'
        ret = discord.Embed(title=title,
                            description=desc, color=funcs.THEME_COLOR)
        ret.set_author(name=funcs.BOTNAME,
                       url=funcs.URL, icon_url=funcs.ICON_URL)
        ret.set_footer(text='자료: 파이널판타지 14 공식 가이드')
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def seller(keyword):  # 상점

    address = to_lodestone_href(keyword)
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/text()')
    if keyword in results:
        idx = results.index(keyword)
        href = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))

        path = '//div[@class="view_base add_box"]/ul//li'
        npcs = tree.xpath(path + '/div[1]//p//b//text()')
        locations = tree.xpath(path + '/div[2]//p//text()')

        title = '**' + keyword + '** 판매 NPC'
        desc = ''
        for i in range(len(npcs)):
            desc += ':white_small_square: ' + npcs[i] + ' `' + locations[i] + '`\n'
        ret = discord.Embed(title=title,
                            description=desc, color=funcs.THEME_COLOR)
        ret.set_author(name=funcs.BOTNAME,
                       url=funcs.URL, icon_url=funcs.ICON_URL)
        ret.set_footer(text='자료: 파이널판타지 14 공식 가이드')
    else:
        ret = NO_RESULT_MESSAGE

    return ret


def job_quest(keyword):  # 잡퀘

    job_npcs = funcs.read_json(JOB_NPC_FILE)
    print(keyword)

    if keyword in job_npcs:
        name = job_npcs[keyword]['name']
        pos = job_npcs[keyword]['pos']
        ret = '**' + keyword + '**의 잡 퀘스트 NPC: ' + name + ' (' + pos + ')'
    else:
        ret = '그런 잡을 찾지 못했어요. :sweat_smile:'

    return ret


def gathering(keyword):  # 채집

    for substr in ['샤드', '크리스탈', '클러스터']:
        if substr in keyword:
            return '샤드, 크리스탈, 클러스터는 검색할 수 없어요. :disappointed_relieved:'
    address = to_lodestone_href(keyword, 'gathering')
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/text()')
    if keyword in results:
        idx = results.index(keyword)
        href = tree.xpath('//div[@class="base_tb"]//tr/td[1]/a/@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))

        path = '//div[2]/div[2]/div[2]/div[2]/div[1]/div[2]'
        regions = tree.xpath(path + '//p//span//text()')
        areas = tree.xpath(path + '//p//b//text()')
        locations = tree.xpath(path + '//text()')
        locations = [x.strip() for x in locations]
        locations = list(filter(lambda x: len(x) > 0, locations))

        title = '**' + keyword + '**의 채집 장소'
        desc = ''
        for location in locations[1:]:
            if location in regions:
                location = '**' + location + '**'
            elif location in areas:
                location = '　' + location
            else:
                location = '　　`' + location + '`'
            desc += location + '\n'

        ret = discord.Embed(title=title,
                            description=desc, color=funcs.THEME_COLOR)
        ret.set_author(name=funcs.BOTNAME,
                       url=funcs.URL, icon_url=funcs.ICON_URL)
        ret.set_footer(text='자료: 파이널판타지 14 공식 가이드')
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
        ret = discord.Embed(title=title,
                            description=desc, color=funcs.THEME_COLOR)
        ret.set_footer(text='자료: 파이널판타지 14 인벤')
        ret.set_image(url=img)
    else:
        ret = NO_RESULT_MESSAGE

    return ret
