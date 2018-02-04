import collections
import logging
import sys
import aiosip
import api_hour
import uvloop

LOG = logging.getLogger(__name__)
COUNTER = 0


async def notify(dialog, message):
    message.payload = 'Aiosip Proxy {}'.format(COUNTER)
    COUNTER += 1
    await dialog.router.proxy(dialog, message)


class Container(api_hour.Container):
    def __init__(self, config, worker, loop):
        super().__init__(config, worker, loop)

        r = aiosip.ProxyRouter()
        r['notify'] = notify
        d = aiosip.Dialplan(default=r)
        self.servers['sip'] = aiosip.Application(loop=self.loop, dialplan=d)
        self.servers['sip']['ah_container'] = self
        self.servers['sip']['clients'] = collections.defaultdict(dict)

        self.handlers = collections.OrderedDict()

    async def make_servers(self, socket):
        await  self.servers['sip'].run(sock=socket[0], protocol=aiosip.TCP)
        return self.handlers

    @classmethod
    def make_event_loop(cls, config):
        """To customize loop generation"""
        return uvloop.new_event_loop()
