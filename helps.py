import discord
from discord.ext import commands
from discord.ext.commands import Bot


def default():
    ret = discord.Embed(description='만나서 반가워요.', color=THEME_COLOR)
    ret.set_author(name=BOTNAME, url=URL, icon_url=ICON_URL)
    ret.add_field(name=PREFIX+'더해',
                  value='주어진 수들을 덧셈해 드려요. (무료)', inline=True)
    ret.add_field(name=PREFIX+'빼',
                  value='처음 수에서 나머지 수를 뺄셈해요.', inline=True)
    ret.add_field(name=PREFIX+'계산',
                  value='(이 정도 쯤이야.)', inline=True)
    ret.add_field(name=PREFIX+'골라',
                  value='배그할까 레식할까? ` ~골라 배그 레식 `', inline=True)
    ret.add_field(name=PREFIX+'초성',
                  value='초성퀴즈를 할 수 있어요. (장르 : 영화, 음악, 동식물, 사전, 게임, 인물, 책)\n` ~초성 게임 5 `처럼 사용하세요. 끝내려면 ` ~초성 끝 `을 입력하세요.\n(유저 등록 개발중)', inline=True)
    #ret.add_field(name=PREFIX+'배그',
    #                 value='[dak.gg](https://dak.gg)에서 배틀그라운드 전적을 찾아요.', inline=True)
    ret.add_field(name=PREFIX+'소전',
                  value='제조 시간을 입력하시면 등장하는 전술인형 종류를 알려 드려요.\n` ~소전 03:40 `처럼 사용하세요.', inline=True)
    ret.add_field(name=PREFIX+'주사위',
                  value='주사위를 던져요.\n` ~주사위 2d6 `처럼 사용하세요.', inline=True)
    ret.add_field(name=PREFIX+'제비',
                  value='당첨이 한 개 들어 있는 제비를 준비해요.\n` ~제비 3 `처럼 시작하고 ` ~제비 `로 뽑으세요.\n취소하려면 ` ~제비 끝 `을 입력하세요.', inline=True)
    ret.add_field(name=PREFIX+'리볼버',
                  value='러시안 룰렛을 할 수 있어요.\n` ~리볼버 1 `처럼 장전하고 ` ~리볼버 `로 발사하세요.', inline=True)
    ret.add_field(name=PREFIX+'알람',
                  value='특정 시각 혹은 일정 시간 후에 메시지와 함께 멘션해 드려요. ` ~알람 23:59 자라 ` ` ~알람 240 컵라면 `')
    ret.add_field(name=PREFIX+'기억',
                  value='키워드에 관한 내용을 DB에 기억해요.\n` ~기억 원주율 3.14159265 `로 기억에 남기고 ` ~기억 원주율 `로 불러오세요.\n` ~기억 랜덤 `을 입력하면 아무 기억이나 불러와요.\n` ~기억 삭제 원주율`로 기억을 지울 수 있어요.', inline=True)
    ret.add_field(name=PREFIX+'포네틱',
                  value='입력하신 문자열을 포네틱 코드로 바꿔 드려요. ` ~포네틱 White House `\n숫자만 입력하면 ITU/IMO 표준 코드로 바꿔요.', inline=True)
    '''
    ret.add_field(name=PREFIX+'게이머 (WIP)',
                     value='게이머 관련 업무를 수행해요. `등록` / `나`', inline=True)
    ret.add_field(name=PREFIX+'코인 (WIP)',
                     value='게이머 코인 관련 업무를 수행해요. `초기화` / `이체`', inline=True)
    '''
    ret.add_field(name=PREFIX+'결투',
                  value='같은 서버에 있는 상대에게 도전할 수 있어요. ` ~듀얼 레버버 `\n상대가 도전에 응하면 결투가 시작돼요. 제가 셋을 세면 ` ~BANG `으로 먼저 맞추는 사람이 승리예요.')
    ret.add_field(name=PREFIX+'블랙잭',
                  value='저와 블랙잭 승부를 겨루실 수 있어요. 히트는 ` ~H `, 스탠드는 ` ~S `를 입력하세요.\n코인을 걸 수 있어요.', inline=True)
    # 빈칸
    ret.add_field(name='\u200B', value='\u200B')
    # 파판 명령어 도움
    ret.add_field(name=PREFIX+'도움 파판',
                  value='FFXIV 관련 명령어를 알려드려요.')

    return ret


def ffxiv():
    ret = discord.Embed(description='FFXIV 관련 명령어를 모아 놓았어요쿠뽀.', color=THEME_COLOR)
    ret.set_author(name=BOTNAME, url=URL, icon_url=ICON_URL)
    ret.add_field(name=PREFIX+'공식',
                  value='[공식 가이드](http://guide.ff14.co.kr/lodestone) 검색 링크를 만들어요. ` ~공식 제멜 토마토 `')
    ret.add_field(name=PREFIX+'레시피',
                  value='공식 가이드에서 아이템 제작 레시피를 검색해요. ` ~레시피 고리갑옷 `')
    ret.add_field(name=PREFIX+'마물',
                  value='[인벤](http://ff14.inven.co.kr)에서 마물 정보를 검색해요. ` ~마물 아스왕 `')
    ret.add_field(name=PREFIX+'상점',
                  value='공식 가이드에서 아이템 판매 NPC를 검색해요. ` ~상점 질긴 가죽 `')
    ret.add_field(name=PREFIX+'의뢰',
                  value='해당 레벨의 용병업 의뢰를 받을 수 있는 곳을 알려 드려요. ` ~의뢰 35 `')
    ret.add_field(name=PREFIX+'잡퀘',
                  value='잡 퀘스트 NPC 위치를 알려 드려요. ` ~잡퀘 전사`\n창천, 홍련 추가 직업은 아직 지원되지 않아요.')
    ret.add_field(name=PREFIX+'장비(WIP)',
                  value='상점에서 파는 채집·제작직 최적 장비를 알려 드려요. ` ~장비 광부 43`\n` ~상점 `으로 검색하면 해당 아이템의 판매 NPC들을 볼 수 있어요.')
    ret.add_field(name=PREFIX+'채집',
                  value='공식 가이드에서 채집 위치정보를 검색해요. ` ~채집 황혼비취 `')
    ret.add_field(name=PREFIX+'토벌',
                  value='인벤에서 토벌수첩 몬스터가 어디 있는지 찾아 드려요. ` ~토벌 무당벌레 `')
    ret.add_field(name=PREFIX+'풍맥',
                  value='공식 가이드에서 풍맥의 샘 지도 링크를 만들어요. ` ~풍맥 홍옥해 `')

    return ret
