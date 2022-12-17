'''
Author: Josh Sowder
Program: Price Comparison Tool - Final Project
Course: SDEV 140
Date: 12/16/2022
'''

from tkinter import *
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

class PCT:
    def __init__(self):
        window = Tk()
        window.title("Price Comparison Tool")
        window.geometry("+500+300")

        frame = Frame(window)
        frame.pack()

        self.v1 = StringVar()
        self.search = Entry(frame, width = 125, textvariable = self.v1).grid(row = 1, column = 1, columnspan = 15, padx = 10, pady = 10)
        self.searchBt = Button(frame, text = "Search", command = self.displayItems(webscraper(self.v1.get()))).grid(row = 1, column = 16, pady = 10, ipadx = 4, ipady = 2)
        self.display = PanedWindow(frame, width = 175, height = 50).grid(row = 2, column = 1, rowspan = 25, columnspan = 25, padx = 10, pady = 10)
        self.displayWindow = PanedWindow(self.display, orient = VERTICAL)
        self.item1 = Canvas(self.displayWindow, yscrollcommand = TRUE)
        self.scroll1 = Scrollbar(self.item1, orient = VERTICAL).set(0, 1)
        self.item2 = Canvas(self.displayWindow, yscrollcommand = TRUE)
        self.scroll2 = Scrollbar(self.item2, orient = VERTICAL).set(0, 1)
        self.item3 = Canvas(self.displayWindow, yscrollcommand = TRUE)
        self.scroll3 = Scrollbar(self.item3, orient = VERTICAL).set(0, 1)
        self.displayWindow.add(self.item1)
        self.displayWindow.add(self.item2)
        self.displayWindow.add(self.item3)
        self.comparator = Listbox(frame, width = 60, height = 50, yscrollcommand = VERTICAL).grid(row = 2, column = 26, rowspan = 25, columnspan = 8, padx = 10, pady = 10)
        self.scroll4 = Scrollbar(self.comparator, orient = VERTICAL).set(0, 1)

        window.mainloop()
       
    def displayItems(self, df1, df2, df3):
        self.item1.itemconfigure(window = df1)
        self.item2.itemconfigure(window = df2)
        self.item3.itemconfigure(window = df3)

def webscraper(searchitem):
    count = 0
    #Adapted from example code - edureka.com/blog/web-scraping-with-python/
    #Credit: Omkar S Hiremath
    driver = webdriver.Chrome("D:\Program Files (x86)\ChromeDriver\chromedriver")
    products=[] #List to store name of the product
    prices=[] #List to store price of the product
    ratings=[] #List to store rating of the product
    while count <= 3:
        if count == 1:
            driver.get("https://www.amazon.com/s?k=" + searchitem)
            content = driver.page_source
            soup = BeautifulSoup(content)
            for a in soup.findAll(searchitem, href = True, attrs = {'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16'}):
                name=a.find('div', attrs = {'class':'a-section a-spacing-none puis-padding-right-small s-title-instructions-style'})
                price=a.find('div', attrs = {'class':'a-section a-spacing-none a-spacing-top-micro s-price-instructions-style'})
                rating=a.find('div', attrs = {'class':'a-section a-spacing-none a spacing-top-micro'})
                products.append(name.text)
                prices.append(price.text)
                ratings.append(rating.text)
            df1 = pd.DataFrame({'Product Name':products, 'Price':prices, 'Rating':ratings}) 
            df1.to_csv('products.csv', index=False, encoding='utf-8') #For testing and debugging
        elif count == 2:
            driver.get("https://www.walmart.com/search?q=" + searchitem)
            content = driver.page_source
            soup = BeautifulSoup(content)
            for a in soup.findAll(searchitem, href = True, attrs = {'class':'mb1 ph1 pa0-xl bb b--near-white w-25'}):
                name=a.find('div', attrs = {'class':'w_V_DM'})
                price=a.find('div', attrs = {'class':'flex flex-wrap justify-start items-center lh-title mb2 mb1-m'})
                rating=a.find('div', attrs = {'class':'flex items-center mt2'})
                products.append(name.text)
                prices.append(price.text)
                ratings.append(rating.text)
            df2 = pd.DataFrame({'Product Name':products, 'Price':prices, 'Rating':ratings}) 
            df2.to_csv('products.csv', index=False, encoding='utf-8') #For testing and debugging
        else:
            driver.get("https://www.target.com/s?searchTerm=" + searchitem)
            content = driver.page_source
            soup = BeautifulSoup(content)
            for a in soup.findAll(searchitem, href = True, attrs = {'class':'Grid__StyledGrid-sc-1vq3yub0 bWTrMu'}):
                name=a.find('div', attrs = {'class':'h-display-flex'})
                price=a.find('div', attrs = {'class':'h-padding-r-tiny'})
                rating=a.find('div', attrs = {'class':'RatingStars__RatingStarsContainer-sc-k7ad82-2 lcJVIa'})
                products.append(name.text)
                prices.append(price.text)
                ratings.append(rating.text)
            df3 = pd.DataFrame({'Product Name':products, 'Price':prices, 'Rating':ratings}) 
            df3.to_csv('products.csv', index=False, encoding='utf-8') #For testing and debugging
        count += 1
    return df1, df2, df3

def main():
    pct = PCT()

main()
