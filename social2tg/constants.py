import random


HEADERS_LIKE_BROWSER = {
    'User-Agent': (
        f'Mozilla/5.0 (Windows NT 10.0; rv:91.0) '
        f'Gecko/20100101 Firefox/{random.randint(90, 107)}.0'
    ),
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    # ~ 'Cookie': '__atuvc=1%7C11; __atuvs=6230df99a9475c52000; _ga=GA1.2.1462889987.1647370140; _gid=GA1.2.1417447429.1647370140; _gat_gtag_UA_206621869_1=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'X-Requested-With': 'XMLHttpRequest',
}
