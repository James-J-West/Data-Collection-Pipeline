from scraper_object import scraper
import time
import json
consoles = ["Playstation4 Games"]
x = scraper(5)
x.open_url("https://uk.webuy.com/boxsearch/?superCatId=1")
x.click_but_by_txt("Accept Cookies")
time.sleep(4)
x.click_all_buttons("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul/li", "a")
web_pages = x.get_links_txt(x.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[6]/div[2]/div[4]/div[2]/ul"), consoles)
all_details = {}
for j,i in enumerate(web_pages):
    console = consoles[j]
    x.open_url(i)
    x.scroll_down_all()
    time.sleep(4)
    search_rcrd = x.get_products('//div[@class="content-area"]', "searchRcrd")
    page_details = []
    for count, record in enumerate(search_rcrd):
        record_id = x.get_prod_id(record, "data-insights-object-id")
        record_name = x.get_product_name(record, "ais-highlight")
        record_price = x.get_product_price(record, "priceTxt")
        record_uuid = x.make_uuid(record_name)
        selling_price = record_price[0].text.split(" ")[-1]
        cash_price = record_price[1].text.split(" ")[-1]
        voucher_price = record_price[2].text.split(" ")[-1]
        page_details.append([record_uuid, record_id, record_name, selling_price, cash_price, voucher_price])
        x.save_screenshots(record.find_element_by_tag_name("img"), "screenshots", record_id)
    all_details[console] = page_details
with open('CEX_data.json', 'w') as fp:
    json.dump(all_details, fp,  indent=4)

