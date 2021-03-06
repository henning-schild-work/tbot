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
# End:

from tbotlib import tbot

# set board state for which the tc is valid
tb.set_board_state("u-boot")

tb.workfd = tb.c_ctrl
tb.eof_call_tc("tc_demo_get_ub_code.py")
tb.config.tc_demo_compile_install_test_poweroff = 'no'

tb.eof_call_tc("tc_demo_compile_install_test.py")

tb.end_tc(True)
