# Telegram analytic dashboard 
(fully working version but still under development)

### **Description**

Telegram Analytic Dashboard is a web-based tool that allows users to analyze their favorite Telegram channels using various graphical representations. Users can gain insights into channel activities, message trends, and more through intuitive visualizations.

## **Requirements**
- Internet connection.
- Downloaded project source code (git clone https://github.com/CESSIDY/telegram-analytic-dashboard)
- Installed and running Docker
- Ensure, that needed for project ports are available (for running with Docker) (Dashboard:8051, Redis:6379, Mongo: 27017, Mongo-express: 8081) or change them on available.

### **Installation**
1. Create telegram app to obtain api_id (https://core.telegram.org/api/obtaining_api_id)
2. Rename the `.env.example` file name to `.env`:
   - Add create account app details at `.env` file:
     - TELEGRAM_API_ID - api id what can get after registering the Telegram application;
     - TELEGRAM_API_HASH - api hash what can get after registering the Telegram application;
     - TELEGRAM_USERNAME - any name;
     - TELEGRAM_PHONE - your account phone;
   - all other settings can remain the same, or you can change them as you wish (eg add your own MongoDB)  
3. Rename the `channels.json.example` file name to `channels.json` into (`/data/channels/`):
    - Add channels to `channels.json` as in the example;
      - For `id` use channels names by witch you able to find them at telegram or use they `hash` - `https://t.me/**hash**` if channel private and link contain '+' in the begin, then just remove it '+Ewa34r3fAWhjnv' -> 'Ewa34r3fAWhjnv';


### **Running (After all configurations)**
  1. go to the project directory;
  2. run: `docker-compose build --force-rm`;
  3. run: `docker-compose up -d`;

### **Usage**
  - Dashboard (http://localhost:8051/) - First you need to run data collection for the channels you want:
    - Click the button at the top right of the screen `RUN SCRAPING FOR(N) CHANNELS`;
    - Now you need to authorize at telegram so enter code what you received from telegram;
    - After this you need to click again on `RUN SCRAPING FOR(N) CHANNELS` button;
    - After some time all needed data will be scraped for channels what you added into `channels.json` (it may take several minutes or even longer if you specified large numbers for (`TELEGRAM_MESSAGES_SCRAPING_LIMIT`, `TELEGRAM_COMMENTS_SCRAPING_LIMIT`) in the `.env` file);
    - Now you can see analytics for channels what you need;
  - Mongo-express: (http://localhost:8081/ credentials: admin:pass) - Here you can check all scraped data (messages, comments, channels) at MongoDB