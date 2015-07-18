#!/usr/bin/env python
from argparse import ArgumentParser
import os
import sys

import requests

API_BASE_URL = 'https://api.cloudflare.com/client/v4'

def fetch_public_ip():
    return requests.get('http://jsonip.com').json()['ip']

class CloudFlare(object):
    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email

    def find_zone(self, **kwargs):
        response = self.get('/zones', params=kwargs)
        return response.json()['result'][0]

    def find_dns_record(self, zone_id, **kwargs):
        response = self.get('/zones/{}/dns_records'.format(zone_id), params=kwargs)
        return response.json()['result'][0]

    def update_dns_record(self, dns_record):
        response = self.put('/zones/{}/dns_records/{}'.format(dns_record['zone_id'], dns_record['id']), json=dns_record)
        return response.json()['result']

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)
    
    def put(self, url, **kwargs):
        return self.request('put', url, **kwargs)

    def request(self, method, url, **kwargs):
        headers = {
            'X-Auth-Key': self.api_key,
            'X-Auth-Email': self.email,
        }

        response = requests.request(method, API_BASE_URL + url, headers=headers, **kwargs)
        response.raise_for_status()

        return response

def main():
    parser = ArgumentParser()
    parser.add_argument('--auth-api-key', default=os.environ.get('CF_API_KEY'))
    parser.add_argument('--auth-email', default=os.environ.get('CF_EMAIL'))
    parser.add_argument('-T', '--record-type', default='A')
    parser.add_argument('-t', '--ttl', default=120, type=int)
    parser.add_argument('zone')
    parser.add_argument('record')

    args = parser.parse_args()

    valid = True

    if not args.auth_api_key:
        print 'CloudFlare API key required; use --auth-api-key or CF_API_KEY'
        valid = False

    if not args.auth_email:
        print 'CloudFlare email required; use --auth-email or CF_EMAIL'
        valid = False

    if not valid:
        sys.exit(1)

    client = CloudFlare(args.auth_api_key, args.auth_email)

    zone = client.find_zone(name=args.zone)
    dns_record = client.find_dns_record(zone['id'], name=args.record, type=args.record_type)

    content = fetch_public_ip()

    if dns_record['content'] != content:
        dns_record['content'] = content
        dns_record['ttl'] = args.ttl
        client.update_dns_record(dns_record)

main()
