#!/usr/bin/python3
# coding: utf-8


from requests_html import HTMLSession
import requests
import os

session = HTMLSession()


def mengambil_url_mentah():
    """mengambil url mentahan dari website dan hasil url nya masih terbungkus"""

    url = "https://www.udemyfreebies.com/"
    response = session.get(url)

    get_coupon_page = response.html.find("#coupon-page", first=True)
    get_cols = get_coupon_page.find("div .col-md-4")

    for i in range(0, len(get_cols)):
        get_col = get_cols[i]
        get_theme_blocks = get_col.find("div .theme-block")

        for x in range(0, len(get_theme_blocks)):
            get_details = get_theme_blocks[x]
            get_detail = get_details.find("div .coupon-details")
            get_link_btns = get_detail[x].links

            for get_link_btn in get_link_btns:
                # print(get_link_btn)
                print(membuka_pembungkus_url_mentah(get_link_btn, x))
                simpan_kupon_udemy(get_link_btn)


def membuka_pembungkus_url_mentah(url_mentah, index):
    """setelah mendapatkan url mentah,request lagi untuk membuka pembungkus url mentah"""

    response = session.get(url_mentah)

    get_link_btns = response.html.find(".button-icon")[index].links

    for get_link in get_link_btns:
        # print(get_link)
        url_udemy = mengambil_url_udemy(get_link)

        return url_udemy


def mengambil_url_udemy(url):
    """setelah pembungkus terbuka request lagi untuk mendapatkan url udemy"""

    response = session.get(url)
    get_links = response.html.url

    return get_links


def simpan_kupon_udemy(url, tgl=""):
    """simpan url udemy"""

    with open("coupon-udemy.txt", "a") as coupon:
        coupon.write(str(url) + '\n')


def main():

    print("[*] Memulai scraping udemy-freebies\n")

    mengambil_url_mentah()


if __name__ == "__main__":
    main()
