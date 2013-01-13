import requests
import simplejson as json
import os
from .exceptions import raises_parse_error

PARSE_URL = 'https://api.parse.com/1'


def _set_parse_credential_from_env():

    application_id = os.environ.get('PARSE_APPLICATION_ID')
    rest_api_key = os.environ.get('PARSE_REST_API_KEY')

    if not application_id or not rest_api_key:
        raise ValueError(
            """Calling ParseClient() with no arguments requires environment
            variables to be set like this:

            >>> import os
            >>> os.environ['PARSE_APPLICATION_ID'] = YOUR_PARSE_APPLICATION_ID
            >>> os.environ['PARSE_REST_API_KEY'] = YOUR_PARSE_REST_API_KEY
            """
        )
    return application_id, rest_api_key


class ParseClient(object):
    """A wrapper for interacting with the Parse API

    This class holds the credentials of your Parse account.

    Args:
        application_id: Your Parse Application ID
        rest_api_key: Your Parse API Key

    Attributes:
        rest_client: a requests object with the necessary Parse credentials
        url: the base url to use for API requests
    """

    def __init__(self, application_id=None, rest_api_key=None):

        if not application_id or not rest_api_key:
            application_id, rest_api_key = _set_parse_credential_from_env()

        headers = {'X-Parse-Application-Id': application_id,
                   'X-Parse-REST-API-Key': rest_api_key}

        self.rest_client = requests.session()
        self.rest_client.headers = headers
        self.url = PARSE_URL

    @raises_parse_error
    def create_object(self, object_class, object_attributes):
        url = self._generate_parse_url(object_class)
        headers = {'content-type': 'application/json'}
        response = self.rest_client.post(url, headers=headers,
                                         data=json.dumps(object_attributes))
        return response.json()

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
        return response.json()

    @raises_parse_error
    def delete_object(self, object_class, object_id, auth=None):
        url = self._generate_parse_url(object_class, object_id)
        headers = {}
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
        return response.json()

    @raises_parse_error
    def query_object_class(self, object_class, constraints,
                           order='',
                           include=None,
                           count=False,
                           first_result_only=False):

        url = self._generate_parse_url(object_class)

        order = '' if not order else ','.join(order)

        params = {'where': json.dumps(constraints), 'order': order}
        params['include'] = '' if not include else ','.join(include)

        if count:
            params['count'] = 1
            params['limit'] = 0

        response = self.rest_client.get(url, params=params)

        if count:
            return response.json()['count']
        if response.json()['results']:
            if first_result_only:
                return response.json()['results'][0]
            else:
                return response.json()['results']
        else:
            return None

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
