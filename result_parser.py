import csv

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


def process_url(url, page_type, status, url_encoded):
    print(url, page_type, status, url_encoded)


if __name__ == '__main__':
    open_file()