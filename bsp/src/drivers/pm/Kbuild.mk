obj-y += wakelocks.o
obj-y += device.o
# FIXME: Move usb_pm config in Kconfig when ready
ifeq ($(CONFIG_CURIE),y)
ifeq ($(CONFIG_QUARK_SE_QUARK),y)
obj-$(CONFIG_USB_PM) += usb_pm.o
endif
endif
obj-$(CONFIG_BLE_CORE_SUSPEND_BLOCKER_PM) += ble_core_pm.o
