import asyncio
import time

from screaming_frog_handler import create_directory, run_spider, open_file
from site_save_handler import start_saving_process


def create_report(domain: str, ssl: bool):
    output = create_directory(domain=domain)
    run_spider(output=output,
               domain=domain,
               ssl=ssl,
               export_tabs='Internal:All')
    return output


def save_site(output: str, domain: str):
    url_list = open_file(output)
    asyncio.run(start_saving_process(url_list, domain))


if __name__ == '__main__':
    start_time = time.time()
    domain = '' # your domain
    output = create_report(domain, True)

    save_site(output, domain)

    print("--- %s seconds ---" % (time.time() - start_time))

