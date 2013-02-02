import os
from ..parse import parse
from nose import with_setup
from nose.tools import raises, eq_


def setup_env():
    os.environ['PARSE_APPLICATION_ID'] = 'foo'
    os.environ['PARSE_REST_API_KEY'] = 'bar'


def teardown_env():
    os.environ.clear()

# ParseClient constructor tests


@with_setup(setup_env, teardown_env)
def test_can_init_ParseClient_from_env_variables():

    p = parse.ParseClient()

    eq_(p.rest_client.headers['X-Parse-Application-Id'], 'foo')
    eq_(p.rest_client.headers['X-Parse-REST-API-Key'], 'bar')


def test_can_init_parse_client_with_args():

    p = parse.ParseClient('foo', 'bar')

    eq_(p.rest_client.headers['X-Parse-Application-Id'], 'foo')
    eq_(p.rest_client.headers['X-Parse-REST-API-Key'], 'bar')


@raises(ValueError)
def test_value_error_when_init_ParseClient_without_args_or_env():
    parse.ParseClient()
