#!/usr/bin/env bash
# Used because Chrome now requires SSL certs to have Subject Alternatic Name set,
# and as of 2018-08-23 the cert on ios-xe-mgmt.cisco.com does not have such
# Hence we need Postman to connect via this socat tunnel, which will do the SSL with unverified cert
echo 'Forwarding http://127.0.0.1:9443 -> https://ios-xe-mgmt.cisco.com:9443'
socat TCP-LISTEN:9443,fork,reuseaddr,bind=127.0.0.1 OPENSSL:ios-xe-mgmt.cisco.com:9443,verify=0
