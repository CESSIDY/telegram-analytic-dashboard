# TelegramCommentingAutomation

## **Before start:**
1. add your accounts app to array into /data/accounts/accounts.json (https://core.telegram.org/api/obtaining_api_id):
   
   1.1 `api_id` - api id what can get after registering the Telegram application
   
   1.2 `api_hash` - api hash what can get after registering the Telegram application
   
   1.3 `username` - any name, must be unique for all accounts

2. add channels to array into /data/channels/channels.json:
   
   2.1 `id` - for `id` use just a `hash` - `https://t.me/**hash**` if channel private and link contain '+' in the begin, 
   then just remove it '+Ewa34r3fAWhjnv' -> 'Ewa34r3fAWhjnv';
   
   2.2 `private` - indicate private channel or not `True or False`;

_Also if you want to store channel or account in separate files, you can simply create 
an json file in the desired directory, with any name, the main thing is that the object need to be in the `array[]` -> `[{"...": "...", ...}]`;_ 

4. `config.ini` - in this file you specify the settings, at the moment this is only the proxy setting, 
and the minimum settings you need to specify here is `proxy_enabled`, if you do not need a proxy then `proxy_enabled = 0`, 
and if the proxy will be used, specify all settings and `proxy_enabled = 1`;
   
After all configurations:
   1. `poetry install`
   1. `cd src`
   2. `poetry run python main.py`
      
      2.1 then there will be logging in for each account and creating a session files, 
      for each account you need to specify the phone number to which it was registered, and the code what you will receive from telegram;
      
