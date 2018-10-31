from unittest import TestCase
import json
import responses
import requests

from cloudconnect.cloudconnect import CloudConnect
#from cloudflare.test_config import email, apikey

class TestCloudConnect(TestCase):
    def setUp(self):
        self.email = "example@example.org"
        self.apikey = "0a1b2c3d4e5f6g7h8i9j10k11l12m13n14o15"
        self.c = CloudConnect(self.email, self.apikey)
        self.expected_header = {'X-Auth-Email': self.email,
                       'X-Auth-Key': self.apikey,
                       'Content-Type': 'application/json'}
        self.api_endpoint = 'https://api.cloudflare.com/client/v4/test.com'

    def tearDown(self):
        pass

    def test_headers(self):
        """ Setup the headers for authentications """
        assert self.c.headers() == self.expected_header

    @responses.activate
    def test_parse_json(self):
        """Parse JSON, return dict. looking for errors """
        data = {'this':[{'is':'json'}, {'right':'?'}],'yup':'it is'}
        responses.add(responses.GET, 'http://exampleurl', body=json.dumps(data))
        response = requests.get('http://exampleurl')
        parsed = self.c.parse_json(response)
        assert parsed == data

    def test_url_kwargs(self):
        """
        Sets up the kwargs to be used in the page request. Returns a dict.
        Takes both request params and request data. Turns data into JSON
        url_kwargs(url, params=None, data=None)
         """
        data = {'a':'param','b':'param'}
        case_params = self.c.url_kwargs('test.com', params=data)
        case_data = self.c.url_kwargs('test.com', data=data)
        case_url_only = self.c.url_kwargs('test.com')

        assert case_params == {
            'url':self.api_endpoint,
            'headers': self.expected_header,
            'params':data}

        assert case_data == {
            'url':self.api_endpoint,
            'headers': self.expected_header,
            'data':json.dumps(data)}
        assert case_url_only == {
            'url':self.api_endpoint,
            'headers':self.expected_header}

    @responses.activate
    def test_post(self):
        """Post request that returns a dict from JSON via request.json().
        """
        data = {'data':'out'}
        in_data = {'test':'data'}
        j_data = json.dumps(data)

        responses.add(responses.POST,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=j_data)
        response = self.c.post('zones', in_data)
        assert response == data

    @responses.activate
    def test_get(self):
        """Get request that returns a dict from JSON via request.json()
        """
        data = {'data':'out'}
        in_data = {'test':'data'}
        j_data = json.dumps(data)
        responses.add(responses.GET,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=j_data)
        response = self.c.get('zones', in_data)
        assert response == data

    @responses.activate
    def test_put(self):
        """Put request that returns a dict from JSON via request.json()
        """
        data = {'data':'out'}
        in_data = {'test':'data'}
        j_data = json.dumps(data)
        responses.add(responses.PUT,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=j_data)
        response = self.c.put('zones', in_data)
        assert response == data
        return response

    @responses.activate
    def test_delete(self):
        """Delete request that returns a dict from JSON via request.json()
        """
        data = {'data':'out'}
        in_data = {'test':'data'}
        j_data = json.dumps(data)
        responses.add(responses.DELETE,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=j_data)
        response = self.c.delete('zones', in_data)
        assert response == data

    @responses.activate
    def test_get_zone_id(self):
        """ Query the API to return the ID for a specific domain """

        data = '{"result":[{"id":"ce2c6fb70e26bd3fe399de7e4894f0cf","name":"exampledomain.com","status":"active","paused":false,"type":"full","development_mode":0,"name_servers":["name1.ns.cloudflare.com","name2.ns.cloudflare.com"],"original_name_servers":["name1.NS.CLOUDFLARE.COM","name2.NS.CLOUDFLARE.COM"],"original_registrar":"","original_dnshost":null,"modified_on":"2015-06-10T17:40:40.353402Z","created_on":"2015-02-11T15:34:21.499024Z","meta":{"step":4,"wildcard_proxiable":false,"custom_certificate_quota":0,"page_rule_quota":"3","phishing_detected":false,"multiple_railguns_allowed":false},"owner":{"type":"user","id":"2ec31053ae9e211bc0550302c7dae136","email":"person@example.com"},"permissions":["#analytics:read","#billing:edit","#billing:read","#cache_purge:edit","#dns_records:edit","#dns_records:read","#organization:edit","#organization:read","#ssl:edit","#ssl:read","#waf:edit","#waf:read","#zone:edit","#zone:read","#zone_settings:edit","#zone_settings:read"],"plan":{"id":"0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee","name":"Free Website","price":0,"currency":"USD","frequency":"","legacy_id":"free","is_subscribed":true,"can_subscribe":true,"externally_managed":false}}],"result_info":{"page":1,"per_page":20,"total_pages":1,"count":1,"total_count":1},"success":true,"errors":[],"messages":[]}'
        responses.add(responses.GET,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=data)
        request = self.c.get_zone_id('example.com')
        assert request == 'ce2c6fb70e26bd3fe399de7e4894f0cf'

    @responses.activate
    def test_create_zone(self):
        data = '{"result":{"id":"ce2c6fb70e26bd3fe399de7e4894f0cf","name":"example.com","status":"pending","paused":false,"type":"full","development_mode":0,"name_servers":["name1.ns.cloudflare.com","name2.ns.cloudflare.com"],"original_name_servers":["name1.NS.CLOUDFLARE.COM","name2.NS.CLOUDFLARE.COM"],"original_registrar":null,"original_dnshost":null,"modified_on":"2015-06-12T21:31:41.120524Z","created_on":"2015-06-12T21:31:41.095186Z","meta":{"step":4,"wildcard_proxiable":false,"custom_certificate_quota":0,"page_rule_quota":"3","phishing_detected":false,"multiple_railguns_allowed":false},"owner":{"type":"user","id":"2ec31053ae9e211bc0550302c7dae136","email":"person@example.com"},"permissions":["#analytics:read","#billing:edit","#billing:read","#cache_purge:edit","#dns_records:edit","#dns_records:read","#organization:edit","#organization:read","#ssl:edit","#ssl:read","#waf:edit","#waf:read","#zone:edit","#zone:read","#zone_settings:edit","#zone_settings:read"],"plan":{"id":"0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee","name":"Free Website","price":0,"currency":"USD","frequency":"","legacy_id":"free","is_subscribed":true,"can_subscribe":true,"externally_managed":false}},"success":true,"errors":[],"messages":[]}'
        responses.add(responses.POST,
                     'https://api.cloudflare.com/client/v4/zones',
                     body=data)
        create = self.c.create_zone('example.com')
        assert create == json.loads(data)
