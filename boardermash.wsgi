activate_this = '/var/www/postmash/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
print sys.path
from boardermash import app as application
