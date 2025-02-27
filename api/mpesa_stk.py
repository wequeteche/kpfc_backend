import json
import base64
import requests
from datetime import datetime


def get_access_token():
    consumer_key = "ANjfBA1xVyZSaTvkLVWjRUKqZP8MFyabAUzJAQrdatHmIBz2"  
    consumer_secret = "yjQDsq27hkdcTCwXBvacXbTalIEHmMc7rAUZVLdGeJ93Hbv4B3RatpW9W1CQpjGz"  
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status() 
        result = response.json()
        access_token = result['access_token']
        return {'access_token': access_token}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
print(get_access_token())

def initiate_stk_push(customer_mpesa_number, total_amount):
        
    access_token_response = get_access_token()

    try:
        access_token = access_token_response['access_token']
        if access_token:
            # amount = total_amount
            # phone = customer_mpesa_number
            passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
            # business_short_code = '7661701'
            business_short_code = '174379'
            process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            callback_url = 'https://mydomain.com/callback'
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
            # party_a = customer_mpesa_number
            account_reference = 'KPFC BUILDERS'
            transaction_desc = 'stkpush test'
            stk_push_headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }

            stk_push_payload = {
                'BusinessShortCode': business_short_code,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': total_amount,
                'PartyA': customer_mpesa_number,
                'PartyB': business_short_code,
                'PhoneNumber': customer_mpesa_number,
                'CallBackURL': callback_url,
                'AccountReference': account_reference,
                'TransactionDesc': transaction_desc
            }

            try:
                response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                response.raise_for_status()   
                # Raise exception for non-2xx status codes
                response_data = response.json()
                checkout_request_id = response_data['CheckoutRequestID']
                response_code = response_data['ResponseCode']
                
                if response_code == "0":
                    return {'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code}
                else:
                    return {'error': 'STK push failed.'}
            except requests.exceptions.RequestException as e:
                return {'error': str(e)}
        else:
            return {'error': 'Access token not found.'}

    except:
        return {'error': 'Failed to retrieve access token.'}
    
print(initiate_stk_push('254759510388', '1'))

