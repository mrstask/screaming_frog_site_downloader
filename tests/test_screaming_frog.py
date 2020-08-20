import pytest
import os
import shutil

from screaming_frog_handler import create_directory, run_screamingfrog, get_data_from_report


@pytest.mark.parametrize('domain', ['example.com'])
def test_create_directory(domain: str):
    output = create_directory(domain)
    assert output.startswith(os.getcwd())
    assert domain in output
    assert os.path.exists(output)
    os.rmdir(output)


@pytest.mark.parametrize('domain, ssl', [('example.com', True), ('example.com', False)])
def test_run_screamingfrog(domain: str, ssl: bool):
    output = f'{os.getcwd()}/reports/{domain}/{"ssl" if ssl else "none_ssl"}'
    os.mkdir(output)
    run_screamingfrog(ssl=ssl, domain=domain, report_save_path=output, export_tabs='Internal:All')
    assert os.path.isfile(f'{output}/internal_all.csv')
    shutil.rmtree(output)


def test_get_data_from_report():
    path_to_report_dir = f'{os.getcwd()}/presetupped_reports'
    report = get_data_from_report(path_to_report_dir)
    assert report[0] == 'https://example.com/'
