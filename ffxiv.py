import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lxml import html
import re
import requests

import funcs

HUNTING_FILE = 'FFXIV/hunting.json'


def search_guide(keyword):
    keyword = re.sub(' ', '%20', keyword)
    address = 'https://guide.ff14.co.kr/lodestone/search?keyword=' + keyword
    markdown = '[공식 가이드 **' + keyword + '** 검색 결과](' + address + ')'
    embed = discord.Embed(description=markdown, color=funcs.THEME_COLOR)
    embed.set_author(name=funcs.BOTNAME, url=funcs.URL, icon_url=funcs.ICON_URL)

    return embed


def search_hunting(keyword):
    huntings = funcs.read_json(HUNTING_FILE)

    if keyword in huntings:
        ret = '**' + keyword + '**: ' + huntings[keyword]
    else:
        ret = '토벌수첩에서 ' + keyword + funcs.josa(keyword, '를') + ' 찾지 못했어요.'

    return ret


def search_recipe(keyword):
    addr_base = 'https://ff14.tar.to'
    address = addr_base + '/item/list/?keyword=' + keyword
    page = requests.get(address)
    tree = html.fromstring(page.content)
    print('searchRecipe: ' + tree.xpath('//a/@href')[14])
    item = re.sub('\n', '', ' '.join(tree.xpath('//a//text()')[15].split()))
    address = addr_base + tree.xpath('//a/@href')[14]
    page = requests.get(address)
    tree = html.fromstring(page.content)

    data = tree.xpath('/html/body/div[3]/div[1]/ul/li//text()')
    data = list(map(lambda x: re.sub('\n', '', ' '.join(x.split())), data))
    data = list(filter(lambda x: x != '', data))

    if len(data) > 0:
        ret = '**' + item + '**의 레시피: ' + ', '.join(data)
    else:
        ret = '결과를 찾지 못했어요.'

    return ret
