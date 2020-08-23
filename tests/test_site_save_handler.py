import asyncio
import shutil

import pytest
import aiohttp
import os

from site_save_handler import write_binary, worker, start_saving_process


@pytest.mark.asyncio
async def test_write_binary():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://example.com', allow_redirects=False, ssl=False) as response:
            await write_binary(response, 'example.com')

    index_file_path = f'{os.getcwd()}/sites/example.com/index.html'
    assert os.path.isfile(index_file_path)

    with open(index_file_path, 'r') as f:
        page_content = f.read()

    assert len(page_content) > 10

    shutil.rmtree(f'{os.getcwd()}/sites/example.com')


@pytest.mark.asyncio
async def test_worker():
    qu = asyncio.Queue()
    await qu.put('https://www.lipsum.com/')
    task = asyncio.Task(worker(qu, 'www.lipsum.com'))
    await asyncio.gather(task)

    assert os.path.exists(f'{os.getcwd()}/sites/www.lipsum.com')

    file_path = f'{os.getcwd()}/sites/www.lipsum.com/index.html'
    assert os.path.isfile(file_path)

    with open(file_path, 'r') as f:
        page_content = f.read()

    assert len(page_content) > 10

    shutil.rmtree(f'{os.getcwd()}/sites/www.lipsum.com')


@pytest.mark.asyncio
async def test_start_saving_process():
    urls = ['https://www.lipsum.com/', 'https://www.lipsum.com/banners/']
    await start_saving_process(urls, 2, 'www.lipsum.com')

    assert os.path.exists(f'{os.getcwd()}/sites/www.lipsum.com')

    saved_pages = os.listdir(f'{os.getcwd()}/sites/www.lipsum.com')
    assert len(saved_pages) == 2

    walk_object = os.walk(f'{os.getcwd()}/sites/www.lipsum.com')

    first_directory = walk_object.__next__()
    assert first_directory[1] == ['banners']
    assert first_directory[2] == ['index.html']

    second_directory = walk_object.__next__()
    assert second_directory[1] == []
    assert second_directory[2] == ['index.html']

    shutil.rmtree(f'{os.getcwd()}/sites/www.lipsum.com')



