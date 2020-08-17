import os
import aiofiles
from settings import project_directory


async def write_binary(response, domain: str):
    print(f'got {response.url} url')
    if response.content_type == 'text/html':
        page_directory = response.url.path if response.url.path != '/' else ''
        file_name = 'index.html'
    else:
        page_directory = '/'.join(response.url.path.split('/')[:-1])
        file_name = response.url.path.split('/')[-1]
    full_path = f'{project_directory}/sites/{domain}{page_directory}'
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    try:
        async with aiofiles.open(f'{full_path}/{file_name}', mode='wb') as f:
            await f.write(await response.read())
            await f.close()
    except OSError as e:
        print(f'OSError, {e}')
    return page_directory
