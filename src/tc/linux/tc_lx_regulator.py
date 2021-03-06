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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_lx_regulator.py
# check if regulators in tb.config.tc_lx_regulator_nrs exist, and have
# the correct microvolts settings.
# End:

from tbotlib import tbot

logging.info("args: %s", tb.config.tc_lx_regulator_nrs)

tb.set_board_state("linux")

c = tb.c_con
def check_regulator(tb, c, nr, name, volts):
    tmp = 'cat /sys/class/regulator/regulator.' + nr + '/name'
    tb.eof_write(c, tmp)
    ret = tb.tbot_expect_string(c, name)
    if ret == 'prompt':
        tb.end_tc(False)
    if volts != '-':
        tb.tbot_expect_prompt(c)
        tmp = 'cat /sys/class/regulator/regulator.' + nr + '/microvolts'
        tb.eof_write_con(tmp)
        ret = tb.tbot_expect_string(c, volts)
        if ret == 'prompt':
            tb.end_tc(False)
    tb.tbot_expect_prompt(c)

for nr in tb.config.tc_lx_regulator_nrs:
    nr_list = nr.split()
    check_regulator(tb, c, nr_list[0], nr_list[1], nr_list[2])

tb.end_tc(True)
