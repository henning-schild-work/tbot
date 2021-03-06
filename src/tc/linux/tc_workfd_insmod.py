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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_workfd_insmod.py
# insmod module tb.tc_workfd_insmod_module with
# module path tb.tc_workfd_insmod_mpath and
# tb.tc_workfd_insmod_module_path
# check if the strings in list tb.tc_workfd_insmod_module_checks
# come back when inserting the module.
# End:

from tbotlib import tbot

# here starts the real test
logging.info("args: %s %s %s %s", tb.workfd.name, tb.tc_workfd_insmod_module, tb.tc_workfd_insmod_mpath, tb.tc_workfd_insmod_module_path)
logging.info("args: %s", tb.tc_workfd_insmod_module_checks)

# set board state for which the tc is valid
tb.set_board_state("linux")

c = tb.workfd
tmp = 'rmmod ' + tb.tc_workfd_insmod_module
tb.eof_write_cmd(c, tmp)

tmp = 'uname -r'
tb.eof_write(c, tmp)

ret = tb.tbot_expect_string(c, '\n')
if ret == 'prompt':
    tb.end_tc(False)
ret = tb.tbot_expect_string(c, '\n')
if ret == 'prompt':
    tb.end_tc(False)

vers = tb.buf.rstrip()
tb.tbot_expect_prompt(c)

tmp = 'insmod ' + tb.tc_workfd_insmod_mpath + '/' + vers + '/' + tb.tc_workfd_insmod_module_path + '/' + tb.tc_workfd_insmod_module + '.ko'
tb.eof_write(c, tmp)
tb.tbot_rup_check_all_strings(c, tb.tc_workfd_insmod_module_checks, endtc=True)
