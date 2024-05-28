import random


HEADERS_LIKE_BROWSER = {
    'User-Agent': (
        f'Mozilla/5.0 (Windows NT 10.0; rv:91.0) '
        f'Gecko/20100101 Firefox/{random.randint(90, 130)}.0'
    ),
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'X-Requested-With': 'XMLHttpRequest',
}
