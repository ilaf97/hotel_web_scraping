Inghams Web Scraper v1.0
Written by Isaac Frewin
January 2023

*** INTRO ***

This web scraper is designed to extract data for accomodation listings from Ingham's and TUI's websites.
An example listing for Ingham's and TUI respectively can be found here:
    • https://www.inghams.co.uk/destinations/italy/neapolitan-riviera/amalfi-coast/hotel-aurora-amalfi#0
    • https://www.tui.co.uk/destinations/italy/lake-garda/garda/hotels/hotel-la-perla.html


*** HOW TO USE ***
The web scraper will extract the following data:
• Hotel name
• Location
• Description
• Facilities
• Rooms
• Meals
• Excursions (Ingham's hotels only)
• Images


*** CONSIDERATIONS ***
1. This web scraper relies on the given page layout at the time of production. Changes to the web page layout will
    likely result in the program failing to scrape the data or scraping the incorrect data. This is as the program
    uses HMTL elements to identify target data fields, which can be subject to change with UI updates.
2. Tests are provided to ensure that the site layouts are correct and that data is read in as expected.
3. The TUI part of this scraper uses Selenium with a Chromium web driver.