# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)

PKG_NAME="evdev"
PKG_ARCH="arm"
PKG_VERSION="1.4.0"
PKG_SHA256="979638719b205acdead3ea3f7861d7b19427a8dc6147c660c24c58e79f0bb427"
PKG_LICENSE="Revised BSD License"
PKG_SITE="https://github.com/Pako2/python-evdev/"
PKG_URL="https://github.com/Pako2/python-evdev/archive/refs/tags/v${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain Python3 distutilscross:host"
PKG_LONGDESC="Allows to read and write input events."
PKG_TOOLCHAIN="manual"


pre_configure_target() {
  export PYTHONXCPREFIX="$SYSROOT_PREFIX/usr"
  export LDSHARED="$CC -shared"
  export CFLAGS="$CFLAGS -fcommon"
  export CPPFLAGS="$TARGET_CPPFLAGS -I${SYSROOT_PREFIX}/usr/include/$PKG_PYTHON_VERSION"
}


make_target() {
  python3 setup.py build
}
