# social2tg
Feeds from various social networks to Telegram. Currently only Instagram (posts) is supported



TODO:
- if there is 1 media and long caption, replace the media with web preview to place more text
- replace convert_to_ptb() with tg-specific classes. Also ptb_media in tg.PtbChatTarget.publish is what should be returned from to_target()
- posting video
- replace usernames with links
- wrap hashtags with <code> tag
- do not even open in the browser what was published
- hiding source mode:
    - replace usernames with mono text without @
    - cut off hashtags
    - don't show footer
- scheduling for pre-moderating
    - by time
    - by manual approval
    - ability to edit caption
- facebook as a source
