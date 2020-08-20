import os
import time
import asyncio

import aiohttp
import aiofiles

from screaming_frog_handler import get_data_from_report

qu = asyncio.Queue()


async def write_binary(response, domain: str):
    print(f'got {response.url} url')
    if response.content_type == 'text/html':
        page_directory = response.url.path if response.url.path != '/' else ''
        file_name = 'index.html'
    else:
        page_directory = '/'.join(response.url.path.split('/')[:-1])
        file_name = response.url.path.split('/')[-1]
    full_path = f'{os.getcwd()}/sites/{domain}{page_directory}'
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    try:
        async with aiofiles.open(f'{full_path}/{file_name}', mode='wb') as f:
            await f.write(await response.read())
            await f.close()
    except OSError as e:
        print(f'OSError, {e}')
    return page_directory


async def start_saving_process(urls, domain: str):
    for url in urls:
        await qu.put(url)
    tasks = []
    for _ in range(10):
        task = asyncio.Task(worker(qu, domain))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def worker(queue, domain: str):
    async with aiohttp.ClientSession() as session:
        while queue.qsize() > 0:
            url = await queue.get()
            try:
                async with session.get(url, allow_redirects=False, verify_ssl=False) as response:
                    await write_binary(response, domain)
            except Exception as e:
                print('session get exception for url', url, type(e), e)


if __name__ == '__main__':
    start_time = time.time()
    output = '' # output path
    domain = '' # site domain

    url_list = get_data_from_report(output)
    asyncio.run(start_saving_process(url_list, domain))
    print("--- %s seconds ---" % (time.time() - start_time))