# CloudConnect

CloudConnect is a simple pure python interface for v4 of the [CloudFlare API](https://api.cloudflare.com/).

At the moment it mostly provides a thin wrapper around CloudFlare API connections. Each wrapped call returns the JSON data as a python dict.  Over time it will also include commands that complement and extend the current API's capabilities.  
An example would be getting record data based on domain name, rather than just by ID as is required currently.

## Under Development

This project is currently underdevelopment. Pull requests and suggested code improvements are welcome. 

## Install

```bash
$ git clone https://github.com/timworx/cloudconnect.git
$ python setup.py install
```

## Usage

Calls to the CloudFlare API with CloudConnect will return a dict of the JSON data returned (unless otherwise noted).


**Initializing** `CloudConnect`

```python
>>> from cloudconnect import CloudConnect
>>> cf = Cloudconnect('email@example.com', 'd2gYOURoAPIoKEYo24fmdsf')
```

**Create a new zone (add a domain)** with `create_zone` and skip the automagic record grabbing by CloudFlare.

```python
>>> cf.create_zone('mydomain.com', jump_start=False)
{u'errors': [], u'messages': [], u'result': {u'status': u'pending', u'original_name_servers': [u'ns1.com', u'ns2.com'], u'original_dnshost': None, u'name': u'anotherdomain.com', u'owner': {u'type': u'user', u'id': u'd2gYOURoAPIoKEYo24fmdsf', u'email': u'tim@dualmediasolutions.com'}, u'original_registrar': None, u'paused': False, u'modified_on': u'2015-06-17T21:37:45.967464Z', u'created_on': u'2015-06-17T21:37:45.930702Z', u'meta': {u'page_rule_quota': u'3', u'wildcard_proxiable': False, u'step': 4, u'phishing_detected': False, u'multiple_railguns_allowed': False, u'custom_certificate_quota': 0}, u'plan': {u'externally_managed': False, u'name': u'Free Website', u'price': 0, u'can_subscribe': True, u'currency': u'USD', u'frequency': u'', u'legacy_id': u'free', u'id': u'0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee', u'is_subscribed': True}, u'name_servers': [u'eric.ns.cloudflare.com', u'gina.ns.cloudflare.com'], u'development_mode': 0, u'type': u'full', u'id': u'd2gYOURoAPIoKEYo24fmdsf', u'permissions': [u'#analytics:read', u'#billing:edit', u'#billing:read', u'#cache_purge:edit', u'#dns_records:edit', u'#dns_records:read', u'#organization:edit', u'#organization:read', u'#ssl:edit', u'#ssl:read', u'#waf:edit', u'#waf:read', u'#zone:edit', u'#zone:read', u'#zone_settings:edit', u'#zone_settings:read']}, u'success': True}
```

**A Note About** `**kwargs`

You can pass `**kwargs` for API call arguments/parameters that are not required by cloudflare for each call. They are passed as a part of either `data=` or `params=` as appropriate.

### Current Queries 

#### Initialize CloudConnect
`cf = Cloudconnect('email@example.com', 'd2gYOURoAPIoKEYo24fmdsf')`


#### Create a Zone (Add a domain)
`cf.create_zone(domain, **kwargs)

#### Get zone_id
`cf.get_zone_id(domain)`

#### Create a DNS Record
`cf.create_dns_record(zone_id, r_type, name, content, **kwargs)`

#### Update DNS Records
`cf.update_dns_record(zone_id, rec_id, **kwargs)`

#### List DNS Records
`cf.list_dns_records(zone_id, **kwargs)`

#### Delete DNS Record
`cf.delete_dns_record(zone_id, rec_id)`

### Commands that improve, augment, or compliment CF API commands

#### List DNS Records for Domain (rather than by Zone ID)
`cf.domain_list_dns_records(domain, **kwargs)`

## Subclassing CloudConnect

you can subclass CloudConnect to create another layer of project specific abstraction for API calls.

For example, let's say that you had two records to apply to your domains, both proxied by CloudFlare.

```python
>>> from cloudconnect import CloudConnect
>>> class MyCloudConnect(CloudConnect):
>>>     def set_the_records(self, domain):
>>>         zone_id = self.get_zone_id(domain)
>>>         rec1 = self.create_dns_record(zone_id, 'A', '@', '127.0.0.1', proxied=True)
>>>         rec2 = self.create_dns_record(zone_id, 'CNAME', 'www', 'mydomain.com', proxied=True)
>>>         return rec1, rec2
```
