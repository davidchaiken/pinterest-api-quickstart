import mock

from integration_mocks import IntegrationMocks

class GetBusinessesTest(IntegrationMocks):
    def mock_requests_put(self, uri, headers=None, data=None):
        print('mock_requests_put', uri, headers, data)
        self.requests_put_calls += 1
        response = mock.MagicMock()
        response.__str__.return_value = '<Response [200]>'
        response.json.return_value = {'status': 'test-status',
                                      'scope': 'test-scope',
                                      # response needs to be different each time
                                      'access_token': 'test-access-token-' + str(self.requests_put_calls),
                                      'data': {'refresh_token': 'test-refresh-token'}
                                      }
        return response

    def mock_requests_get(self, uri, headers=None, data=None):
        print('mock_requests_get', uri, headers, data)
        response = mock.MagicMock()
        response.__str__.return_value = '<Response [200]>'
        if (uri == 'https://api.pinterest.com/v3/users/me/'):
            self.requests_get_users_me_calls += 1
            response.json.return_value = {'data':
                                          {'full_name': 'test fullname',
                                           'about': 'test about',
                                           'profile_url': 'test profile url',
                                           'pin_count': 'pin count'
                                           }
                                          }
        elif (uri == 'https://api.pinterest.com/v3/users/me/businesses/'):
            self.requests_get_users_me_businesses_calls += 1
            response.json.return_value = {'data':
                                          {'full_name': 'test business name',
                                           'id': 'test-business-id-number'
                                           }
                                          }
        return response

    def test_get_access_token(self):
        from scripts.get_businesses import main # import here to see monkeypatches

        self.requests_put_calls = 0
        self.requests_get_users_me_calls = 0
        self.requests_get_users_me_businesses_calls = 0

        with self.mock_redirect():
            main() # run get_businesses

        self.assertEqual(self.requests_put_calls, 1)
        self.assertEqual(self.requests_get_users_me_calls, 1)
        self.assertEqual(self.requests_get_users_me_businesses_calls, 1)