import asyncio
import time

from screaming_frog_handler import create_directory, run_screamingfrog, get_data_from_report
from site_save_handler import start_saving_process


def generate_screamingfrog_report(domain: str, ssl: bool) -> str:
    """
    Generate report using Screaming Frog Seo Spider
    :param domain: domain name without slashes
    :param ssl: is domain starts with https:// or with http://
    :return: path to generated report
    """
    report_output = create_directory(domain=domain)
    run_screamingfrog(ssl=ssl, domain=domain, report_save_path=report_output, export_tabs='Internal:All')
    return report_output


def save_site(output_path: str, domain: str, num_of_tasks: int) -> None:
    """
    Creating target site local html copy
    :param output_path: path to screaming frog report
    :param domain: target domain
    :return: None
    """
    url_list = get_data_from_report(output_path)
    asyncio.run(start_saving_process(url_list=url_list, num_of_tasks=num_of_tasks, domain=domain))


if __name__ == '__main__':
    start_time = time.time()
    domain = 'lotosite.ru' # your domain
    output = generate_screamingfrog_report(domain, True)

    save_site(output, domain, 10)

    print("--- %s seconds ---" % (time.time() - start_time))

