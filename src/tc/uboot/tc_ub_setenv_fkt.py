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
# python2.7 src/common/tbot.py -s lab_denx -c beagleboneblack -t tc_ub_setenv_fkt.py
# set U-Boot Environmentvariable tb.config.setenv_name with value
# tb.config.setenv_value
#
# This is for demonstration how to use functions in tbot only.
# So, this testcase sets 3 times the U-Boot Envvariable:
# - The new way with importing the functions from testcase
#   src/tc/uboot/tc_ub_testfkt.py
# - The oldstyled way with calling the testcase tc_ub_testfkt.py
#   with tb.eof_call_tc()
# - The oldstyled way with calling the testcase tc_ub_testfkt.py
#   with tb.call_tc() and getting the return value.
# End:

from tbotlib import tbot

# here starts the real test
logging.info("testcase arg: %s %s", tb.config.setenv_name, tb.config.setenv_value)
# set board state for which the tc is valid
tb.set_board_state("u-boot")

# set env var
c = tb.c_con

# calling functions in testcase src/tc/uboot/tc_ub_testfkt.py

# import testcase
import tc_ub_testfkt

print ("****************** Set through fkt")
# set U-Boot Envvariable
tc_ub_testfkt.ub_setenv(tb, c, tb.config.setenv_name, tb.config.setenv_value)
# check if it is set with the correct value
tc_ub_testfkt.ub_checkenv(tb, c, tb.config.setenv_name, tb.config.setenv_value)

print ("****************** Set through eof_call_tc")
# now Test with old styled way tb.eof_call_tc
tb.eof_call_tc("tc_ub_testfkt.py")

print ("****************** Set through call_tc")
# and tb.call_tc
ret = tb.call_tc("tc_ub_testfkt.py")

tb.end_tc(ret)
