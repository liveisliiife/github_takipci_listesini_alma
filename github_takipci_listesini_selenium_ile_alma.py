import time
from selenium import webdriver
from selenium.webdriver.common.by import By

print("Eğer hata alıyorsanız time.sleep() de ki bekleme süresinin arttırın")
kullanici_adi = input("Kullanıcı adınız: ")
sifre = input("Şifreniz: ")
hedef = input("Ulaşmak istediğiniz hesabın kullanıcı adını giriniz: ")

class Github:
    def __init__(self,kullanici_adi,sifre):
        self.browser = webdriver.Chrome()
        # driver yerine self.browser kullandık
        self.username = kullanici_adi
        self.password = sifre
        self.followers = []

    def sign_in(self):
        url = "https://github.com/login"
        self.browser.get(url)
        time.sleep(3)
        giris = self.browser.find_element(By.XPATH, "//*[@id='login_field']")
        giris.send_keys(kullanici_adi)
        time.sleep(1)
        password = self.browser.find_element(By.XPATH, "//*[@id='password']")
        password.send_keys(sifre)
        time.sleep(1)
        password.click()
        time.sleep(3)

    def get_followers(self):
        url = "https://github.com/{}?tab=followers".format(hedef)
        self.browser.get(url)
        time.sleep(3)
        elements = self.browser.find_elements(By.CSS_SELECTOR,".d-table.table-fixed.col-12.width-full.py-4.border-bottom.color-border-muted")
        for i in elements:
            self.followers.append(i.find_element(By.CSS_SELECTOR,".Link--secondary").text)
        tempo = self.browser.find_element(By.CSS_SELECTOR, ".Link--secondary.no-underline.no-wrap").text
        numbers_followers = tempo.split(" ")[0]
        if "." in numbers_followers:
            numbers_followers = numbers_followers[:-1]
            numbers_followers = float(numbers_followers) * 1000
        else:
            numbers_followers = int(numbers_followers)
        if numbers_followers > 50:
            while True:
                pagi = self.browser.find_element(By.CLASS_NAME,"pagination").find_elements(By.TAG_NAME,"a")
                if len(pagi) == 1:
                    if pagi[0].text == "Next":
                        pagi[0].click()
                        time.sleep(3)
                        elements = self.browser.find_elements(By.CSS_SELECTOR,".d-table.table-fixed.col-12.width-full.py-4.border-bottom.color-border-muted")
                        for i in elements:
                            self.followers.append(i.find_element(By.CSS_SELECTOR, ".Link--secondary").text)
                    else:
                        break

                else:
                    for link in pagi:
                        if link.text == "Next":
                            link.click()
                            time.sleep(3)
                            elements = self.browser.find_elements(By.CSS_SELECTOR,".d-table.table-fixed.col-12.width-full.py-4.border-bottom.color-border-muted")
                            for i in elements:
                                self.followers.append(i.find_element(By.CSS_SELECTOR, ".Link--secondary").text)

        print("Toplam Takipçi Sayısı: ",len(self.followers))
        j = 1
        for i in self.followers:
            print(f"{j}-    {i}")
            j += 1


github = Github(kullanici_adi,sifre)
github.sign_in()
github.get_followers()


