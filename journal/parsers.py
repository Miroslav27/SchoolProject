
from requests_html import AsyncHTMLSession, HTMLSession
from lxml import etree
asession = AsyncHTMLSession()
session = HTMLSession()

#URL=https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5
#https://api.monobank.ua/bank/currency
#https://www.eximb.com/ua/business/pryvatnym-klientam/pryvatnym-klientam-inshi-poslugy/obmin-valyut/kursy-valyut.html
# https://lion-kurs.rv.ua/
# "https://vkurse.dp.ua/"

async def get_vkurse():
    res_vkurse = {}

    r = await asession.get("https://vkurse.dp.ua/")
    await r.html.arender()
    # print(r.html.search('<p id="euroBuy" class="pokupka-value">{eur}</p>')['eur'])
    res_vkurse["broker"] = "vkurse"
    res_vkurse["usd_buy"] = float(r.html.search('<p id="dollarBuy" class="pokupka-value">{usd}</p>')['usd'])
    res_vkurse["usd_sell"] = float(r.html.search('<p id="dollarSale" class="pokupka-value">{usd}</p>')['usd'])
    res_vkurse["eur_buy"] = float(r.html.search('<p id="euroBuy" class="pokupka-value">{eur}</p>')['eur'])
    res_vkurse["eur_sell"] = float(r.html.search('<p id="euroSale" class="pokupka-value">{eur}</p>')['eur'])
    return res_vkurse


# print(res_vkurse)
# instance = Currency(**res)
# instance.save()

def get_privat():
    res_privat = {}
    r = session.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    if r.ok:
        res_privat['broker'] = 'privat'
        res_privat['usd_buy'] = float(r.json()[1]["buy"])
        res_privat['usd_sell'] = float(r.json()[1]["sale"])
        res_privat['eur_buy'] = float(r.json()[0]["buy"])
        res_privat['eur_sell'] = float(r.json()[0]["sale"])
    # print(r.json())
    # print(res_privat)
    return res_privat


def get_mono():
    # 980/840 980/978
    res_mono = {}
    r = session.get('https://api.monobank.ua/bank/currency')
    if r.ok:
        res_mono["broker"] = "monobank"
        for kurs in r.json():
            if 840 == kurs["currencyCodeA"] and 980 == kurs["currencyCodeB"]:
                # print(kurs['rateBuy'],kurs['rateSell'])
                res_mono['usd_buy'] = float(kurs['rateBuy'])
                res_mono['usd_sell'] = float(kurs['rateSell'])
            if 978 == kurs["currencyCodeA"] and 980 == kurs["currencyCodeB"]:
                # print(kurs['rateBuy'], kurs['rateSell'])
                res_mono['eur_buy'] = float(kurs["rateBuy"])
                res_mono['eur_sell'] = float(kurs["rateSell"])
    return (res_mono)


async def get_ukrsib():
    res_ukrsib = {}
    res_ukrsib["broker"] = "ukrsib"
    r = await asession.get("https://ukrsibbank.com/currency-cash/")
    await r.html.arender()
    kurs_tree = etree.HTML(str(r.text))
    for kurs in kurs_tree.cssselect(
            '#exchange > div > div.exchange__list.exchange__list--cash > ul.exchange__wrap > li:nth-child(1) > div:nth-child(2) > div'):
        res_ukrsib["usd_buy"] = float(kurs.text.replace(",", "."))
    res_ukrsib["usd_sell"] = \
        [float(x.text.replace(",", ".")) for x in kurs_tree.cssselect(
            "#exchange > div > div.exchange__list.exchange__list--cash > ul.exchange__wrap > li:nth-child(1) > div:nth-child(3) > div")][
            0]
    kurs_xpath_tree = kurs_tree.xpath('//*[@id="exchange"]/div/div[2]/ul[2]/li[2]/div[2]/div')
    kurs_eur_buy = float([x.text for x in kurs_xpath_tree][0].replace(",", "."))
    res_ukrsib['eur_buy'] = kurs_eur_buy
    kurs_eur_sell = r.html.search_all('<div class="exchange__item-text">{text}</div>')[6]
    res_ukrsib['eur_sell'] = float(kurs_eur_sell["text"].replace(",", "."))
    return (res_ukrsib)


def get_lion():
    res_lion = {}
    r = session.get('https://lion-kurs.rv.ua/')
    if r.ok:
        res_lion['broker'] = "lion_rv"
        res_lion['usd_buy'] = float(r.html.search_all('<td class="white">{text}</td>')[0]["text"])
        res_lion['usd_sell'] = float(r.html.search_all('<td class="white">{text}</td>')[1]["text"])
        res_lion['eur_buy'] = float(r.html.search_all('<td class="white">{text}</td>')[2]["text"])
        res_lion['eur_sell'] = float(r.html.search_all('<td class="white">{text}</td>')[3]["text"])
    return (res_lion)
def parse_all():
    #asession = AsyncHTMLSession()
    #session = HTMLSession()
    results= []
    parsers = [get_lion, get_mono, get_privat]
    aparsers = [get_ukrsib,get_vkurse()]
    for aparser in aparsers:
        try:
            results.append(asession.run(aparser))
        except:pass
    for parser in parsers:
        try:
            results.append(parser())
        except:pass

    return results







"""
    asession.run(get_vkurse)
    get_privat()
    get_mono()
    asession.run(get_ukrsib)
    get_lion()
    print(res_lion,res_mono,res_privat,res_ukrsib,res_vkurse,sep='\n')
"""
