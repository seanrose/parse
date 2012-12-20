import requests
import simplejson as json
import settings as s
from functools import wraps


class ParseException(Exception):
        pass


class ParseClient(object):
    """A wrapper for interacting with the Parse API

    This class handles interacting with Parse. It handles
    all of the HTTP requests and can create, retrieve, delete,
    update, and search for objects.
    objects.


    Attributes:
        rest_client: a requests object with the necessary Parse credentials
        url: the base url to use for API requests
    """

    def __init__(self):
        headers = {'X-Parse-Application-Id': s.PARSE_APPLICATION_ID,
                   'X-Parse-REST-API-Key': s.PARSE_REST_API_KEY}
        self.rest_client = requests.session(headers=headers)
        self.url = s.PARSE_URL

    def raises_parse_error(func):
        @wraps(func)
        def checked_for_parse_error(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is not None and 'error' in result:
                raise ParseException(result)
            else:
                return result
        return checked_for_parse_error

    @raises_parse_error
    def create_object(self, object_class, object_attributes):
        url = self._generate_parse_url(object_class)
        headers = {'content-type': 'application/json'}
        response = self.rest_client.post(url, headers=headers,
                                         data=json.dumps(object_attributes))
        return response.json

    @raises_parse_error
    def get_object(self, object_class, object_id, include=None,
                   login_credentials=None):
        url = self._generate_parse_url(object_class, object_id)
        params = {}
        if login_credentials is not None:
            params = login_credentials
        if include is not None:
            params['include'] = ','.join(include)
        response = self.rest_client.get(url, params=params)
        return response.json

    @raises_parse_error
    def delete_object(self, object_class, object_id, auth=None):
        url = self._generate_parse_url(object_class, object_id)
        headers = ''
        if auth is not None:
            headers = {'X-Parse-Session-Token': auth}
        response = self.rest_client.delete(url, headers=headers)
        deletion_result = (response.status_code == requests.codes.ok)
        return deletion_result

    @raises_parse_error
    def update_object(self, object_class, object_id, object_attributes):
        url = self._generate_parse_url(object_class, object_id)
        headers = {'content-type': 'application/json'}
        response = self.rest_client.put(url,
                                        headers=headers,
                                        data=json.dumps(object_attributes))
        return response.json

    @raises_parse_error
    def query_object_class(self, object_class, constraints,
                           order='',
                           include=None,
                           first_result_only=False):
        order = ','.join(order)
        url = self._generate_parse_url(object_class)
        params = {'where': json.dumps(constraints), 'order': order}
        if include is not None:
            params['include'] = ','.join(include)
        response = self.rest_client.get(url, params=params)
        if first_result_only and response.json['results']:
            return response.json['results'][0]
        else:
            return response.json

    def _generate_parse_url(self, object_class, object_id=None,):
        if object_class is 'users' or object_class is 'login':
            resource_alias = ''
        else:
            resource_alias = '/classes'
        if object_id:
            url = '%s%s/%s/%s' % (self.url, resource_alias,
                                  object_class, object_id)
        else:
            url = '%s%s/%s' % (self.url, resource_alias,
                               object_class)
        return url
