import os
from datetime import datetime

from settings import project_directory


def create_directory(domain: str):
    if not os.path.exists(f'{project_directory}/reports/{domain}'):
        os.mkdir(f'{project_directory}/reports/{domain}')
    run_date = str(datetime.now()).replace(' ', '_')
    output = f'{project_directory}/reports/{domain}/{run_date}'
    os.mkdir(output)
    return output


def run_spider(ssl: bool, domain: str, output: str, export_tabs: str):
    protocol = 'https://' if ssl else 'http://'
    cmd = f'screamingfrogseospider --crawl {protocol + domain}/ --headless ' \
          f'--save-crawl --output-folder {output} --export-tabs "{export_tabs}"'
    os.system(cmd)
