# social2tg
Feeds from various social networks to Telegram. Currently only Instagram (posts) is supported


To add new feed:
- create tg channel, set avatar
- add bot, make it admin
- curl https://api.telegram.org/bot{TOKEN}/getUpdates
- obtain channel ID. Add 100 to it at the beginning, keeping "-" sign at the very beginning, if necessarry
- create source, target, and a feed in config.py


TODO:
- lowercase all the config vars
- implement other Instagram providers
    - https://www.picuki.com
    - https://www.pixwox.com
    - https://greatfon.com/
    - https://dumpor.com (not so simiar)
    - https://apkun.com
    - https://imginn.com
    - https://storiesig.net
    - https://storiesig.app/
    - https://storiesig.me/
    - https://storistalker.com/ (not similar)
    - https://instanavigation.com/
    - https://inflact.com/
    - https://instastories.watch
    - https://iganony.com
    - https://privatephotoviewer.com
    - https://insta-stories-viewer.com/
    - https://www.exploreig.com/
    - https://imginn.org/
- PhantomJS backend
- Chrome driver backend
- https://playwright.dev/python/docs/intro backend
- https://github.com/adw0rd/instagrapi backend
- posting video
- if there is 1 media and long caption, replace the media with web preview to place more text
- replace convert_to_ptb() with tg-specific classes. Also ptb_media in tg.PtbChatTarget.publish is what should be returned from to_target()
- ability to run "run.py" with feeds as arguments
- replace usernames with links
- wrap hashtags with <code> tag
- do not even open in the browser what was published
- analyze config on start and complain if smth is wrong
- hiding source mode:
    - replace usernames with mono text without @
    - cut off hashtags
    - don't show footer
- scheduling for pre-moderating
    - by time
    - by manual approval
    - ability to edit caption
- facebook as a source
- reddit as a source
