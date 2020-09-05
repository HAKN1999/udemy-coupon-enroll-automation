#!/usr/bin/python3
# coding: utf-8


from requests_html import HTMLSession
import requests
import os

session = HTMLSession()


def memgambil_url_mentah(page=1):
    """mengambil url mentahan dari website yang hasil nya masih terbungkus"""

    get_h3_tags = []

    url = 'https://www.tutorialbar.com/all-courses/page/{page}/'.format(
        page=page)
    response = session.get(url)
    get_pages = response.html.find("#page-19")

    for get_page in get_pages:
        get_cols = get_page.find("div .content_constructor")
        for get_col in get_cols:
            get_h3_tags.append(get_col)

    for get_h3_tag in get_h3_tags:
        for get_h3 in get_h3_tag.find("h3"):
            for links in get_h3.links:
                print(links)
                url_udemy(links)


def url_udemy(url_mentah):
    """membuka bungkus url dan request lagi untuk mengambil url udemy"""

    response = session.get(url_mentah)
    get_pages = response.html.find("div .text-center")

    for get_page in get_pages:
        for get_btn_offers in get_page.find(".btn_offer_block"):
            for get_btn_offer in get_btn_offers.links:
                #                 print(get_btn_offer)
                simpan_kupon_udemy(get_btn_offer)


def simpan_kupon_udemy(url):
    """simpan url udemy"""

    with open("coupon-tutorialbar.txt", "a") as coupon:
        coupon.write(str(url) + '\n')


def main():

    memgambil_url_mentah()


if __name__ == "__main__":
    main()
