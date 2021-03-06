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
# python2.7 src/common/tbot.py -s lab_denx -s labconfigname -c boardconfigname -t tc_ub_create_imx6_reg_file.py
#
# creates U-Boot register dump files for an imx6 based board.
# using testcase tc_ub_create_reg_file.py
#
# dumps:
# - pinmux  20e0000 - 20e0950
#
# into files found in src/files/
# create for your board a subdir in the directory,
# and move the new created files into it, so you have
# them as a base for comparing further use.
#
# End:

import datetime
from tbotlib import tbot

logging.info("args: none")

# set board state for which the tc is valid
tb.set_board_state("u-boot")
tb.workfd = tb.c_con

tb.config.tc_ub_create_reg_file_name = 'src/files/ub_new_imx6_pinmux.reg'
tb.config.tc_ub_create_reg_file_comment = 'imx6 pinmux'
tb.config.tc_ub_create_reg_file_start = '20e0000'
tb.config.tc_ub_create_reg_file_stop = '20e0950'
tb.config.tc_ub_readreg_mask = '0xffffffff'
tb.config.tc_ub_create_reg_file_mode = 'w+'
tb.config.tc_ub_readreg_type = 'l'
tb.eof_call_tc("tc_ub_create_reg_file.py")

tb.end_tc(True)
