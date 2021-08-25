# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)

PKG_NAME="opi-tools"
PKG_VERSION="1.0"
PKG_REV="003"
PKG_ARCH="arm"
PKG_LICENSE="MIT"
PKG_SITE="https://libreelec.tv"
PKG_URL=""
PKG_DEPENDS_TARGET="toolchain OrangePi.GPIO"
PKG_SECTION="virtual"
PKG_SHORTDESC="A bundle of tools and programs for use on the Orange Pi"
PKG_LONGDESC="This bundle currently includes OrangePi.GPIO"
PKG_DISCAIMER="Orange Pi is a trademark of the Shenzhen Xunlong Software CO., Limited"

PKG_IS_ADDON="yes"
PKG_ADDON_NAME="Orange Pi Tools"
PKG_ADDON_TYPE="xbmc.python.module"
PKG_ADDON_PROJECTS="Allwinner"


addon() {
  mkdir -p $ADDON_BUILD/$PKG_ADDON_ID/lib/OPi/
  cp -PR $(get_build_dir OrangePi.GPIO)/build/lib.linux-*/OPi/* $ADDON_BUILD/$PKG_ADDON_ID/lib/OPi
}
