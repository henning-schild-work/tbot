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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_workfd_compile_uboot.py
# compile u-boot
# End:

from tbotlib import tbot

tb.eof_call_tc("tc_workfd_goto_uboot_code.py")

if tb.config.tc_lab_compile_uboot_export_path != 'none':
    tb.event.create_event('main', 'tc_lab_compile_uboot.py', 'SET_DOC_FILENAME', 'compile_uboot_set_dtc')
    tmp = "printenv PATH | grep --color=never " + tb.config.tc_lab_compile_uboot_export_path
    ret = tb.write_lx_cmd_check(tb.workfd, tmp, endTC=False)
    if ret == False:
        tmp = "export PATH=" + tb.config.tc_lab_compile_uboot_export_path + ":$PATH"
        tb.write_lx_cmd_check(tb.workfd, tmp)

tb.event.create_event('main', 'tc_lab_compile_uboot.py', 'SET_DOC_FILENAME', 'compile_uboot_mrproper')
tmp = "make mrproper"
tb.write_lx_cmd_check(tb.workfd, tmp)

tb.event.create_event('main', 'tc_lab_compile_uboot.py', 'SET_DOC_FILENAME', 'compile_uboot_config')
defname = tb.config.tc_lab_compile_uboot_boardname + "_defconfig"
tmp = "make " + defname
tb.event.create_event('main', tb.config.boardname, "UBOOT_DEFCONFIG", defname)
tb.write_lx_cmd_check(tb.workfd, tmp)
if tb.workfd.name == 'tb_cpc':
    tb.event.create_event('main', tb.config.boardname, "UBOOT_SRC_PATH", tb.config.tftpdir + '/' + tb.config.tftpboardname + '/' + tb.config.ub_load_board_env_subdir)
else:
    tb.event.create_event('main', tb.config.boardname, "UBOOT_SRC_PATH", tb.config.tc_lab_source_dir + "/u-boot-" + tb.config.boardlabname)

tb.event.create_event('main', 'tc_lab_compile_uboot.py', 'SET_DOC_FILENAME', 'compile_uboot_make')
tmp = "make " + self.config.tc_lab_compile_uboot_makeoptions + " all"
tb.write_lx_cmd_check(tb.workfd, tmp)

tb.end_tc(True)
