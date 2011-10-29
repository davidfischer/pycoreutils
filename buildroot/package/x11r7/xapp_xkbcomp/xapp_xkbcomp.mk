################################################################################
#
# xapp_xkbcomp -- compile XKB keyboard description
#
################################################################################

XAPP_XKBCOMP_VERSION = 1.1.1
XAPP_XKBCOMP_SOURCE = xkbcomp-$(XAPP_XKBCOMP_VERSION).tar.bz2
XAPP_XKBCOMP_SITE = http://xorg.freedesktop.org/releases/individual/app
XAPP_XKBCOMP_AUTORECONF = NO
XAPP_XKBCOMP_DEPENDENCIES = xlib_libX11 xlib_libxkbfile
HOST_XAPP_XKBCOMP_DEPENDENCIES = host-xlib_libX11 host-xlib_libxkbfile

$(eval $(call AUTOTARGETS,package/x11r7,xapp_xkbcomp))
$(eval $(call AUTOTARGETS,package/x11r7,xapp_xkbcomp,host))
