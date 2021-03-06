#!/usr/bin/python
# -*- coding: utf-8 -*-

# INTEL CONFIDENTIAL Copyright 2015 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors.
# Title to the Material remains with Intel Corporation or its suppliers and
# licensors.
# The Material contains trade secrets and proprietary and confidential information
# of Intel or its suppliers and licensors. The Material is protected by worldwide
# copyright and trade secret laws and treaty provisions.
# No part of the Material may be used, copied, reproduced, modified, published,
# uploaded, posted, transmitted, distributed, or disclosed in any way without
# Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise.
#
# Any license under such intellectual property rights must be express and
# approved by Intel in writing

import sys
import argparse
import ctypes
import binascii

import factory_data

base_addr = hex(0xffffe000 + 0x200)

def main():
# Parse input arguments
    parser = argparse.ArgumentParser(description="Generate a binary file containing"
        "various provisioning product info such as product serial number.")
    parser.add_argument('--product_sn', help="the product serial number, up to 16 ASCII characters", required=True)
    parser.add_argument('--product_name', help="the product hardware version, 1 byte in hexadecimal", required=True)
    parser.add_argument('--product_type', help="the product hardware type, 1 byte in hexadecimal", required=True)
    parser.add_argument('--product_revision', help="the product hardware revision, 1 byte in hexadecimal", required=True)
    parser.add_argument('--product_variant', help="the product hardware variant, 1 byte in hexadecimal", required=True)
    args = parser.parse_args()


# Create instance of customer data struct
    product_data = factory_data.CustomerData()

    # Add the product serial number
    ############
    assert len(args.product_sn) <= 16

    product_sn_padded = args.product_sn.ljust(16, '\0')
    product_data.product_sn = (ctypes.c_ubyte * 16).from_buffer_copy(bytearray(product_sn_padded))

    print "Product S/N        : " + product_sn_padded

    # Add the product hardware name
    ############
    assert len(args.product_name) <= 2

    product_name_padded = args.product_name.rjust(2, '0')
    product_data.product_name = ctypes.c_ubyte.from_buffer_copy(binascii.unhexlify(product_name_padded))

    print "Product HW name    : " + product_name_padded

    # Add the product hardware type
    ############
    assert len(args.product_type) <= 2

    product_type_padded = args.product_type.rjust(2, '0')
    product_data.product_type = ctypes.c_ubyte.from_buffer_copy(binascii.unhexlify(product_type_padded))

    print "Product HW type    : " + product_type_padded

    # Add the product hardware revision
    ############
    assert len(args.product_revision) <= 2

    product_revision_padded = args.product_revision.rjust(2, '0')
    product_data.product_revision = ctypes.c_ubyte.from_buffer_copy(binascii.unhexlify(product_revision_padded))

    print "Product HW revision: " + product_revision_padded

    # Add the product hardware variant
    ############
    assert len(args.product_variant) <= 2

    product_variant_padded = args.product_variant.rjust(2, '0')
    product_data.product_variant = ctypes.c_ubyte.from_buffer_copy(binascii.unhexlify(product_variant_padded))

    print "Product HW variant : " + product_variant_padded

    # Pad with 0xFF to fit project_data size
    ############
    product_data_padded = bytearray().ljust(len(product_data.reserved), binascii.unhexlify("FF"))
    product_data.reserved = type(product_data.reserved).from_buffer_copy(product_data_padded)

# Save the .bin file
    arr = bytearray(product_data)
    assert len(arr) == 512, "ERROR: product data struct size error"
    out_file = open("factory_data_product.bin", "wb")
    out_file.write(arr)
    out_file.close()


# Creates the OpenOCD flash script
    flash_script = """### Generated script, please do not edit
### Flash product provisining data in OTP
load_image factory_data_product.bin %s
verify_image factory_data_product.bin %s
""" % (base_addr, base_addr)
    f = open('factory_data_product.cmd', 'w')
    f.write(flash_script)
    f.close()


if __name__ == "__main__":
    sys.exit(main())
