#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json


# In[62]:


# Define the API endpoint URL
api_url = 'http://localhost:6767/predict'  # Replace with your API URL

# Sample input data as JSON
# input_data = [{
#     "product_id" : "tv1",
#     "actual_price": 1200,
#     "competitor1": 1000,
#     "competitor2": 1100,
#     "competitor3": 1050,
#     "competitor4": 950,
#     "competitor5": 980,
#     "product_type": "electronics"
# }]

input_data = [
    {
        "position": 1,
        "title": "Google Pixel 7 Pro - 128 GB - Snow - Unlocked",
        "link": "https://store.google.com/us/config/pixel_7_pro?srsltid=AfmBOori8AZVqIykUidQ58RbUuPPpPLr-JOiz3u3rQixPa-KlEHF7HTr-hM",
        "product_link": "https://www.google.com/shopping/product/15169918534433587853?gl=us",
        "product_id": "15169918534433587853",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=15169918534433587853",
        "number_of_comparisons": "10+",
        "comparison_link": "https://www.google.com/shopping/product/15169918534433587853/offers?gl=us&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&hl=en&q=query_string%3DGoogle+Pixel+7+Pro&prds=eto:1429711858013942727_0,pid:11018721410002916832,rsk:PC_6023854479048717292&sa=X&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECN0N",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A1429711858013942727_0%2Cpid%3A11018721410002916832%2Crsk%3APC_6023854479048717292&hl=en&offers=1&product_id=15169918534433587853&sa=X&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECN0N",
        "source": "Google Store",
        "price": "$899.00",
        "extracted_price": 899.0,
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQGBUlMdWjHP3WKJZWeQPApScLYvO0BDQqJJg9xS3S31IyNNdxy_0J-DiCKPek&usqp=CAE",
        "delivery": "Free delivery"
    },
    {
        "position": 2,
        "title": "Google Pixel 7 Pro | Unlocked | Obsidian | 128 GB",
        "link": "https://www.ebay.com/itm/256521246107?chn=ps&mkevt=1&mkcid=28&srsltid=AfmBOoq7fznro-5GhdSpehfZoDk0C1uSqKTyxXszSbBbGcyONqZYwNCKVmY&com_cvv=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e",
        "product_link": "https://www.google.com/shopping/product/2178543973361632735?gl=us",
        "product_id": "2178543973361632735",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=2178543973361632735",
        "number_of_comparisons": "10+",
        "comparison_link": "https://www.google.com/shopping/product/2178543973361632735/offers?gl=us&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&hl=en&q=query_string%3DGoogle+Pixel+7+Pro&prds=eto:6757750269104099361_0,pid:9445730519170029428,rsk:PC_12659412856873390207&sa=X&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECO4N",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A6757750269104099361_0%2Cpid%3A9445730519170029428%2Crsk%3APC_12659412856873390207&hl=en&offers=1&product_id=2178543973361632735&sa=X&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECO4N",
        "source": "eBay - wirelesssdepot",
        "price": "$195.01",
        "extracted_price": 195.01,
        "second_hand_condition": "used",
        "rating": 4.5,
        "reviews": 556,
        "thumbnail": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRKzMI1ILT3_DGVlqOwilsGVFwxpZK9q9FlZXIyffofyRC_CRsImqNjOOAvxQ&usqp=CAE",
        "delivery": "Free delivery by Mon, Jul 8"
    },
    {
        "position": 3,
        "title": "Smartphone Google Pixel 7 Pro 128 GB",
        "link": "https://www.walmart.com/ip/Restored-Google-Pixel-7-Pro-128GB-Spectrum-Locked-Obsidian-Refurbished/5194928448?wmlspartner=wlpa&selectedSellerId=3628",
        "product_link": "https://www.google.com/shopping/product/13679582481398876053?gl=us",
        "product_id": "13679582481398876053",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=13679582481398876053",
        "number_of_comparisons": "2",
        "comparison_link": "https://www.google.com/shopping/product/13679582481398876053/offers?gl=us&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&hl=en&q=query_string%3DGoogle+Pixel+7+Pro&prds=eto:610318197907012797_0,pid:7210004154757958363,rsk:PC_6023854479048717292&sa=X&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECP4N",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A610318197907012797_0%2Cpid%3A7210004154757958363%2Crsk%3APC_6023854479048717292&hl=en&offers=1&product_id=13679582481398876053&sa=X&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECP4N",
        "source": "Walmart - Mobile Shop",
        "price": "$349.99",
        "extracted_price": 349.99,
        "second_hand_condition": "refurbished",
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQQU_WDWDq9lRMn2s1VsO_O9azc2rX6bquTceXNQNxivGisTFegY1zNEtTRcg&usqp=CAE",
        "delivery": "$45.00 delivery"
    },
    {
        "position": 4,
        "title": "Google Pixel 7 Pro 128GB Hazel Unlocked Smartphone - 12 Months Warranty",
        "link": "https://reebelo.com/products/google-pixel-7-pro-128-gb-hazel-12-gb-ram-fully-unlocked-pristine-pqr9i&utm_organicad=true?srsltid=AfmBOorj0oaTPo29Olr1CFIE28CbPfHdkUv2zTZZZZ7JOaNxLlI7Sd9yBoY",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:13339413675381839438",
        "product_id": "13339413675381839438",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=13339413675381839438",
        "source": "Reebelo USA",
        "price": "$399.00",
        "extracted_price": 399.0,
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRYqpz_IG5UPgh41tfmx8URnUf4n6WF2UY9dMqwqD-yLPzHjBGoN8UEnu1_ksw&usqp=CAE",
        "delivery": "Free delivery by Wed, Jul 3"
    },
    {
        "position": 5,
        "title": "Google Pixel 7 - 128 GB - Lemongrass - Unlocked",
        "link": "https://www.target.com/p/google-pixel-7-5g-unlocked-128gb-smartphone-lemongrass/-/A-87361069?ref=tgt_adv_xsf&AFID=google&CPNG=Electronics&adgroup=80-6&lnm=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e",
        "product_link": "https://www.google.com/shopping/product/9035097249628994289?gl=us",
        "product_id": "9035097249628994289",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=9035097249628994289",
        "number_of_comparisons": "10+",
        "comparison_link": "https://www.google.com/shopping/product/9035097249628994289/offers?gl=us&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&hl=en&q=query_string%3DGoogle+Pixel+7+Pro&prds=eto:6306460734819596533_0,pid:15365577240069642693,rsk:PC_16632475449553064166&sa=X&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECKEO",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A6306460734819596533_0%2Cpid%3A15365577240069642693%2Crsk%3APC_16632475449553064166&hl=en&offers=1&product_id=9035097249628994289&sa=X&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECKEO",
        "source": "Target",
        "price": "$599.00",
        "extracted_price": 599.0,
        "rating": 4.2,
        "reviews": 3687,
        "badge": "Top Quality Store",
        "thumbnail": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRyEOY-pbBjBvkm1hnMzE1Lx_KqbHEadr9sLW3TKicpz1XAbzN3fNgitg39FYzamrULEZPWUCHD&usqp=CAE",
        "tag": "FREE 2-DAY",
        "extensions": [
            "FREE 2-DAY"
        ],
        "delivery": "Free delivery by Wed, Jul 3"
    },
    {
        "position": 6,
        "title": "Google Pixel 7 Pro - 128 GB - Obsidian - AT&T",
        "link": "https://www.amazon.com/Google-Pixel-Pro-Version-Obsidian/dp/B0CNZF9DHL?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A39YHAI3NCE75F",
        "product_link": "https://www.google.com/shopping/product/12628552975825606726?gl=us",
        "product_id": "12628552975825606726",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=12628552975825606726",
        "number_of_comparisons": "10+",
        "comparison_link": "https://www.google.com/shopping/product/12628552975825606726/offers?gl=us&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&hl=en&q=query_string%3DGoogle+Pixel+7+Pro&prds=eto:10395390744340087570_0,pid:11551969161071740592,rsk:PC_6023854479048717292&sa=X&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECLEO",
        "serpapi_product_api_comparisons": "https://serpapi.com/search.json?engine=google_product&filter=eto%3A10395390744340087570_0%2Cpid%3A11551969161071740592%2Crsk%3APC_6023854479048717292&hl=en&offers=1&product_id=12628552975825606726&sa=X&uule=w+CAIQICIaQXVzdGluLFRleGFzLFVuaXRlZCBTdGF0ZXM&ved=0ahUKEwiTzer81v6GAxU2v4kEHebBBxoQ3q4ECLEO",
        "source": "Amazon.com - Seller",
        "price": "$349.98",
        "extracted_price": 349.98,
        "second_hand_condition": "refurbished",
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQiQhC1cDriXo8iWZHICsjlmnfxTrFLPxr8c6ehwtFA1n8yV5FgslRQJwEQBQvpP2jqNKer2Cs&usqp=CAE",
        "delivery": "Free delivery"
    },
    {
        "position": 7,
        "title": "Google Pixel 7 Pro 128GB - White - Unlocked",
        "link": "https://www.backmarket.com/en-us/p/google-google-pixel-7-pro-128-gb-hazel-fully-unlocked-gsm-cdma/774a6919-6e31-470d-af91-dea84d62084f?shopping=gmc&srsltid=AfmBOoqpT2ucHDDuAXygmWZfac8qLhLAJrStwHH0aJw8aj3ZRMVCeCR8oTI",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:17050633983488848034",
        "product_id": "17050633983488848034",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=17050633983488848034",
        "source": "Back Market",
        "price": "$381.78",
        "extracted_price": 381.78,
        "old_price": "$899.99",
        "extracted_old_price": 899.99,
        "second_hand_condition": "refurbished",
        "rating": 4.4,
        "reviews": 4599,
        "badge": "Top Quality Store",
        "thumbnail": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTrF2rg91Ebf9Uk1ckhsCUmbAvWvWPixG1-qJlGMJpcmEMbYWsC3FbXStpSmEc&usqp=CAE",
        "tag": "SALE",
        "extensions": [
            "SALE"
        ],
        "delivery": "Delivery by Mon, Jul 8"
    },
    {
        "position": 8,
        "title": "Google Pixel 7 Pro - 256 Gb - White (unlocked) (dual Sim (sim + Esim))",
        "link": "https://www.ebay.com/itm/166816081130?chn=ps&mkevt=1&mkcid=28",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:15449032278205672404",
        "product_id": "15449032278205672404",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=15449032278205672404",
        "source": "eBay",
        "price": "$229.95",
        "extracted_price": 229.95,
        "second_hand_condition": "used",
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRC6-pDtVShtlF2I6M8dxwU7Y5wKJr3im28I6SisD-ETFFZL0UlG72Ch_ZJ6ec&usqp=CAE",
        "delivery": "Delivery by Wed, Jul 10"
    },
    {
        "position": 9,
        "title": "Google Pixel 7 Pro",
        "link": "https://q1.cricketwireless.com/product/google-pixel-7-pro/",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:16519101739992123383",
        "product_id": "16519101739992123383",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=16519101739992123383",
        "source": "Cricket Wireless",
        "price": "$569.00",
        "extracted_price": 569.0,
        "thumbnail": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSvzLd8ms9XY3xtEMhFjMV8OO_GH7wdt8191LKbd6PPAcBgXZwyMelF0sh6mlpNHRRqg7ks14pH&usqp=CAE",
        "delivery": "Free delivery by Tue, Jul 2"
    },
    {
        "position": 10,
        "title": "Google Geek Squad Certified Refurbished Pixel 7 Pro 128GB (Unlocked) - Snow",
        "link": "https://realry.com/products/6615012e61bcc6a54f061c4c?srsltid=AfmBOooVT52LOvB60TKvfOYIHuj60UH7kkz_mXR9jumt4Ba1VFQDyMf7Jks",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:2261697338142903497",
        "product_id": "2261697338142903497",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=2261697338142903497",
        "source": "Realry",
        "price": "$259.99",
        "extracted_price": 259.99,
        "second_hand_condition": "used",
        "rating": 4.4,
        "reviews": 4599,
        "thumbnail": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRGIkLwGSxKNRZxXZMQhdX4En_SbPjOcvdcxCZ9U4aARrr_O-f7EcLs44w6FbiKH_WD6lUIycE&usqp=CAE",
        "delivery": "Free delivery"
    },
    {
        "position": 11,
        "title": "Google Pixel 7 Pro - Electronics | Color: White",
        "link": "https://www.mercari.com/us/item/m51860009630/?srsltid=AfmBOooqf5DSrApfSp2pNFhhXdNUAgD39s9cLtLeIq0GxMZulmZVRdgOcOM&com_cvv=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:2344796447774360543",
        "product_id": "2344796447774360543",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=2344796447774360543",
        "source": "Mercari",
        "price": "$260.00",
        "extracted_price": 260.0,
        "old_price": "$335.00",
        "extracted_old_price": 335.0,
        "second_hand_condition": "used",
        "thumbnail": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQqID-WwislfWFJLu4D6Eln7rKDOyZuZ0NGJaZgAGdEUgbYGVGLZJqJvTHF1i0&usqp=CAE",
        "tag": "SALE",
        "extensions": [
            "SALE"
        ],
        "delivery": "Free delivery"
    },
    {
        "position": 12,
        "title": "Google Pixel 7 Pro Unlocked 5G - Obsidian Smartphone; GSM/CDMA; 8 GB RAM/256 GB ...",
        "link": "https://www.microcenter.com/product/676055/Pixel_7_Pro_Unlocked_5G_-_Obsidian_Smartphone;_GSM-CDMA;_8_GB_RAM-256_GB_Storage;_67''_LTPO_AMOLED_Display;_50_Megapixel_Camera;_Android_13;_Single_Na",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:9038666531091560539",
        "product_id": "9038666531091560539",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=9038666531091560539",
        "source": "Micro Center",
        "price": "$469.99",
        "extracted_price": 469.99,
        "thumbnail": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRuZy2b4B0d1s0i1feOS5m812bzoMrxZ0UdMRrJInSxJjJwBkc&usqp=CAE",
        "delivery": "$5.99 delivery"
    },
    {
        "position": 13,
        "title": "Google Pixel 7 Pro - 5G Smartphone - Dual-SIM - Ram 12 GB / Internal Memory 128 ...",
        "link": "https://www.newegg.com/p/N82E16875505083?item=9SIAC8UK7F7355&nm_mc=knc-googleadwords&cm_mmc=knc-googleadwords-_-cell+phones+-+no+contract+phone-_-google-_-9SIAC8UK7F7355&utm_source=google&utm_medium=organic+shopping&utm_campaign=knc-googleadwords-_-cell+phones+-+no+contract+phone-_-google-_-9SIAC8UK7F7355&source=region&srsltid=AfmBOopdXJQ1JlbwGL15iXTkkiKknir8LFCsa3mzdT4CV5G4q7KU7exzhQI&com_cvv=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e",
        "product_link": "https://www.google.com/shopping/product/8303050205076014837?gl=us",
        "product_id": "8303050205076014837",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=8303050205076014837",
        "source": "Newegg.com - Calipaks",
        "price": "$419.00",
        "extracted_price": 419.0,
        "second_hand_condition": "used",
        "rating": 4.5,
        "reviews": 556,
        "thumbnail": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQP6cJSg6N3znsFKNNfuKXaOrSefyOztLWJ-kW7Dw5UJ3AgGMuVraLw91iDKm-zyWZRI5pdABC-&usqp=CAE",
        "delivery": "Free delivery"
    },
    {
        "position": 14,
        "title": "Google Pixel 7 Pro Duos - Ge2ae - 128gb - Snow (unlocked) (s21993)",
        "link": "https://www.ebay.com/itm/266860387408?chn=ps&mkevt=1&mkcid=28&srsltid=AfmBOorrWnVivB6FW6qs0s13YtVNClVvFILBpXXg6PyBXhKYdH4G17kdbQg&com_cvv=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e",
        "product_link": "https://www.google.com/shopping/product/1?gl=us&prds=pid:17593501751967283583",
        "product_id": "17593501751967283583",
        "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&location=Austin%2C+Texas&product_id=17593501751967283583",
        "source": "eBay - wirelesssdepot",
        "price": "$238.90",
        "extracted_price": 238.9,
        "second_hand_condition": "used",
        "thumbnail": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRcv6tYK6Gj39RMRKZH4HfxrpRQ3M6jo4Jc7C5auZDtzZddeAjsSnkCoX523gVjXVLaL6qDGsQ&usqp=CAE",
        "delivery": "Free delivery by Mon, Jul 8"
    }
]

# Convert dict to JSON string
json_data = json.dumps(input_data)

# Send POST request to the API
response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response JSON
    print(response.json())
else:
    # Print error message if request failed
    print(f"Error: {response.text}")


# In[ ]:





# In[ ]:




