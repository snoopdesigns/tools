# selfoss-youtube-subs-to-opml.py -- Convert YouTube subscriptions exported
# via Google Takeout (CSV format) into OPML, which can be then imported in Selfoss (https://selfoss.aditu.de/)
#
# Usage:
# python3 selfoss-youtube-subs-to-opml.py subscriptions.csv > yt-subs.opml

import sys
import csv
from xml.sax.saxutils import escape

with open(sys.argv[1], newline='') as csvfile:
    subscriptions = csv.reader(csvfile, delimiter=',', quotechar='"')

    print(f'''<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <body>
        <outline title="YouTube subscriptions" text="YouTube subscriptions">''')
    for subscription in subscriptions:
        title = escape(subscription[2])
        channelId = escape(subscription[0])
        print(f'''            <outline title="{title}"
                     text="{title}"
                     xmlUrl="https://www.youtube.com/feeds/videos.xml?channel_id={channelId}"
                     htmlUrl="https://www.youtube.com/channel/{channelId}" 
                     type="rss" 
                     selfoss:spout="spouts\youtube\youtube"/>
        ''')
    print('''
        </outline>
    </body>
</opml>
    ''')