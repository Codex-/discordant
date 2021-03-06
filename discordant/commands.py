
from .discordant import Discordant
from discord.embeds import Embed
from discord.colour import Colour
from functools import partial
from random import randrange
import re
import requests
import asyncio


async def perform_async(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


@Discordant.register_handler(r'^ping$', re.I)
async def _ping(self, match, message):
    await self.send_message(message.channel,
                            message.content.replace('i', 'o')
                                           .replace('I', 'O'))


@Discordant.register_handler(r'\bayy+$', re.I)
async def _ayy_lmao(self, match, message):
    await self.send_message(message.channel, 'lmao')


@Discordant.register_command('youtube')
async def _youtube_search(self, args, message):
    base_req_url = 'https://www.googleapis.com/youtube/v3/search'
    req_args = {
        'key': self.config.get('API-Keys', 'youtube'),
        'part': 'snippet',
        'type': 'video',
        'maxResults': 1,
        'q': args
    }

    res = await perform_async(requests.get, base_req_url, req_args)
    if not res.ok:
        await self.send_message(message.channel, 'Error:',
                                res.status_code, '-', res.reason)
        return

    json = res.json()
    if json['pageInfo']['totalResults'] == 0:
        await self.send_message(message.channel, 'No results found.')
    else:
        video_title = json['items'][0]['snippet']['title']
        video_url = 'https://youtu.be/' + json['items'][0]['id']['videoId']
        await self.send_message(message.channel, '**{0}:**\n{1}'
                                .format(video_title, video_url))


@Discordant.register_command('urban')
async def _urban_dictionary_search(self, args, message):
    base_req_url = 'http://api.urbandictionary.com/v0/define'

    res = await perform_async(requests.get, base_req_url, {'term': args})
    if not res.ok:
        await self.send_message(message.channel, 'Error:',
                                res.status_code, '-', res.reason)
        return

    json = res.json()
    if len(json['list']) == 0:
        await self.send_message(message.channel,
                                'No results found for "{}".'.format(args))
    else:
        entry = json['list'][0]
        definition = re.sub(r'\[(\w+)\]', '\\1', entry['definition'])

        reply = ''
        reply += definition[:1000].strip()
        if len(definition) > 1000:
            reply += '... (Definition truncated. '
            reply += 'See more at <{}>)'.format(entry['permalink'])
        reply += '\n\n{} :+1: :black_small_square: {} :-1:'.format(
            entry['thumbs_up'], entry['thumbs_down'])

        result = Embed(
            title=args,
            type='rich',
            description=reply,
            url=entry['permalink'],
            colour=Colour.green(),
        )

        await self.send_message(message.channel, embed=result)


_memos = {}


@Discordant.register_command('draw')
async def _draw(self, args, message):
    responses = [
        "{} is the lucky winner!",
        "Oof, bad luck {}",
        "Rest in peace, {}",
        "It's not oats, but {} will do"
    ]

    members = []
    for member in message.server.members:
        if member.id != message.author.id and not member.bot:
            members.append(member)

    response = responses[int(randrange(0, len(responses)))]\
        .format(members[int(randrange(0, len(members)))].mention)

    await self.send_message(message.channel, response)


@Discordant.register_command('remember')
async def _remember(self, args, message):
    global _memos

    key, *memo = args.split()
    if len(memo) == 0:
        if key in _memos:
            del _memos[key]
            await self.send_message(message.channel, 'Forgot ' + key + '.')
        else:
            await self.send_message(message.channel,
                                    'Nothing given to remember.')
        return

    memo = args[len(key):].strip()
    _memos[key] = memo
    await self.send_message(
        message.channel,
        "Remembered message '{}' for key '{}'.".format(memo, key))


@Discordant.register_command('recall')
async def _recall(self, args, message):
    global _memos
    if args not in _memos:
        await self.send_message(message.channel,
                                'Nothing currently remembered for', args + '.')
        return

    await self.send_message(message.channel, _memos[args])


@Discordant.register_command('join')
async def _join(self, args, message):
    app_info = await self.application_info()
    join_string = "A server admin must add this bot to their server!\n" \
                  "Follow: <https://discordapp.com/oauth2/authorize?"\
                  "client_id=" + app_info.id + "&scope=bot>"
    await self.send_message(message.channel, join_string)


@Discordant.register_command('resetname')
async def _reset(self, args, message):

    app_info = await self.application_info()
    # member = message.server.get_member(app_info.id)
    # print(type(app_info))
    await self.change_nickname(message, '')


@Discordant.register_command('lenny')
async def _lenny(self, args, message):
    await self.send_message(message.channel, '( ͡° ͜ʖ ͡°)')


@Discordant.register_command('poop')
async def _poop(self, args, message):
    cat_poop = (".                                        /￣￣￣＼\n　　　　　　"
                " 　　/|　　 　　 ｜\n　　　　　 　　/　| 　 | ∩　 　＼\n　　　　 　　∫"
                "　     |      | | | ＼　　 ￣￣＼ ∧　 ∧　     ／￣￣￣￣￣￣￣￣￣￣"
                "￣￣￣￣|\n　　　　　　　 　 | / 　| |　　＼＿＿ 　(　´ ∀｀)  < 　POO"
                "P UPLOAD COMPLETE          )\n　　　　　　　　 / / 　| |　　　　　"
                " /　/ / /　　  ＼＿＿＿＿＿＿＿＿＿＿＿＿＿＿|\n　　　　　 　　 / /　　"
                "| | 　　　　（ （ / /\n　　　          　 / /　　　| | 　　　　    "
                " ＼＼\n　       　:poop:      U　　       U 　　　         ⊂ / ∪")
    await self.send_message(message.channel, cat_poop)
