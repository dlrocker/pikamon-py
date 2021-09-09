import sys
import os

# Append the "helpers" python files for our tests to the python path so they are discoverable
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

# Add all fixtures for our tests so they are discoverable
pytest_plugins = [
    'fixtures.database_fixtures'
]
