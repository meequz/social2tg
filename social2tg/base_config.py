from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


LOG_PATH = BASE_DIR / 'log.txt'

BROWSER_HEADLESS = True
