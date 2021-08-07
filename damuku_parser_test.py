import os,core.plugins.video_player.video_apis,sys

with open('/home/p0010/XmediaCenter-Python-Remaked-Version/core/storage/Video/CLANNAD/CLANNAD：第1话 在那落樱缤纷的坡道上.cmt.xml','r') as f:
    xmlf = f.read().encode(encoding='utf-8')
    result = core.plugins.video_player.video_apis.damuku_parser(xmlf)
    for i in result:
        print(i)
