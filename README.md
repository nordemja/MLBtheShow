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



