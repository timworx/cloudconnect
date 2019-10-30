# CloudConnect

## DEPRECATED
> Use the [official Python wrapper](https://github.com/cloudflare/python-cloudflare) provided by Cloudflare.
> This was built when v4 of the API was very fresh and the official wrapper had not existed yet.
> 
---


[![Build Status](https://travis-ci.org/timworx/cloudconnect.svg?branch=master)](https://travis-ci.org/timworx/cloudconnect)

CloudConnect is a simple pure python interface for v4 of the [CloudFlare API](https://api.cloudflare.com/).

At the moment it mostly provides a thin wrapper around CloudFlare API connections. Each wrapped call returns the JSON data as a python dict.  

Over time it will also include commands that complement and extend the current CF API's capabilities.  
A current example is listing DNS records based on domain name, rather than just by ID.

## Python Versions Supported

- [x] Python 2.7  
- [x] Python 3.5+

## Under Development

This project is currently under development. Pull requests and suggested code improvements are welcome. 

## Install

```bash
$ git clone https://github.com/timworx/cloudconnect.git
$ python setup.py install
```

Or via pip with:

```bash
$ pip install git+git://github.com/timworx/cloudconnect.git
```

## Usage

Calls to the CloudFlare API with CloudConnect will return a dict of the JSON data returned (unless otherwise noted).


**Initializing** `CloudConnect`

```python
>>> from cloudconnect import CloudConnect
>>> cf = CloudConnect('email@example.com', 'd2gYOURoAPIoKEYo24fmdsf')
```

**Create a new zone (add a domain)** with `create_zone` and skip the automagic record grabbing by CloudFlare.

```python
>>> from cloudconnect import CloudConnect
>>> cf = CloudConnect('email@example.com', 'd2gYOURoAPIoKEYo24fmdsf')
>>> cf.create_zone('mydomain.com', jump_start=False)
{u'errors': [],
 u'messages': [],
 u'result': {u'status': u'pending',
             u'original_name_servers': [u'ns1.com', u'ns2.com'],
             u'original_dnshost': None,
             u'name': u'anotherdomain.com',
             u'owner': {u'type': u'user', 
                        u'id': u'd2gYOURoAPIoKEYo24fmdsf', 
                        u'email': u'tim@dualmediasolutions.com'},
             u'original_registrar': None,
             u'paused': False, 
             u'modified_on': u'2015-06-17T21:37:45.967464Z',
             u'created_on': u'2015-06-17T21:37:45.930702Z',
  ...
```

**A Note About** `**kwargs`

You can use `**kwargs` to pass arguments/parameters that are not required by Cloudflare. For example, notice how `jump_start=False` is passed above.

### Current Queries 

#### Initialize CloudConnect
`cf = Cloudconnect('email@example.com', 'd2gYOURoAPIoKEYo24fmdsf')`


#### Create a Zone (Add a domain)
`cf.create_zone(domain, **kwargs)`

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
