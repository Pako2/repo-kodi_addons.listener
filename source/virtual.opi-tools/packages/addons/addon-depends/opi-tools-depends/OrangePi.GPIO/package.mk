# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)

PKG_NAME="OrangePi.GPIO"
PKG_ARCH="arm"
PKG_LICENSE="MIT"
PKG_VERSION="0.6.6"
PKG_SHA256="f2b9e6e149b897fac1b4609fe0029c95af24f02459e9b1e08b7cb3412131d1d4"
PKG_SITE="https://github.com/Pako2/OrangePi.GPIO"
PKG_URL="https://github.com/Pako2/OrangePi.GPIO/archive/refs/tags/v${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain Python3 distutilscross:host"
PKG_LONGDESC="A module to control Orange Pi GPIO channels."
PKG_TOOLCHAIN="manual"

pre_configure_target() {
  export PYTHONXCPREFIX="$SYSROOT_PREFIX/usr"
  export LDSHARED="$CC -shared"
  export CFLAGS="$CFLAGS -fcommon"
  export CPPFLAGS="$TARGET_CPPFLAGS -I${SYSROOT_PREFIX}/usr/include/$PKG_PYTHON_VERSION"
}

PKG_OPI_VERSION=""
if [ "$DEVICE" = "H6" ]; then
  PKG_OPI_VERSION="--force-h6"
fi

make_target() {
  python3 setup.py build $PKG_OPI_VERSION
}
