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

    def patch(self, url, data=None):
        """ Patch request that returns JSON. Takes data as dict """
        r = requests.patch(**self.url_kwargs(url, data=data))
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

    def list_zones(self, **kwargs):
        """ List, search, sort, and filter all zones (domains) """
        return self.get('zones', kwargs)

    def zone_details(self, zone_id):
        """ Get zone details. """
        return self.get('zones/{}'.format(zone_id))

    def edit_zone_properties(self, zone_id, **kwargs):
        """ Edit zone properties. Only one can be changed at a time. """
        return self.patch('zones/{}'.format(zone_id), kwargs)

    def delete_zone(self, zone_id):
        """ Delete an existing zone. Plans & subscriptions must be cancelled"""
        return self.delete('zones/{}'.format(zone_id))

    def purge_cache(self, zone_id, **kwargs):
        """ Basic purge cache command to remove files from cloudflare """
        return self.delete('zones/{}'.format(zone_id), kwargs)

    def purge_all_files(self, zone_id):
        """ Remove ALL files from CloudFlare's cache """
        return self.purge_cache(zone_id, purge_everything=True)

    def purge_individual_files(self, zone_id, files):
        if not isinstance(files, list):
            files = [files]
        return self.purge_cache(zone_id, files=files)

    def create_dns_record(self, zone_id, r_type, name, content, **kwargs):
        """ Create a DNS Record """
        url = 'zones/{}/dns_records'.format(zone_id)
        data = {'type':r_type, 'name':name, 'content':content}
        if kwargs:
            data.update(kwargs)
        return self.post(url, data)

    def list_dns_records(self, zone_id, **kwargs):
        """ List DNS Record from zone ID """
        url = 'zones/{}/dns_records'.format(zone_id)
        return self.get(url, kwargs)

    def dns_record_details(self, zone_id, rec_id):
        """ Get the details of a DNS records by ID """
        url = 'zones/{}/dns_records/{}'.format(zone_id, rec_id)
        return self.get(url)

    def update_dns_record(self, zone_id, rec_id, **kwargs):
        """ Update a DNS Record """
        url = 'zones/{}/dns_records/{}'.format(zone_id, rec_id)
        return self.put(url, kwargs)

    def domain_list_dns_records(self, domain, **kwargs):
        """ List DNS records from domain """
        z_id = self.get_zone_id(domain)
        return self.list_dns_records(z_id, **kwargs)

    def delete_dns_record(self, zone_id, rec_id):
        """ Delete a DNS record, using zone (domain) id and record id """
        return self.delete('zones/{}/dns_records/{}'.format(zone_id, rec_id))
