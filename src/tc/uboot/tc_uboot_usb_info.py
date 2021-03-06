# This file is part of tbot.  tbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Description:
# start with
# python2.7 src/common/tbot.py -s lab_denx -c fipad -t tc_uboot_usb_info.py
#
# call "usb info" command
#
# used vars:
# tb.config.tc_uboot_usb_info_expect = ['Hub,  USB Revision 2.0',
#    'Mass Storage,  USB Revision 2.0']
# End:

from tbotlib import tbot

try:
    tb.config.tc_uboot_usb_info_expect
except:
    tb.config.tc_uboot_usb_info_expect = ['Hub,  USB Revision 2.0',
    'Mass Storage,  USB Revision 2.0']

# here starts the real test
logging.info("testcase arg: %s", tb.config.tc_uboot_usb_info_expect)
# set board state for which the tc is valid
tb.set_board_state("u-boot")

# set env var
c = tb.c_con

l = tb.config.tc_uboot_usb_info_expect
tb.eof_write(c, "usb info")
tb.tbot_rup_check_all_strings(c, l, endtc=True)

tb.end_tc(True)
