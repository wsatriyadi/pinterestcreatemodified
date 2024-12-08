from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json, requests, time, datetime

foldercookies = "cookies"
#while(True):
print("proses ambil email")
emaildata = requests.get("https://mailku.cloudrss.biz.id/api/getdata/type/json")
datainput = emaildata.json()
print("email didapat "+datainput['email'])

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False, proxy = {'server': '127.0.0.1:8080'}) #tulis aja host proxy nya
    context = browser.new_context()
    page = context.new_page()

    print("Fill form")
    page.goto("https://www.pinterest.com/business/create/",timeout=100000)

    #page.pause()
    page.get_by_placeholder("Email").fill(datainput['email'])
    page.get_by_placeholder("Password").fill('BebasSuka123#')
    #date_object = datetime.strptime(datainput['umur'], "%Y-%m-%d")
    page.locator("[data-test-id=\"signup-birthdate-field\"]").get_by_label("Birthdate").fill("1990-12-05")
    page.get_by_role("button", name="Create account").click(timeout=1000)
    page.wait_for_url("**/hub/")

    all_cookies = context.cookies()
    print("Sukses, simpan cookies")
    file_path = foldercookies+"/"+datainput['email']+".json"
    with open(file_path, 'w') as file:
        json.dump(all_cookies, file)
    
    print("menunggu inbox")
    time.sleep(120)
    inbox = requests.get("https://mailku.cloudrss.biz.id/api/inboxjson/email/"+datainput['email'])
    isiinbox = inbox.json()

    for isian in isiinbox:
        if(isian['from'] == 'confirm@account.pinterest.com'):
            linkinbox = isian['readurl']

            getemail = requests.get(linkinbox)
            soup = BeautifulSoup(getemail.content, 'html.parser')
            links = soup.find_all('a', class_="pf dm_df")

            for link in links:
                url = link.get('href')

                page.goto(url,timeout=50000)
    browser.close()
    print("selesai")