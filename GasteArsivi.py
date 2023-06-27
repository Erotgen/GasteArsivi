from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
import urllib.request
from PIL import Image
import time
import ocrmypdf
import os
import fitz
import pathlib
import sys


def ConvertWord(kelime):
    if kelime[0] == '"' and kelime[-1] == '"':
        kelimeklasör = kelime[1:-1]
        
    else:
        kelimeklasör = kelime
        
    return kelimeklasör

def CreateFolder(kelime, yol):
    
    folderlist = os.listdir(yol+"\\Çıktılar")
    count = 0
    kelimeklasör = kelime
    
    while kelimeklasör in folderlist:
        count += 1
        kelimeklasör = kelime+" - "+str(count)
    
    
    os.chdir(yol+"\\Çıktılar")
    os.makedirs(kelimeklasör)
    os.chdir(yol+"\\Çıktılar\\"+kelimeklasör)
    os.makedirs("Resimler")
    os.makedirs("PDF")
    os.makedirs("OCR-PDF")
    
    return kelimeklasör
        
def Page(kelime):
    fp = webdriver.FirefoxProfile(yol+"\\FirefoxProfile")
    fp.set_preference("dom.popup_maximum", 0)
    browser = webdriver.Firefox(firefox_profile = fp)
    browser.get("https://www.gastearsivi.com/")
    time.sleep(1)
    
    try:
        browser.find_element("xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]").click()
    except NoSuchElementException:
        time.sleep(0.5)
        
    time.sleep(0.5)
    browser.find_element("xpath", "//*[@id='root']/div/div[1]/div/div[2]/form/div/input").send_keys(kelime)
    time.sleep(1)
    browser.find_element("xpath", "//*[@id='button-search1']").click()
    time.sleep(2)
    url = browser.current_url
    
    return browser, url

def OpenPage(url, page):
    
    fp = webdriver.FirefoxProfile(yol+"\\FirefoxProfile")
    fp.set_preference("dom.popup_maximum", 0)
    browser = webdriver.Firefox(firefox_profile = fp)
    browser.get(url+"/"+str(page))
    try:
        browser.find_element("xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]").click()
    except NoSuchElementException:
        time.sleep(0.5)
    
    return browser

def FindPage(browser, url):
    time.sleep(8)
    for i in range(4, 0, -1):
        try:
            browser.find_element("xpath","//*[@id='root']/div/div[2]/div/div[3]/div/nav/ul/li["+str(i)+"]/span")
            control = "var"
        
        except NoSuchElementException:
            control = "yok"
            if i == 1:
                break
            continue
        
        try:
            browser.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[3]/div/nav/ul/li["+str(i)+"]/span")
            sonsayfa = browser.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[3]/div/nav/ul/li["+str(i)+"]/span").text
        except NoSuchElementException:
            sonsayfa = browser.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[3]/div/nav/ul/li["+str(i)+"]/span/a").text
            
        break
    if control == "yok":
        sonsayfa = "1"
    return sonsayfa

def FindOutput(browser, url):
    
    for i in range(20, 0, -1):
        try:
            browser.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[2]/div["+str(i)+"]/a/img")
            control = "var"
        
        except NoSuchElementException:
            control = "yok"
            continue

        soncikti = str(i)
        break
    
    if control == "yok":
        
        try:
            browser.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[2]/div/a/img")
            control = "var"
        
        except NoSuchElementException:
            control = "yok"        
    
        if control == "var":
            soncikti = "1"
        
        else:
            soncikti = "0"
    
    return soncikti

def Output(sürücü, output, yol, count, kelimeklasör):
    text = sürücü.find_element("xpath","//*[@id='root']/div/div[2]/div/div[2]/div["+str(output)+"]/a/h3").text
    url = sürücü.find_element("xpath", "//*[@id='root']/div/div[2]/div/div[2]/div["+str(output)+"]/a/img").get_attribute("src")
    
    url1 = str(url)
    
    url2 = url1[8:-1]
    index1 = url2.find("/")
    firstpart = url2[0:index1]
    url3 = url2[index1+1:-1]
    url4 = url3[11:-1]
    index2 = url4.find("thumbnail250")
    url4 = url4[0:index2]
    image = "https://"+firstpart+"/"+"sayfalar"+"/"+url4[0:-1]+".jpg"
    
    urllib.request.urlretrieve(image, yol+"\\Çıktılar\\"+kelimeklasör+"\\Resimler\\"+str(count)+" - "+text+".jpg")
    
    return image, text

