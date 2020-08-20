import os
import csv

from datetime import datetime


def create_directory(domain: str) -> str:
    """
    Creating directory to save report
    :param domain: target domain name without slashes
    :return: directory path
    """
    project_directory = os.getcwd()
    if not os.path.exists(f'{project_directory}/reports/{domain}'):
        os.mkdir(f'{project_directory}/reports/{domain}')
    run_date = str(datetime.now()).replace(' ', '_')
    output = f'{project_directory}/reports/{domain}/{run_date}'
    os.mkdir(output)
    return output


def run_screamingfrog(ssl: bool, domain: str, report_save_path: str, export_tabs: str):
    """
    Run Screaming Frog report cli
    :param ssl: is site ssl or not
    :param domain: plain domain
    :param report_save_path: directory path to save report
    :param export_tabs: tabs to export
    :return: None
    """
    protocol = 'https://' if ssl else 'http://'
    cmd = f'screamingfrogseospider --crawl {protocol + domain}/ --headless ' \
          f'--save-crawl --output-folder {report_save_path} --export-tabs "{export_tabs}"'
    os.system(cmd)


def get_data_from_report(report_path: str) -> list:
    """
    Open screaming frog generated inbound links report and get urls
    :param report_path: path to screaming frog report
    :return: list of rows that were extracted from report
    """
    res_file = []
    with open(f'{report_path}/internal_all.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                res_file.append(row[-1])
                line_count += 1
        print(f'Processed {line_count} lines.')
    return res_file
