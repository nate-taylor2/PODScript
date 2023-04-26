# Must save each POD (pdf) as the order number.
# Must compile all PODs into a folder.
# Right click folder, and "copy as path."
# Last updated: 4/26/2023
# Created by Nate Taylor

import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from tkinter import Entry, Label, Tk, Button

# Grab Login Info
root = Tk()
root.title('TTR TOOLS')
root.geometry('450x240')

userText = Label(root, text = 'USERNAME: ', font = 1, pady = 5)
passText = Label(root, text = 'PASSWORD: ', font = 1, pady = 5)
pinText = Label(root, text = 'PIN: ', font = 1, pady = 5)
dirText = Label(root, text = 'DIRECTORY: ', font = 1, pady = 5)
extraText = Label(root, text = '(Format: C:\\users\\name\\desktop\\PODs4_26)', pady = 5)
userBox = Entry(root)

passBox = Entry(root)

pinBox = Entry(root)

dirBox = Entry(root, width = 50)

submit = Button(text = 'LOGIN', padx = 40, bg = 'orange', pady = 5, font = 3, command = lambda: getLogin())

userText.grid(row = 0, column = 0, sticky = 'w')
passText.grid(row = 1, column = 0, sticky = 'w')
pinText.grid(row = 2, column = 0, sticky = 'w')
dirText.grid(row = 3, column = 0, sticky = 'w')
userBox.grid(row = 0, column = 1, sticky = 'w')
passBox.grid(row = 1, column = 1, sticky = 'w')
pinBox.grid(row = 2, column = 1, sticky = 'w')
dirBox.grid(row = 3, column = 1, sticky = 'w')
extraText.grid(row = 4, columnspan = 2, sticky = 'w')
submit.grid(row = 5, column = 1, sticky = 'w')


def getLogin():
    global user, pw, pin, direct
    user = userBox.get()
    pw = passBox.get()
    pin = pinBox.get()
    direct = dirBox.get()

    if user and pw and pin and direct != '':
        root.destroy()
    else:
        print('Invalid Login Info')

root.mainloop()

# Open folder with files saved as order numbers
def openFolder(direct):
    print('\n')
    print('\n')
    tempFiles = []
    # Check that folder input is a valid directory and contains PODs
    if direct[:9] == 'C:\\Users\\':
        os.chdir(direct)
        for file in os.listdir():
            tempFiles.append(file)
            if len(file) == 10 and file[-4:] == '.pdf':
                continue
            else:
                print('This folder contains files that are not in the correct format. Please try again.\n')
                openFolder()
    else:
        print('\nInvalid Directory, please try again.\n')
        openFolder()

    print('\n\nConfirm you want to upload these', len(tempFiles), 'PODs:\n')
    for i in tempFiles:
        print(i)

    confirm = input('\nType Y/N: ')
    if confirm == 'Y' or 'y':
        print('Uploading the PODs for:', direct)
    elif confirm == 'N' or 'n':
        print('Cancelling.')
        openFolder()

    return direct

# Create session
def driver(directory, user, pw, pin):
    path = '/path/to/chromedriver'
    url = 'https://ome.ttrshipping.com'
    service = Service(executable_path = path)

    response = requests.get(url)
    if response.status_code == 200:
        driver = webdriver.Chrome(service = service)
        driver.get(url)

        try:
            # LOGIN 
            usernameInp = driver.find_element('id','ContentPlaceHolder1_TextBoxUserName')
            usernameInp.send_keys(user)
            
            passwordInp = driver.find_element('id','ContentPlaceHolder1_TextBoxPassword')
            passwordInp.send_keys(pw)
            
            pinInp = driver.find_element('id','ContentPlaceHolder1_TextBoxPIN')
            pinInp.send_keys(pin)
            
            submitButton = driver.find_element('id','ContentPlaceHolder1_ButtonLogin')
            submitButton.click()
            # REQUEST SENT!!!!!!!!!!
            time.sleep(7)

        except Exception as e:
            print('An exception error occurred while trying to login: ', e)
            driver.quit()

        # Navigate to Delivery Tab
        orderTab = driver.find_element('id','hrefdelivery')
        orderTab.click()
        # REQUEST SENT!!!!!!!!!!
        time.sleep(5)

        # Click Documents Button
        docButton = driver.find_element('id','ContentPlaceHolder1_LinkButtonDocs')
        docButton.click()
        # REQUEST SENT!!!!!!!!!!
        time.sleep(4)

        # LOOP THROUGH EACH FILE AND UPLOAD EACH POD
        os.chdir(directory)
        for file in os.listdir(directory.replace('\\\\','\\')):
            
            orderNumBox = driver.find_element('id','ContentPlaceHolder1_TextBoxOrderNumbers')
            orderNumBox.send_keys(file[:6])

            findOrdersButton = driver.find_element('id','ContentPlaceHolder1_ButtonFind')
            findOrdersButton.click()
            # REQUEST SENT!!!
            time.sleep(4)
            

            # Click List Dropdown
            dropdownBox = driver.find_element('id','ContentPlaceHolder1_DropDownListDocType')
            dropdownBox.click()

            # Click Proof of Delivery
            dropdownPOD = driver.find_element('xpath',"//option[@value='8']")
            dropdownPOD.click()

            # Click Choose File, and send path
            chooseFile = driver.find_element('id','ContentPlaceHolder1_FileUploadControl')
            chooseFile.send_keys(directory + '\\' + file)

            # Click Upload
            uploadButton = driver.find_element('id','ContentPlaceHolder1_ButtonUpload')
            uploadButton.click()
            # REQUEST SENT!!!
            time.sleep(4)

            print('\nPOD for order number: ' + file[:6] + ' successfully uploaded.') 

            orderNumBoxClear = driver.find_element('id','ContentPlaceHolder1_TextBoxOrderNumbers')
            orderNumBoxClear.clear()

    else:
        time.sleep(30)
        print('Page failed to load, trying again in 30 seconds.')
        driver()

# Call the open folder function to get user input and confirm directory validity
directory = openFolder(direct)
# Call the driver function to create the webdriver object
driver(directory, user, pw, pin)