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
import logging
import sys
import os

class doc_backend(object):
    """extract from all executed testcases the logs from tbots connection.

    Format of the created filenames:

    testcasename_connectionname_index_incnumber.txt

      testcasename:   Name of TC

      connectionname: Name of the tbot connection

      index: counts, how often the TC was called, starts with 1

      incnumber: each switch to another connection increments this number
                 starts with 1
 
    This files could be used to create documentation
    files, which contains logs.

    enable this backend with "create_documentation = 'yes'"

    created files are stored in tb.workdir + '/logfiles/
    so, be sure you have created this directory.

    Problem: First prompt is not visible

    see https://github.com/hsdenx/tbot/blob/testing/scripts/demo/documentation_backend/README
    for a demo, how you can create a html/pdf/man page, which
    contains content of tbot logfiles and text around it.

    - **parameters**, **types**, **return** and **return types**::
    :param arg1: tb
    :param arg2: list of strings, containing testcasesnames, which get ignored
    """
    def __init__(self, tb, ignorelist):
        self.dotnr = 0
        self.tb = tb
        self.ev = self.tb.event
        self.tc_list = []
        self.ignoretclist = ignorelist

    def create_docfiles(self):
        """create the files
        """
        el = list(self.tb.event.event_list)
        self._analyse(el, 'main')
 
    def _get_event_id(self, tmp):
        if tmp[self.ev.id] == 'Start':
            return tmp[self.ev.id]
        if tmp[self.ev.id] == 'End':
            return tmp[self.ev.id]
        if tmp[self.ev.id] == 'log':
            return tmp[self.ev.id]
        return 'none'

    def _get_event_name(self, tmp):
        return tmp[self.ev.name]

    def _get_next_event(self, el):
        if el == None:
            return ''

        if len(el) == 0:
            return ''

        ret = el[0]
        el.pop(0)
        return ret

    def _check_ignore_list(self, typ, name, evl):
        if typ != 'Start':
            return 'ok'

        for ign in self.ignoretclist:
            if ign == name:
                # search until End event
                line = 'start'
                while line != '':
                    line = self._get_next_event(evl)
                    tmp = line.split()
                    if tmp == []:
                        continue
                    if tmp[self.ev.typ] != 'EVENT':
                        continue
                    eid = self._get_event_id(tmp)
                    if eid == 'none':
                        continue
                    newname = self._get_event_name(tmp)
                    if newname == name and eid == 'End':
                        return 'ignore'

        return 'ok'

    def _search_in_list(self, name):
        for el in self.tc_list:
            if el[0] == name:
                # tuples are immutable ...
                nr = el[1]
                nr = nr + 1
                # delete element
                self._rm_from_list(name)
                # add element
                self._add_to_list(name, nr)
                return nr

        return 0

    def _add_to_list(self, name, value):
        newel = name, value
        self.tc_list.append(newel)

    def _rm_from_list(self, name):
        new_list = []
        for s in self.tc_list:
            if not s[0] == name:
                new_list.append(s)
        self.tc_list = new_list

    def _create_fn(self, filename, conname, index, lnr):
        fn = filename.replace("/", "_")
        return self.tb.workdir + '/logfiles/' + fn + '_' + conname + '_' + str(index) + '_' + str(lnr) + '.txt'

    def _analyse(self, evl, name):
        filename = name
        index = self._search_in_list(name)
        if index == 0:
            self._add_to_list(name, 1)
            index = 1
        lnr = 1
        oldname = 'none'
	end = False
        while end != True:
            line = self._get_next_event(evl)
            tmp = line.split()
            if line == '':
                end = True
            if tmp == []:
                continue
            if tmp[self.ev.typ] != 'EVENT':
                continue
            eid = self._get_event_id(tmp)
            if eid == 'none':
                continue
            newname = self._get_event_name(tmp)
            ret = self._check_ignore_list(eid, newname, evl)
            if ret == 'ignore':
                continue
            if eid == 'Start':
                self._analyse(evl, newname)
            if eid == 'End':
                try:
                    fd.close()
                except:
                    print("filename no entry")
                return
            if eid == 'log':
                logline = line.split(newname)
                logline = logline[1]
                logline = logline.strip()
                if logline[:1] == 'r':
            	    logline = logline[1:]
                else:
                    continue
 
                if oldname == 'none':
                    oldname = newname
                    fd = open(self._create_fn(filename, newname, index, lnr), 'w')
                    fd.write(logline)
                elif oldname == newname:
                    fd.write(logline)
                else:
                    fd.close()
                    lnr = lnr + 1
                    fd = open(self._create_fn(filename, newname, index, lnr), 'w')
                    oldname = newname