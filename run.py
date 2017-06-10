#!flask/bin/python

from app import app

import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
logger.info("Starting App")
app.run(debug=True)