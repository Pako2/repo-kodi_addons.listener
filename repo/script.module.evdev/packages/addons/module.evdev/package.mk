# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)

PKG_NAME="module.evdev"
PKG_VERSION="1.0"
PKG_REV="001"
PKG_ARCH="any"
PKG_LICENSE="Revised BSD License"
PKG_SITE="https://libreelec.tv"
PKG_URL=""
PKG_DEPENDS_TARGET="toolchain evdev"
PKG_SECTION="script"
PKG_SHORTDESC="Allows to read and write input events."
PKG_TOOLCHAIN="manual"

PKG_IS_ADDON="yes"
PKG_ADDON_NAME="python-evdev"
PKG_ADDON_TYPE="xbmc.python.module"
PKG_ADDON_PROJECTS="Allwinner RPi"


addon() {
  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/docs/
  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/lib/evdev/
  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/examples/
  cp -PR $(get_build_dir evdev)/docs/* $ADDON_BUILD/$PKG_ADDON_ID/docs
  cp -PR $(get_build_dir evdev)/build/lib.linux-*/evdev/* $ADDON_BUILD/$PKG_ADDON_ID/lib/evdev
  cp -PR $(get_build_dir evdev)/examples/* $ADDON_BUILD/$PKG_ADDON_ID/examples
  cp -PR $(get_build_dir evdev)/LICENSE $ADDON_BUILD/$PKG_ADDON_ID/LICENSE
  cp -PR $(get_build_dir evdev)/README.rst $ADDON_BUILD/$PKG_ADDON_ID/README.rst
}
