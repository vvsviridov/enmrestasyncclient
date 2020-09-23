import asyncio
import logging

from client import EnmRestAsyncSession
from rbsfile import bs_list
from termcolor import colored
from fdndict import FdnDict
from os import environ


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.INFO,
    filename='cellstate.log'
)


async def get_rbs_cells(sess, rbs):
    param = {"name": "readCells", "fdn": f"NetworkElement={rbs}"}
    resp = await sess.post_task(param)
    result = []
    if resp.get('requestResult') == 'SUCCESS':
        for rbs in resp.get('successfulMoOperations').get('LTE'):
            result += rbs.get('cells')
    for cell in result:
        status = await get_cell_status(sess, cell)
        fd = FdnDict(status.get('fdn'))
        if status.get('attributes').get('operationalState') == 'DISABLED':
            print(
                fd['MeContext'],
                fd['EUtranCellFDD'],
                colored(status.get('attributes'), 'red')
            )
        else:
            print(
                fd['MeContext'],
                fd['EUtranCellFDD'],
                status.get('attributes')
            )


async def get_cell_status(sess, cell_fdn):
    param = {
        "name": "readCellsData",
        "fdn": cell_fdn,
        "attributes": ["administrativeState", "operationalState"]
    }
    resp = await sess.post_task(param)
    if resp.get('requestResult') == 'SUCCESS':
        return resp.get('successfulMoOperations').get('LTE')[0]


async def main():
    URL = environ['enm_url']
    USER = environ['enm_user']
    PASS = environ['enm_pass']
    async with EnmRestAsyncSession(
        URL,
        USER,
        PASS,
    ) as erc:
        tasks = []
        for bs in bs_list('NodesBS.txt'):
            task = asyncio.create_task(get_rbs_cells(erc, bs))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
