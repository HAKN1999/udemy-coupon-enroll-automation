#!/usr/bin/python3
# coding: utf-8


from selenium import webdriver
from time import sleep
import pickle
import sys
import os


PATH = os.getcwd()
driver = webdriver.Chrome(
    executable_path=r"{PATH}/chromedriver".format(PATH=PATH))

url = "https://www.udemy.com/join/login-popup"


def halaman_masuk_udemy(email, password):
    """untuk login ke halaman udemy dan menyimpan cookies untuk
       menghindari human verifikasi jika password salah berluang kali
    """
    try:

        input_email = driver.find_element_by_xpath("//input[@id='email--1']")
        input_email.send_keys(email)

        input_password = driver.find_element_by_xpath(
            "//input[@id='id_password']")
        input_password.send_keys(password)

        login = driver.find_element_by_xpath(
            "//input[@id='submit-id-submit']").click()

        try:
            # salah input email / password
            get_problem_logging = driver.find_element_by_class_name("alert")
            if get_problem_logging:
                print(get_problem_logging.text)
                # keluar program

        except:
            pass

        simpan_cookies(driver)
        driver.implicitly_wait(2)

    except:
        sys.exit("[X] Mungkin kena verifikasi you are a human,coba lagi 30Menit!")


def simpan_cookies(driver):
    """simpan cookies setelah loginn"""

    # simpan cookies untuk login sesi berikut nya
    with open("cookies-udemy.pickle", "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

    print("[*] Cookies berhasil di simpan")


def load_cookies(url):
    """meload cookies yg telah di simpan"""

    with open("cookies-udemy.pickle", "rb") as read_cookies:
        cookies = pickle.load(read_cookies)
    driver.get(url)

    for cookie in cookies:
        driver.add_cookie(cookie)
    print("[*] Refresh driver ")

    driver.refresh()

    print("[*] Cookies berhasil di load")


def baca_kupon_udemy(coupon):
    """enroll kursus, tapi masih bingung sama jalan nya flow jadi agak stuck di bagian ini, minim handel error"""

    driver.get(coupon)

    print("\n{coupon}".format(coupon=coupon.strip()))

    sleep(10)

    try:
        getinfo_price = driver.execute_script(
            "return document.getElementsByClassName('styles--btn--express-checkout--28jN4')[0].textContent")

    except:
        sys.exit('Detail harga tidak ditemukan,cek koneksi internet!')

    if getinfo_price == 'Buy now':
        price = driver.execute_script(
            "return document.getElementsByClassName('buy-box__element')[1].getElementsByTagName('span')[1].textContent")
        return '\t|_ ' + str(getinfo_price) + ' ' + str(price)

    elif getinfo_price == 'Go to course':
        return '\t|_ ' + 'Kursus telah di ambil, ' + ' ' + str(getinfo_price)

    else:
        try:
            print('\t|_ ' + str(getinfo_price))
            driver.execute_script(
                "document.getElementsByClassName('styles--btn--express-checkout--28jN4')[0].click()")
        except:
            return '\t|_ ' + 'Mungkin,halaman page Berbeda jadi tidak bisa di enroll!'

        sleep(5)

        try:
            driver.execute_script(
                "document.getElementsByClassName('ellipsis')[0].click()")

            sleep(5)

            print_enroll = driver.execute_script(
                "return document.getElementsByClassName('content')[0].textContent")
            success = re.findall(r"([aA-zZ].*)30-", print_enroll)
            return '\t|_ ' + str(success)

        except:
            return ('\t|_ ' + 'Tombol enroll tidak ditemukan')


def main():

    # agar link udemy tetap fresh harus di hapus tiap kali menjalankan program
    try:
        os.remove("coupon-udemy.txt")
        print("[*] File berhasil di hapus ")

    except Exception as e:
        print(e)
        print("[*] Mungkin file sudah di hapus atau file belum terbuat\n")

    os.system("python3 udemyfreebies.py")
    os.system("python3 udemytutorialbar.py")

    os.system("clear")
    driver.get(url)

    # cek cookies
    if os.path.isfile("cookies-udemy.pickle"):
        print("[*] Cookies ditemukan")
        load_cookies(url)

    else:
        print("[*] Harus login! ")
        email = input("    Masukan email: ")
        password = input("    Masukan password: ")

        halaman_masuk_udemy(email, password)

    print("[*] Memulai enroll kursus")
    with open("coupon-tutorialbar.txt", 'r') as f:
        coupons = f.readlines()

    for coupon in coupons:
        print(baca_kupon_udemy(coupon))


if __name__ == "__main__":
    main()
