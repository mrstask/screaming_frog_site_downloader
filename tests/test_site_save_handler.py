import shutil

import pytest
import aiohttp
import os

from site_save_handler import write_binary


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
