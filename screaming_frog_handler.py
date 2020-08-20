import os
import csv

from datetime import datetime


def create_directory(domain: str):
    project_directory = os.getcwd()
    if not os.path.exists(f'{project_directory}/reports/{domain}'):
        os.mkdir(f'{project_directory}/reports/{domain}')
    run_date = str(datetime.now()).replace(' ', '_')
    output = f'{project_directory}/reports/{domain}/{run_date}'
    os.mkdir(output)
    return output


def run_screamingfrog(ssl: bool, domain: str, output: str, export_tabs: str):
    protocol = 'https://' if ssl else 'http://'
    cmd = f'screamingfrogseospider --crawl {protocol + domain}/ --headless ' \
          f'--save-crawl --output-folder {output} --export-tabs "{export_tabs}"'
    os.system(cmd)


def open_file(output: str):
    res_file = []
    with open(f'{output}/internal_all.csv') as csv_file:
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


if __name__ == '__main__':
    domain = ''  # your domain without slashes
    output = create_directory(domain=domain)
    run_screamingfrog(ssl=True, domain=domain, output=output, export_tabs='Internal:All')
