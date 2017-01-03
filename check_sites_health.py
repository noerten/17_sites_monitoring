import datetime
import os

import requests
import whois


NUMBER_OF_DAYS_PAID = 30


def load_url_file(path):
    if not os.path.exists(path):
        return None
    with open(path) as text_file:
        return text_file.read()


def get_url_list(text_file):
    raw_url_list = text_file.split('\n')
    return [one_url.strip() for one_url in raw_url_list if one_url != '']


def does_server_respond_with_200(url):
    return requests.head(url).status_code == 200


def get_domain_expiration_date(domain_name):
    whois_object = whois.whois(domain_name)
    if type(whois_object.expiration_date) is not datetime.datetime:
        return whois_object.expiration_date[0]
    else:
        return whois_object.expiration_date


def is_paid_month_ahead(expiration_date):
    date_n_days_ahead = datetime.datetime.today() + datetime.timedelta(
        days=NUMBER_OF_DAYS_PAID)
    return expiration_date > date_n_days_ahead


if __name__ == '__main__':
    filepath = input('Enter file name/path: ')
    url_file = load_url_file(filepath)
    url_list = get_url_list(url_file)
    print("Website", "| responds 200", "| Prepaid atleast for month ahead")
    for one_url in url_list:
        expiration_date = get_domain_expiration_date(one_url)
        print(one_url, does_server_respond_with_200(one_url),
              is_paid_month_ahead(expiration_date))
