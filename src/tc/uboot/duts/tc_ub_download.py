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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_ub_download.py
# convert duts tests from:
# http://git.denx.de/?p=duts.git;a=blob;f=testsystems/dulg/testcases/15_UBootCmdGroupDownload.tc;h=8e58d53add90b680ef7a1300894d2392f90d9824;hb=101ddd5dbd547d5046363358d560149d873b238a
# End:

from tbotlib import tbot

try:
    tb.config.tc_ub_download_load
except:
    tb.config.tc_ub_download_load = 'yes'

# set board state for which the tc is valid
tb.set_board_state("u-boot")

cmdlist = [
"help bootp",
"help dhcp",
"help loadb",
"help loads",
"help rarp",
"help tftp"
]

tb.eof_write_cmd_list(tb.c_con, cmdlist, create_doc_event=True)

ret = tb.write_cmd_check(tb.c_con, "help loadb", "Unknown command", create_doc_event=True)
if ret == True:
    # we have no loadb cmd, exit
    tb.end_tc(True)

if tb.config.tc_ub_download_load != 'yes':
    tb.end_tc(True)

tb.eof_call_tc("tc_workfd_get_uboot_config_vars.py")

# check if u-boot.img file exists, if not
save = tb.workfd
tb.workfd = tb.c_ctrl
tfile = tb.config.tftpdir + '/' + tb.config.tc_ub_tftp_path + '/u-boot.img'
tb.config.tc_workfd_check_if_file_exists_name = tfile
ret = tb.call_tc("tc_workfd_check_if_file_exist.py")
if ret != True:
    # check if u-boot.bin exists, if not end
    binfile = tb.config.tftpdir + '/' + tb.config.tc_ub_tftp_path + '/u-boot.bin'
    tb.config.tc_workfd_check_if_file_exists_name = binfile
    ret = tb.call_tc("tc_workfd_check_if_file_exist.py")
    if ret !=  True:
        tb.workfd = save
        tb.end_tc(True)

    # if yes, create u-boot.img
    cmd = 'mkimage -A arm -O u-boot -d ' + binfile + ' ' + tfile
    ret = tb.write_lx_cmd_check(tb.workfd, cmd, endTC=False, split=tb.workfd.line_length / 2)
    if ret != True:
        tb.workfd = save
        tb.end_tc(True)

tb.workfd = save
tb.config.tc_uboot_load_bin_ram_addr = tb.config.tc_ub_memory_ram_ws_base.replace('0x', '')
tb.config.tc_uboot_load_bin_file = tfile
tb.eof_call_tc("tc_uboot_load_bin_with_kermit.py")
tb.eof_write_cmd(tb.c_con, "imi " + tb.config.tc_uboot_load_bin_ram_addr, create_doc_event=True)

tb.end_tc(True)
