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
# python2.7 src/common/tbot.py -s labconfigname -c boardconfigname -t tc_ub_flinfo.py
# convert duts tests from:
# http://git.denx.de/?p=duts.git;a=blob;f=testsystems/dulg/testcases/10_UBootFlinfo.tc;h=f5b728258250211d86dc9c6a9208639d8542b845;hb=101ddd5dbd547d5046363358d560149d873b238a
# End:

from tbotlib import tbot

# set board state for which the tc is valid
tb.set_board_state("u-boot")

cmdlist = [
"help flinfo",
"flinfo",
]

tb.eof_write_cmd_list(tb.c_con, cmdlist, create_doc_event=True)
tb.end_tc(True)
