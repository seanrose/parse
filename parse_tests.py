import unittest
import os
from parse import ParseClient


class ParseTests(unittest.TestCase):

    def testCanInitParseClientFromEnvVariables(self):

        os.environ['PARSE_APPLICATION_ID'] = 'foo'
        os.environ['PARSE_REST_API_KEY'] = 'bar'

        p = ParseClient()

        self.failUnless(
            p.rest_client.headers['X-Parse-Application-Id'] == 'foo'
        )
        self.failUnless(
            p.rest_client.headers['X-Parse-REST-API-Key'] == 'bar'
        )

    def testCanInitParseClientWithArgs(self):

        p = ParseClient('foo', 'bar')

        self.failUnless(
            p.rest_client.headers['X-Parse-Application-Id'] == 'foo'
        )
        self.failUnless(
            p.rest_client.headers['X-Parse-REST-API-Key'] == 'bar'
        )


def main():
    unittest.main()

if __name__ == '__main__':
    main()
