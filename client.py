import aiohttp
import logging


logging.getLogger(__name__)


class EnmRestAsyncSession():

    def __init__(self, enm, login, password):
        self.enm = enm if enm[-1] == "/" else f"{enm}/"
        self.session = None
        self.login = login
        self.password = password
        self.task = f'{self.enm}configuration-tasks/v1/tasks'
        logging.info(f'Connecting to {enm} as {login}')

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False, limit=20)
        self.session = aiohttp.ClientSession(connector=connector)
        login_dict = {'IDToken1': self.login, 'IDToken2': self.password}
        resp = await self.session.post(f'{self.enm}login', params=login_dict)
        assert resp.status == 200
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.get(f"{self.enm}logout")
            await self.session.close()
        except Exception as e:
            print(repr(e))
            logging.critical(repr(e))

    async def post_task(self, payload):
        async with self.session.post(self.task, json=payload) as response:
            logging.debug(f'Request status: {response.status}')
            try:
                resp_json = await response.json()
                return resp_json
            except Exception as e:
                logging.critical(repr(e))
                logging.critical(await response.status)
                logging.critical(await response.text())
                raise(e)
