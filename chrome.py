from selenium import webdriver

chrome = webdriver.Chrome(r"D:\chromedriver\chromedriver.exe")
chrome.get("https://aq.lianjia.com/ershoufang/daguanqu/pg1co32/")
print(chrome.page_source)