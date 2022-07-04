from scraper_object import scraper
import time
import json

#ALL CONSOLES TO SCRAPE
consoles = ["Playstation4 Games"]

#USING THE SCRAPER
x = scraper(15)

#CHOICE TO SAVE LOCALLY / UPLOAD
choice_local, choice_upload = x.data_choice("cex")

#ACCEPt COOKIES
x.open_url("https://uk.webuy.com/boxsearch/?superCatId=1")
x.click_but_by_txt("Accept Cookies")
time.sleep(4)

#HAVE TO USE BUTTONS TO GET THE LINKS REQUIRED
x.click_all_buttons("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul/li", "a")
web_pages = x.get_links_txt(x.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul"), consoles)

#DETAILS OF ALL RECORDS
all_details = {}


for j,i in enumerate(web_pages):
    console = consoles[j]
    #OPEN URL
    x.open_url(i)

    #LOAD ALL RESULTS - MAY NEED TO CHANGE AS SOMETIMES DOESNT AUTO LOAD RESULTS
    x.scroll_down_all()
    time.sleep(4)

    #GET THE ELEMENT CONTAINING ALL DETAILS
    search_rcrd = x.get_products('//div[@class="content-area"]', "searchRcrd")

    for count, record in enumerate(search_rcrd):
        record_id = x.get_prod_id(record, "data-insights-object-id")
        record_name = x.get_product_name(record, "ais-highlight")
        record_price = x.get_product_price(record, "priceTxt")
        record_uuid = x.make_uuid(record_name)
        selling_price = record_price[0].text.split(" ")[-1]
        cash_price = record_price[1].text.split(" ")[-1]
        voucher_price = record_price[2].text.split(" ")[-1]
        record_details = [record_uuid,record_id, record_name, selling_price, cash_price, voucher_price]

        #SAVE THE SCREENSHOTS OF THE COVERS
        #x.save_screenshots(record.find_element_by_tag_name("img"), "screenshots", record_id)

        #SAVE THE DATA
        filename = f'{record_id}_data.json'
        x.save_data(filename, choice_local, choice_upload, [record_uuid, record_id, record_name, selling_price, cash_price, voucher_price], "cex")
        print(count)
