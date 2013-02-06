import os
from ..parse import parse
from nose import with_setup
from nose.tools import ok_
from test_object_schema import TEST_CLASS_NAME


def dummy_env_setup():
    os.environ['PARSE_REST_API_KEY'] = os.environ.get('PARSE_TEST_KEY')
    os.environ['PARSE_APPLICATION_ID'] = os.environ.get('PARSE_TEST_ID')


# Create an object
@with_setup(dummy_env_setup)
# @timed(1)
def test_create_object():

    p = parse.ParseClient()

    obj = p.create_object(TEST_CLASS_NAME)

    ok_(obj, 'Object was not successfully created')


# Get an object
@with_setup(dummy_env_setup)
# @timed(1)
def test_get_object():

    p = parse.ParseClient()

    obj = p.query_object_class(TEST_CLASS_NAME, {}, first_result_only=True)

    p.get_object(TEST_CLASS_NAME, obj['objectId'])

    ok_(obj, 'Object was not successfully gotten')


# Update the object
@with_setup(dummy_env_setup)
# @timed(1)
def test_update_object():

    p = parse.ParseClient()

    obj = p.query_object_class(TEST_CLASS_NAME, {}, first_result_only=True)

    updated_at = p.update_object(TEST_CLASS_NAME, obj['objectId'],
                                 {'foo': 'bar'})

    ok_(updated_at, 'Object was not successfully updated')


# Delete the object
@with_setup(dummy_env_setup)
# @timed(1)
def test_delete_object():

    p = parse.ParseClient()

    obj = p.query_object_class(TEST_CLASS_NAME, {}, first_result_only=True)

    ok_(p.delete_object(TEST_CLASS_NAME, obj['objectId']),
        'Object was not successfully deleted')
