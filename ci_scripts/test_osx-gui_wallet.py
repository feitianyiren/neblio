#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import multiprocessing as mp
import neblio_ci_libs as nci

working_dir = os.getcwd()
build_dir = "build"

parser = argparse.ArgumentParser()
parser.add_argument('--test', '-t', help='Only build and run tests', action='store_true')
args = parser.parse_args()

nci.mkdir_p(build_dir)
os.chdir(build_dir)

nci.call_with_err_code('brew update')

nci.call_with_err_code('brew fetch --retry qt            && brew install qt --force')
nci.call_with_err_code('brew fetch --retry berkeley-db@4 && brew install berkeley-db@4 --force')
nci.call_with_err_code('brew fetch --retry boost@1.60    && brew install boost@1.60 --force')
nci.call_with_err_code('brew fetch --retry miniupnpc     && brew install miniupnpc --force')
nci.call_with_err_code('brew fetch --retry curl          && brew install curl --force')
nci.call_with_err_code('brew fetch --retry openssl       && brew install openssl --force')
nci.call_with_err_code('brew fetch --retry qrencode      && brew install qrencode --force')

nci.call_with_err_code('brew unlink qt            && brew link --force --overwrite qt')
nci.call_with_err_code('brew unlink berkeley-db@4 && brew link --force --overwrite berkeley-db@4')
nci.call_with_err_code('brew unlink boost@1.60    && brew link --force --overwrite boost@1.60')
nci.call_with_err_code('brew unlink miniupnpc     && brew link --force --overwrite miniupnpc')
nci.call_with_err_code('brew unlink curl          && brew link --force --overwrite curl')
nci.call_with_err_code('brew unlink python        && brew link --force --overwrite python')
nci.call_with_err_code('brew unlink openssl       && brew link --force --overwrite openssl')
nci.call_with_err_code('brew unlink qrencode      && brew link --force --overwrite qrencode')


if (args.test):
	nci.call_with_err_code('qmake "USE_UPNP=1" "USE_QRCODE=1" "RELEASE=1" "NEBLIO_CONFIG += NoWallet" ../neblio-wallet.pro')
	nci.call_with_err_code("make -j" + str(mp.cpu_count()))
	# run tests
	nci.call_with_err_code("./wallet/test/neblio-Qt.app/Contents/MacOS/neblio-Qt")
else:
	nci.call_with_err_code('qmake "USE_UPNP=1" "USE_QRCODE=1" "RELEASE=1" ../neblio-wallet.pro')
	nci.call_with_err_code("make -j" + str(mp.cpu_count()))
	# build our .dmg
	nci.call_with_err_code('sudo easy_install appscript')
	nci.call_with_err_code('../contrib/macdeploy/macdeployqtplus ./wallet/neblio-Qt.app -add-qt-tr da,de,es,hu,ru,uk,zh_CN,zh_TW -dmg -verbose 1 -rpath /usr/local/opt/qt/lib')
	nci.call_with_err_code('zip -j neblio-Qt---macOS---$(date +%Y-%m-%d).zip ./neblio-QT.dmg')
	nci.call_with_err_code('echo "Binary package at $PWD neblio-Qt---macOS---$(date +%Y-%m-%d).zip"')


print("")
print("")
print("Building finished successfully.")
print("")
