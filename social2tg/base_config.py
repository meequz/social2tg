from pathlib import Path


base_dir = Path(__file__).resolve(strict=True).parent.parent


log_path = base_dir / 'log.txt'

browser_headless = True
tor_proxy = False
proxy = None
disable_ssl = False

gramhir_host = '167.172.252.123'  # or 'gramhir.com', 'picuki.com', 'www.picuki.com'
gramhir_host_header = 'www.picuki.com'

delay_after_post = 3
delay_after_source = 5
delay_after_any_request = 3
