import sys
import os
sys.path.insert(0, '/var/www/html/medaccess')
os.environ['MEDACCESS_CONFIG'] = '/home/ubuntu/medaccess/settings.cfg'

from medaccess_app import app as application
