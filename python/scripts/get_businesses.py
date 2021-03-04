#!/usr/bin/env python
from os.path import dirname, abspath, join
import sys

sys.path.append(abspath(join(dirname(__file__), '..', 'src')))

from api_config import ApiConfig
from access_token import AccessToken
from oauth_scope import Scope
from user import User

# get configuration from defaults and/or the environment
api_config = ApiConfig()

# Note that the OAuth will fail if your application does not
# have access to the scope that is required to access
# linked business accounts.
access_token = AccessToken(api_config, scopes=[Scope.READ_USERS,Scope.READ_ADVERTISERS])

# use the access token to get information about the user
user_me = User('me', api_config, access_token)
user_me_data = user_me.get()
user_me.print_summary(user_me_data)

print('trying /v3/users/me/businesses...')
user_me_businesses = user_me.get_businesses()
if user_me_businesses:
    print(user_me_businesses)
else:
    print('This account has no information on linked businesses.')