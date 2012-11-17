import requests
import simplejson as json
from settings import PARSE_APPLICATION_ID, PARSE_REST_API_KEY


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
        headers = {'X-Parse-Application-Id': PARSE_APPLICATION_ID,
                   'X-Parse-REST-API-Key': PARSE_REST_API_KEY}
        self.rest_client = requests.session(headers=headers)
        self.url = 'https://api.parse.com/1'

    def create_object(self, object_class, object_attributes):
        url = self._generate_parse_url(object_class)
        headers = {'content-type': 'application/json'}
        response = self.rest_client.post(url, headers=headers,
                                         data=json.dumps(object_attributes))
        return response.json

    def get_object(self, object_class, object_id):
        url = self._generate_parse_url(object_class, object_id)
        response = self.rest_client.get(url)
        return response.json

    def delete_object(self, object_class, object_id):
        url = self._generate_parse_url(object_class, object_id)
        response = self.rest_client.delete(url)
        deletion_result = (response.status_code == requests.codes.ok)
        return deletion_result

    def update_object(self, object_class, object_id, object_attributes):
        url = self._generate_parse_url(object_class, object_id)
        response = self.rest_client.put(url,
                                        data=json.dumps(object_attributes))
        return response.json

    def query_object_class(self, object_class, constraints,
                           first_result_only=False):
        url = self._generate_parse_url(object_class)
        params = {'where': json.dumps(constraints)}
        response = self.rest_client.get(url, params=params)
        if not response.json['results']:
            return None
        elif first_result_only:
            return response.json['results'][0]
        else:
            return response.json['results']

    def _generate_parse_url(self, object_class, object_id=None,):
        if object_class is 'users':
            resource_alias = '/'
        else:
            resource_alias = '/classes'
        if object_id:
            url = '%s%s/%s/%s' % (self.url, resource_alias,
                                  object_class, object_id)
        else:
            url = '%s%s/%s' % (self.url, resource_alias,
                               object_class)
        return url
