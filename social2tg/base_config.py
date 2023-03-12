from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


LOG_PATH = BASE_DIR / 'log.txt'

BROWSER_HEADLESS = True
TOR_PROXY = False
WAIT_BETWEEN = 3

GRAMHIR_HOST = 'picuki.com'  # or 'gramhir.com'

REQUESTS_CLOUDSCRAPER = True

BETWEEN_POSTS_DELAY = 61
BETWEEN_SOURCES_DELAY = 121
