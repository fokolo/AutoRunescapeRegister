import time
from selenium import webdriver
import selenium.common.exceptions
import sys
import logging

temp_mail = 'http://temp-mail.org/'
start_runscape_login = 'https://secure.runescape.com/m=account-creation/g=oldscape/create_account'

form_values = {
    'age': '22',
    'charactername': 'TestFFs12345',
    'email1': 'lolkkksdf@sadfhh.csd',
    'password1': 'Aag425fd',
    'password2': 'Aag425fd',
}

ATTEMPTS = 20
WAIT_TIME_FOR_MAIL = 10

logging.basicConfig()
LOG = logging.getLogger()

LOG_FILE = r'c:\Temp\log_file'

def main():
    mail_browser = webdriver.PhantomJS()
    mail_browser.get(temp_mail)

    email_addr = mail_browser.find_element_by_xpath('//*[@id="mail"]').get_attribute('value')
    form_values['email1'] = email_addr

    browser = webdriver.Chrome()
    browser.get(start_runscape_login)

    for elem in browser.find_elements_by_xpath('//input[@class]'):
        try:
            elem.send_keys(form_values[format(elem.get_attribute('id'))])
        except KeyError:
            continue

    browser.switch_to.frame(0)
    checkbox = browser.find_element_by_xpath("//div[@class='recaptcha-checkbox-checkmark']")
    checkbox.click()

    while browser.find_element_by_xpath('//*[@id="recaptcha-anchor"]').get_attribute('aria-checked') != 'true':
        time.sleep(5)

    browser.switch_to.default_content()

    try:
        is_name_taken = browser.find_element_by_xpath('//*[@id="characternameAltsInner"]/span[1]')
        LOG.debug('New username: ' + str(is_name_taken.text))
        form_values['charactername'] = is_name_taken.text
        is_name_taken.click()
    except selenium.common.exceptions.ElementNotVisibleException:
        pass

    browser.find_element_by_xpath('//*[@id="submit"]').click()

    LOG.debug('Waiting for form to submit')
    resend_btn = None
    while True:
        try:
            resend_btn = browser.find_element_by_xpath('//*[@id="account-resend"]')
            break
        except:
            time.sleep(1)
            LOG.debug('.')
            continue
    LOG.debug('Done')

    for i in range(ATTEMPTS):
        time.sleep(WAIT_TIME_FOR_MAIL)
        try:
            mail_browser.find_element_by_xpath('//*[@id="mails"]/tbody/tr/td[4]/a').click()
            break
        except selenium.common.exceptions.NoSuchElementException:
            LOG.warning('Attempt {} failed of reading mail...'.format(i))
            if resend_btn is not None:
                resend_btn.click()
                resend_btn = None
            continue

    time.sleep(3)

    for elem in mail_browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[4]/table/tbody/tr/td/table[2]/tbody/tr/td/a'):
        LOG.debug('HREF:', elem.get_attribute('href'))
        if 'https://secure.runescape.com/m=email-register/submit_code.ws' in elem.get_attribute('href'):
            browser.get(elem.get_attribute('href'))

    success = browser.find_element_by_xpath('//*[@id="optout"]/div[1]/div/div/div[2]/div/h3').text
    if success == 'Creation Successful':
        'Account created.'

    print 'Account Created:', form_values

    log_file = open(LOG_FILE, 'a')
    log_file.write('New account: ' + str(form_values) + '\r\n')
    log_file.close()

    browser.close()
    mail_browser.close()


if __name__ == '__main__':
    while True:
        main()
