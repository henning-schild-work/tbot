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
#
# switch bootmode for the bbb
#
# - power off the board
# - set bootmode
#   2 states:
#   normal: we use emmc
#   recovery: we boot from sd card
#
# End:

from tbotlib import tbot

logging.info("arg: %s", tb.config.tc_board_bootmode)

tb.set_board_state("lab")
savefd = tb.workfd
tb.workfd = tb.c_ctrl

tb.eof_call_tc("tc_lab_poweroff.py")

# low = emmc boot
state = 'high'
if tb.config.tc_board_bootmode == 'normal':
    state = 'low'

tb.eof_call_tc("tc_workfd_set_gpio.py", highlow=state, gpio=tb.config.jumper)

tb.workfd = savefd
tb.end_tc(True)
