# social2tg
Feeds from various social networks to Telegram. Currently only Instagram (posts) is supported



TODO:
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
- https://github.com/venomous/cloudscraper backend
- PhantomJS backend
- Chrome driver backend
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
