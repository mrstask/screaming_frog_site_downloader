import os
import asyncio
import aiohttp
import aiofiles

from settings import logging


async def write_binary(response, domain: str):
    """
    Writing requested page to a file
    :param response: response object
    :param domain: site domain without slashes
    :return:
    """
    logging.debug(f'got {response.url} url')
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
        logging.error(f'OSError, {e}')


async def start_saving_process(urls, num_of_async_tasks: int, domain: str):
    """
    Start site saving process via filling que with urls and create tasks
    :param num_of_async_tasks: number of asynchronous tasks
    :param urls: list of urls to crawl
    :param domain:
    :return:
    """
    qu = asyncio.Queue()
    for url in urls:
        await qu.put(url)
    tasks = []
    for _ in range(num_of_async_tasks):
        task = asyncio.Task(worker(qu, domain))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def worker(queue, domain: str):
    """
    Start worker that make page request and saves response
    :param queue: queue
    :param domain: domain without slashes
    :return:
    """
    async with aiohttp.ClientSession() as session:
        while queue.qsize() > 0:
            url = await queue.get()
            try:
                async with session.get(url, allow_redirects=False, verify_ssl=False) as response:
                    await write_binary(response, domain)
            except Exception as e:
                logging.error('session get exception for url', url, type(e), e)
