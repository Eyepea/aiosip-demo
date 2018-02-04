import asyncio
import logging
import aiosip

sip_config = {
    'srv_ip': '217.182.114.36',
    'srv_host': 'qd.allocloud.com',
    'srv_port': 10060,
    'user': 'XXXX',
    'pwd': 'XXXXX',
}


async def options(dialog, request):
    await dialog.reply(request, status_code=200)


async def register(app, protocol):
    peer = await app.connect((sip_config['srv_ip'], sip_config['srv_port']), protocol)
    register_dialog = peer.create_dialog(
        from_details=aiosip.Contact.from_header(
            'sip:{}@{}:{}'.format(sip_config['user'], sip_config['srv_host'], sip_config['srv_port'])),
        to_details=aiosip.Contact.from_header(
            'sip:{}@{}:{}'.format(sip_config['user'], sip_config['srv_host'], sip_config['srv_port'])),
        password=sip_config['pwd'],
    )
    await register_dialog.register()
    await asyncio.sleep(60)


def main():
    loop = asyncio.get_event_loop()
    app = aiosip.Application(loop=loop)

    r = aiosip.Router()
    r['options'] = options
    app.dialplan.add_user('asterisk', r)

    loop.run_until_complete(register(app, aiosip.TCP))
    loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
