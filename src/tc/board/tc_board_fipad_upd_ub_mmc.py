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
# tbot.py -s lab_denx -c fipad -t tc_board_fipad_upd_ub_mmc.py
# update SPL and u-boot.img on the MMC0
# End:

from tbotlib import tbot

logging.info("typ: %s", tb.tc_board_fipad_upd_ub_typ)

# set board state for which the tc is valid
tb.set_board_state("linux")

tb.workfd = tb.c_con

# get rootfspath from cmdline ToDo
rootfspath = '/opt/eldk-5.5/armv7a-hf/rootfs-sato-sdk'
rootfsworkdir = '/home/hs/fipad'

tb.workfd = tb.c_ctrl
# copy files to rootfs dir
tb.statusprint("copy files")
c = tb.workfd
so = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/u-boot.img'
ta = rootfspath + rootfsworkdir + '/u-boot.img'
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)

so = "/tftpboot/" + tb.config.tftpboardname + "/" + tb.config.ub_load_board_env_subdir + '/SPL'
ta = rootfspath + rootfsworkdir + '/SPL'
tb.eof_call_tc("tc_lab_cp_file.py", ch=c, s=so, t=ta)

tb.workfd = tb.c_con
dev = '/dev/mmcblk0'
tmp = 'dd if=' + rootfsworkdir + '/SPL of=' + dev + ' bs=1K seek=1 oflag=sync status=none && sync'
tb.write_lx_cmd_check(tb.workfd, tmp)
tmp = 'dd if=' + rootfsworkdir + '/u-boot.img of=' + dev + ' bs=1K seek=69 oflag=sync status=none && sync'
tb.write_lx_cmd_check(tb.workfd, tmp)

tb.end_tc(True)
