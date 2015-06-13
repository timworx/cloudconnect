""" Cloudflare API wrapper in Python """
import requests
import json

class CloudConnect:
    """ Initialize with your email and apikey"""
    def __init__(self, email, apikey):
        self.email = email
        self.apikey = apikey
        self. auth = self.email, self.apikey
        self.api = 'https://api.cloudflare.com/client/v4/'

    class APIError(Exception):
        """ Exception Subclass for handling Api Errors
        """
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return self.value

    def headers(self):
        """
        Setup the headers for authentications
        """
        return {'X-Auth-Email':self.email,
                'X-Auth-Key':self.apikey,
                'Content-Type': 'application/json'}

    def parse_json(self, request):
        """ Parse request JSON for, looking for errors """
        try:
            return  request.json()
        except ValueError:
            raise self.APIError('parse_json failed.')

    def url_kwargs(self, url, params=None, data=None):
        """
        Sets up the kwargs to be used in the page request. Returns a dict
        Takes both request params and request data. Turns data into JSON
         """
        kwarg_dict = {'url':self.api+url, 'headers':self.headers()}
        if params:
            try:
                params.keys()
            except AttributeError:
                raise self.APIError('Pycf url_kwargs "params" must be a dict')
            else:
                kwarg_dict['params'] = params
        if data:
            try:
                data.keys()
            except AttributeError:
                raise self.APIError('Pycf url_kwargs "data" must be a dict')
            else:
                kwarg_dict['data'] = json.dumps(data)
        return kwarg_dict

    def post(self, url, data=None):
        """Post request that returns JSON. Takes data as a dict """
        r = requests.post(**self.url_kwargs(url, data=data))
        return self.parse_json(r)

    def get(self, url, params=None):
        """Get request that returns JSON. Takes params as a dict """
        r = requests.get(**self.url_kwargs(url, params=params))
        return self.parse_json(r)

    def put(self, url, data=None):
        """Put request that returns JSON. Takes data as a dict """
        r = requests.put(**self.url_kwargs(url, data=data))
        return self.parse_json(r)

    def delete(self, url, data=None):
        """Delete request that return JSON. Takes data as a dict """
        r = requests.delete(**self.url_kwargs(url, data=data))
        return self.parse_json(r)

    def get_zone_id(self, domain):
        """ Find the ID for a specific domain """
        data = self.get('zones', {'name':domain})
        if data['result']:
            return data['result'][0]['id']
        else:
            return None

    def create_zone(self, domain, **kwargs):
        """ AKA add a domain to cloudflare """
        data = {'name':domain}
        if kwargs:
            data.update(kwargs)
        return self.post('zones', data)

    def create_dns_record(self, zone_id, r_type, name, content, **kwargs):
        """ Create a DNS Record """
        url = 'zones/{}/dns_records'.format(zone_id)
        data = {'type':r_type, 'name':name, 'content':content}
        if kwargs:
            data.update(kwargs)
        return self.post(url, data)

    def update_dns_record(self, zone_id, rec_id, **kwargs):
        """ Update a DNS Record """
        url = 'zones/{}/dns_records/{}'.format(zone_id, rec_id)
        return self.put(url, kwargs)

    def list_dns_records(self, zone_id, **kwargs):
        """ List DNS Record from zone ID """
        url = 'zones/{}/dns_records'.format(zone_id)
        return self.get(url, kwargs)

    def domain_list_dns_records(self, domain, **kwargs):
        """ List DNS records from domain """
        z_id = self.get_zone_id(domain)
        return self.list_dns_records(z_id, **kwargs)

    def delete_dns_record(self, zone_id, rec_id):
        """ Delete a DNS record, using zone (domain) id and record id """
        return self.delete('zones/{}/dns_records/{}'.format(zone_id, rec_id))
