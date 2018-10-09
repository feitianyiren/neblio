#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import multiprocessing as mp
import neblio_ci_libs as nci

working_dir = os.getcwd()
build_dir = "wallet"

packages_to_install = \
[
"qt5-default",
"qt5-qmake",
"qtbase5-dev-tools",
"qttools5-dev-tools",
"build-essential",
"libboost-dev",
"libboost-system-dev",
"libboost-filesystem-dev",
"libboost-program-options-dev",
"libboost-thread-dev",
"libboost-regex-dev",
"libssl-dev",
"libdb++-dev",
"libminiupnpc-dev",
"libqrencode-dev",
"libcurl4-openssl-dev",
"libldap2-dev",
"libidn11-dev",
"librtmp-dev"
]

nci.install_packages_debian(packages_to_install)

os.chdir(build_dir)

nci.call_with_err_code('python $TRAVIS_BUILD_DIR/build_scripts/CompileOpenSSL-Linux.py')
nci.call_with_err_code('python $TRAVIS_BUILD_DIR/build_scripts/CompileCurl-Linux.py')

os.environ['PKG_CONFIG_PATH'] = os.path.join(working_dir, build_dir, 'curl_build/lib/pkgconfig/')
os.environ['OPENSSL_INCLUDE_PATH'] = os.path.join(working_dir, build_dir, 'openssl_build/include/')
os.environ['OPENSSL_LIB_PATH'] = os.path.join(working_dir, build_dir, 'openssl_build/lib/')

nci.call_with_err_code('make "STATIC=1" -B -w -f makefile.unix -j' + str(mp.cpu_count()))
nci.call_with_err_code('tar -zcvf "nebliod---ubuntu16.04---$(date +%Y-%m-%d).tar.gz" ./nebliod')
nci.call_with_err_code('echo "Binary package at $PWD nebliod---ubuntu16.04---$(date +%Y-%m-%d).tar.gz"')

print("")
print("")
print("Building finished successfully.")
print("")