def ConvertPDF(image, text, yol, kelime, count, kelimeklasör):
    
    img = Image.open(yol+"\\Çıktılar\\"+kelimeklasör+"\\Resimler\\"+str(count)+" - "+text+".jpg")
    imaj = img.convert("RGB")
    imaj.save(yol+"\\Çıktılar\\"+kelimeklasör+"\\PDF\\"+str(count)+" - "+text+".pdf")
    os.remove(yol+"\\Çıktılar\\"+kelimeklasör+"\\Resimler\\"+str(count)+" - "+text+".jpg")
    

def OCR(yol, kelime, text, count, kelimeklasör):
    ocrmypdf.ocr(yol+"\\Çıktılar\\"+kelimeklasör+"\\PDF\\"+str(count)+" - "+text+".pdf", yol+"\\Çıktılar\\"+kelimeklasör+"\\OCR-PDF\\"+str(count)+" - "+text+".pdf", skip_text=True, optimize=0, output_type="pdf", fast_web_view=0, skip_big=50)    
    os.remove(yol+"\\Çıktılar\\"+kelimeklasör+"\\PDF\\"+str(count)+" - "+text+".pdf")    
    
def TotalPDF(yol, kelime, count, text, kelimeklasör):
    if count == 1:
        doctotal = fitz.open()
        doc = fitz.open(yol+"\\Çıktılar\\"+kelimeklasör+"\\OCR-PDF\\"+str(count)+" - "+text+".pdf")
        doctotal.insert_pdf(doc)
        doctotal.save(yol+"\\Çıktılar\\"+kelimeklasör+"\\"+kelime+".pdf")
        doc.close()
        doctotal.close()
    else:
        doctotal = fitz.open(yol+"\\Çıktılar\\"+kelimeklasör+"\\"+kelime+".pdf")
        doc = fitz.open(yol+"\\Çıktılar\\"+kelimeklasör+"\\OCR-PDF\\"+str(count)+" - "+text+".pdf")
        doctotal.insert_pdf(doc)
        doctotal.save(yol+"\\Çıktılar\\"+kelimeklasör+"\\"+kelime+".pdf", incremental=True, encryption=0)
        doc.close()
        doctotal.close()

yol = str(pathlib.Path(__file__).parent.resolve())
kelime = input("Lütfen aranacak kelimeyi giriniz: ")
url = Page(kelime)
sayfa = FindPage(url[0], url[1])
kelime = ConvertWord(kelime)
kelimeklasör = CreateFolder(kelime, yol)


if int(sayfa) == 1:
    
    sürücü = OpenPage(url[1], 1)
    cikti = FindOutput(sürücü, url[1])
    
    if cikti == "0":
        print("Bu arama hiç sonuç vermedi!")
        sys.exit()
        
    count = 1
    
    for output in range(1, int(cikti)+1):
        print(str(count),". çıktı.")
        image = Output(sürücü, output, yol, count, kelimeklasör)
        ConvertPDF(image[0], image[1], yol, kelime, count, kelimeklasör)
        OCR(yol, kelime, image[1], count, kelimeklasör)
        TotalPDF(yol, kelime, count, image[1], kelimeklasör)
        print(str(count)+". çıktı tamamlandı.")
        count += 1
    
    sürücü.close()
        
else:
    
    count = 1
    
    for page in range(1, int(sayfa)+1):
        
        sürücü = OpenPage(url[1], page)
        
        if page == int(sayfa):
            
            cikti = FindOutput(sürücü, url[1])
            for output in range(1, int(cikti)+1):
                print(str(count),". çıktı.")
                image =  Output(sürücü, output, yol, count, kelimeklasör)
                ConvertPDF(image[0], image[1], yol, kelime, count, kelimeklasör)
                OCR(yol, kelime, image[1], count, kelimeklasör)
                TotalPDF(yol, kelime, count, image[1], kelimeklasör)
                print(str(count)+". çıktı tamamlandı.")
                count += 1
            
            sürücü.close()
       
        else:        
            for output in range(1, 21):
                print(str(count),". çıktı.")
                image =  Output(sürücü, output, yol, count, kelimeklasör)
                ConvertPDF(image[0], image[1], yol, kelime, count, kelimeklasör)
                OCR(yol, kelime, image[1], count, kelimeklasör)
                TotalPDF(yol, kelime, count, image[1], kelimeklasör)
                print(str(count)+". çıktı tamamlandı.")
                count += 1
        
            sürücü.close()

url[0].close()
print("İşlem tamamlandı.")