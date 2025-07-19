#!/usr/bin/env python3
"""
HTTPS development server for Safari compatibility
"""
import ssl
from app import app

if __name__ == '__main__':
    # Create a simple SSL context for development
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem') if False else None  # We'll use adhoc for now
    
    # Run with adhoc SSL context (self-signed certificate)
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True,
        ssl_context='adhoc'  # Creates temporary self-signed certificate
    )