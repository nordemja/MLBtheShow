# MLB The Show
This is a collection of tools I created to aid with several tasks within MLB The Show.

## Usage
1. Navigate to https://mlb21.theshow.com/community_market and log in
2. Open up developer tools in the browser
3. Click on network tab of developer tools
4. Scroll down and select the second page
5. Right click on the request that says **/completed_orders?page=2&**
6. Select Copy -> Copy as cURL (cmd)
7. Open a new tab and navigate to https://curl.trillworks.com/ and paste the command into the window
8. Copy **ONLY** the python headers section. 
9. Paste headers into headers.json
10. Do ctrl+h and find/replace all ' with "
11. Save headers.json
12. Run desired tool

**NOTE:** Running MarketBot.py will require API_KEY and data_sitekey to be updated. To obtain an API key - a subscription to the 2captcha recaptcha solving service will be needed. Further guidance can be follwed at https://www.youtube.com/watch?v=_jV5GgbRpXA&t=1s

## Next Steps
I am currently in the process of updating both getRankedSeasonsData to work with 2021 data. Once this is done, then the .ipynb file will be develoed further for complete analysis as this is still a work in progress.

For the market bot, I would like to integrate a daily report. This would work by scraping data from https://mlb21.theshow.com/orders/completed_orders and analyzing data such as frequently bought, frequently sold, average buy/sell price, best buy, best sell, as well as peak times. From here, I would generate visual representation using matplotlib and pyplot and generate an email report to give the user a daily summary of transactions.


