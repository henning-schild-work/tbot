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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_ub_ubi_info.py
# - simple print ubi info
# End:

from tbotlib import tbot

# set board state for which the tc is valid
tb.set_board_state("u-boot")

tmp = "ubi info"
tb.eof_write_cmd(tb.c_con, tmp)

tmp = "ubi info l"
tb.eof_write_cmd(tb.c_con, tmp)

tb.end_tc(True)
