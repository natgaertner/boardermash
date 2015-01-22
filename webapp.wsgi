activate_this = '/var/www/boardermash_home/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
print sys.path
from webapp_closed import app as application
