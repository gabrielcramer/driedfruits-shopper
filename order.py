#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os, time, sys
from collections import OrderedDict

def get_weight(product_weight):
    product_weight = product_weight.lower()
    if "kg" in product_weight:
        return 1000 * float(product_weight.strip('kg '))
    elif "g" in product_weight:
        return float(product_weight.strip('g '))
    else:
        return 0

def main():
    # Add geckodriver location to PATH environment variable
    os.environ["PATH"] += ":" + "include/"
    if len(sys.argv) != 4:
        print ("Usage:", sys.argv[0], "[email] [password] [products]")
        return
    email = sys.argv[1]
    password = sys.argv[2]
    file_name = sys.argv[3]
    driver = webdriver.Firefox()
    driver.get("https://driedfruits.ro/index.php?route=account/login")
    wait = WebDriverWait(driver, 20)
    # Login action. Close the driver if the page is not loaded or some of the elements can't be found
    try:
        wait.until(EC.presence_of_element_located((By.NAME,"email")))
        email_field = driver.find_element_by_name("email")
        email_field.send_keys(str(email))
        password_field = driver.find_element_by_name("password")
        password_field.send_keys(str(password))
        button = driver.find_element_by_xpath("//input[@value='Autentificare' and @type='submit']")
        button.click()
        return
    except:
        driver.quit()
        return
    try:
        with open(file_name) as f:
            raw_products = [tuple(reversed(line.split('\t'))) for line in ( line.strip() for line in f ) if line]
    finally:
        f.close()

    products = dict()
    for t in raw_products:
        if t[0] in products:
            products[t[0]] += int(t[1])
        else:
            products[t[0]] = int(t[1])

    count = 0
    total_weight = 0
    total_cost = 0
    items = 0
    total = len(products)
    for link in products:
        count += 1
        items += products[link]
        driver.get(link)
        product_types = driver.find_elements_by_class_name('radio-type-button2')
        price = driver.find_element_by_id('price-old').text
        full_product_name = driver.find_element_by_class_name('product-name').text
        product_name = full_product_name.split('-')[0].strip()
        product_weight = full_product_name.split('-')[-1].strip()
        total_weight += get_weight(product_weight) * products[link]
        total_cost += float(price.strip("Ron").replace(",",".")) * products[link]
        if product_types:
            if product_weight != 0:
                for pt in product_types:
                    if pt.text == product_weight:
                        pt.click()
            else:
                product_types[0].click()

        print("{0:2d}/{1:2d} Name: {2:<60s} Weight/Volume: {3:>7s} Quantity: {4:<2d} Price: {5:>9s}".format(count, total, product_name, product_weight, products[link], price))

        if products[link] > 1:
            quantity_field = driver.find_element_by_id('quantity_wanted')
            quantity_field.clear()
            quantity_field.send_keys(products[link])

        wait.until(EC.element_to_be_clickable((By.ID,'button-cart')))
        add_button = driver.find_element_by_id('button-cart')
        add_button.click()
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'alert-success')))
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,'alert-success')))
        except:
            continue
    print("{0} \nSuccessfully added to your shopping cart {1} items with a total weight greater than {2} kg. Total cost: {3} RON \n{0}".format('='*125, items, total_weight/1000, total_cost))


if __name__ == "__main__":
    main()
