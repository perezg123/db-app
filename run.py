import os
import OpenSSL 
import ssl

from app import create_app
from OpenSSL import SSL

# config_name = os.getenv('FLASK_CONFIG')
config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
#    context = ssl.SSLContext()
#    context.load_cert_chain('./ssl/cert1.pem', './ssl/provkey1.pem')
#    This is the py 2.7 method context = ('./ssl/cert1.pem', './ssl/privkey1.pem')
#    app.run(ssl_context=context, threaded=True, debug=True)
    app.run()

