import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import re
import requests

import funcs

JOB_NPC_FILE = 'FFXIV/job_npc.json'
HUNTING_FILE = 'FFXIV/hunting.json'


def guide(keyword):

    keyword = re.sub(' ', '%20', keyword)
    address = 'https://guide.ff14.co.kr/lodestone/search?keyword=' + keyword
    markdown = '[공식 가이드 **' + keyword + '** 검색 결과](' + address + ')'
    ret = discord.Embed(description=markdown, color=funcs.THEME_COLOR)
    ret.set_author(name=funcs.BOTNAME, url=funcs.URL, icon_url=funcs.ICON_URL)

    return ret


def job_quest(keyword):

    job_npcs = funcs.read_json(JOB_NPC_FILE)
    print(keyword)

    if keyword in job_npcs:
        name = job_npcs[keyword]['name']
        pos = job_npcs[keyword]['pos']
        ret = '**' + keyword + '**의 잡 퀘스트 NPC: ' + name + ' (' + pos + ')'
    else:
        ret = '그런 잡을 찾지 못했어요. :sweat_smile:'

    return ret


def hunting(keyword):

    huntings = funcs.read_json(HUNTING_FILE)

    if keyword in huntings:
        pos = huntings[keyword]['pos']
        href = huntings[keyword]['href']
        img = huntings[keyword]['img']
        markdown = '[' + pos + '](' + href + ')'
        ret = discord.Embed(title=keyword,
                            description=markdown, color=funcs.THEME_COLOR)
        ret.set_footer(text='자료: 파이널판타지 14 인벤')
        ret.set_image(url=img)
    else:
        ret = '토벌수첩에서 ' + keyword + funcs.josa(keyword, '를') + ' 찾지 못했어요.'

    return ret


def recipe(keyword):

    keyword = re.sub(' ', '%20', keyword)
    address = 'http://guide.ff14.co.kr/lodestone/search?keyword=' + keyword + '&search=recipe'
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[4]/table/tbody//tr/td[1]/a//text()')
    if keyword in results:
        idx = names.index(keyword)
        href = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[4]/table/tbody//tr/td[1]/a//@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))

        names = tree.xpath('//div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul[1]//li//p//b//text()')
        # cnts = ['3 ', '1 ']
        cnts = tree.xpath('//div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul[1]//li//p/text()')

        desc = ''
        for i in range(0, len(names)):
            desc += cnts[i] + names[i] + '\n'
        ret = discord.Embed(title=keyword, description=desc, color=funcs.THEME_COLOR)
        ret.set_author(name=funcs.BOTNAME, url=funcs.URL, icon_url=funcs.ICON_URL)
        ret.set_footer(text='자료: 파이널판타지 14 공식 가이드')
    else:
        ret = '결과를 찾지 못했어요.'

    return ret

def gathering(keyword):

    keyword = re.sub(' ', '%20', keyword)
    address = 'http://guide.ff14.co.kr/lodestone/search?keyword=' + keyword + '&search=recipe'
    page = requests.get(address)
    tree = html.fromstring(page.content.decode('utf-8'))
    results = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[4]/table/tbody//tr/td[1]/a//text()')
    if keyword in results:
        idx = names.index(keyword)
        href = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[4]/table/tbody//tr/td[1]/a//@href')[idx]
        address = 'http://guide.ff14.co.kr' + href
        page = requests.get(address)
        tree = html.fromstring(page.content.decode('utf-8'))

        names = tree.xpath('//div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul[1]//li//p//b//text()')
        # cnts = ['3 ', '1 ']
        cnts = tree.xpath('//div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/ul[1]//li//p/text()')

        desc = ''
        for i in range(0, len(names)):
            desc += cnts[i] + names[i] + '\n'
        ret = discord.Embed(title=keyword, description=desc, color=funcs.THEME_COLOR)
        ret.set_author(name=funcs.BOTNAME, url=funcs.URL, icon_url=funcs.ICON_URL)
        ret.set_footer(text='자료: 파이널판타지 14 공식 가이드')
    else:
        ret = '결과를 찾지 못했어요.'

    return ret
