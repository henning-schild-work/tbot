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
# start with
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_lab_compile_uboot.py
# compile u-boot
from tbotlib import tbot

read_line_retry_save=tb.read_line_retry
tb.read_line_retry=500
tmp = "make mrproper"
tb.eof_write_ctrl(tmp)
tb.eof_read_end_state_ctrl(1)

tmp = "make " + tb.boardname + "_defconfig"
tb.eof_write_ctrl(tmp)
tb.eof_search_str_in_readline_ctrl("configuration written to .config")
tb.read_line_retry=read_line_retry_save

tmp = "make all"
tb.eof_write_ctrl(tmp)
tb.eof_search_str_in_readline_end_ctrl("Error")

tb.eof_read_end_state_ctrl(1)
tb.end_tc(True)
