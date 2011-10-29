################################################################################
#
# xapp_xclipboard -- interchange between cut buffer and selection
#
################################################################################

XAPP_XCLIPBOARD_VERSION = 1.0.1
XAPP_XCLIPBOARD_SOURCE = xclipboard-$(XAPP_XCLIPBOARD_VERSION).tar.bz2
XAPP_XCLIPBOARD_SITE = http://xorg.freedesktop.org/releases/individual/app
XAPP_XCLIPBOARD_AUTORECONF = NO
XAPP_XCLIPBOARD_DEPENDENCIES = xlib_libXaw

$(eval $(call AUTOTARGETS,package/x11r7,xapp_xclipboard))
