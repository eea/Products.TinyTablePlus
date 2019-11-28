# Copyright (c) 1998-1999 Endicor Technologies, Inc.
# All rights reserved. Written by Ty Sarna <tsarna@endicor.com>
# Modified by Shane Hathaway. (April 2000)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

""" Import and Export data from TinyTablePlus to human readable CSV-type text
"""

import six
from six.moves import map
from six import BytesIO
import token, tokenize, Missing


class FormatError(Exception):
    pass

class ImportDataState(object):
    def __init__(self):
        self.rows = []
        self.row = []
        self.value = Missing.Value
        self.seenvalue = self.sign = 0
        self.lasttok = tokenize.ENDMARKER

    def token(self, t, s, src, erc, l):
        estr = "at line %d column %d" % src
        signerr = "Already have sign %s" % estr
        invtok = "invalid token %s %s" % (repr(s), estr)
        
        if t == token.OP:
            if  s == ',':
                self.row.append(self.value)
                self.value = Missing.Value
                self.seenvalue = self.sign = 0
            elif s == '+':
                if self.seenvalue or self.sign:
                    raise FormatError(signerr)
                self.sign = 1
            elif s == '-':
                if self.seenvalue or self.sign:
                    raise FormatError(signerr)
                self.sign = -1                
            else:
                raise FormatError(invtok)

        elif t == token.NAME:
            if s.upper() in ('NONE', 'NULL'):
                if self.seenvalue or self.sign:
                    raise FormatError(invtok)

                self.value = Missing.Value
                self.seenvalue = 1
            else:
                if self.seenvalue:
                    if isinstance(self.value, six.string_types):
                        self.value = self.value + ' ' + s
                    else:
                        raise FormatError(invtok)
                else:
                    self.value = s
                    self.seenvalue = 1

        elif t == token.STRING:
            if self.seenvalue or self.sign:
                raise FormatError(invtok)
            
            self.value = eval(s)
            self.seenvalue = 1

        elif t == token.NUMBER:
            if self.seenvalue:
                raise FormatError(invtok)
            
            self.value = eval(s)
            if self.sign < 0:
                self.value = -self.value
            self.seenvalue = 1

        elif t in (token.NEWLINE, tokenize.ENDMARKER):
            if t == tokenize.NEWLINE or self.lasttok != token.NEWLINE:
                self.row.append(self.value)
                self.seenvalue = self.sign = 0
                self.value = Missing.Value
                self.rows.append(self.row)
                self.row = []

        elif t in (token.ENCODING, tokenize.COMMENT, tokenize.NL):
            pass

        else:
            raise FormatError(invtok)

        self.lasttok = t


def ImportData(s):
    if len(s) < 1:
        # Patch by Shane, April 2000 - Check for empty data set.
        return []
    s = s.encode('utf-8')
    f = BytesIO(s)
    i = ImportDataState()
    token_gen = tokenize.tokenize(f.readline)
    for t in token_gen:
        i.token(t.type, t.string, t.start, t.end, t.line)

    return i.rows


# translate specialcharacter to escaped form
cval = {
    '\\'    :   '\\\\',
    '\"'    :   '\\\"',
    '\a'    :   '\\a',
    '\b'    :   '\\b',
    '\f'    :   '\\f',
    '\n'    :   '\\n',
    '\r'    :   '\\r',
    '\t'    :   '\\t',
    '\v'    :   '\\v'
}

    
def ExportVal(data):
    if data is Missing.Value:
        return "NULL"
    elif data is Missing.Value:
        return "NULL"
    elif isinstance(data, (int, float, int)):
        return str(data)
    elif isinstance(data, six.string_types):
        s = '"'
        for c in data:
            if c in cval:
                s = s + cval[c]
            elif ord(c) <= 31 or ord(c) >= 127:
                s = s + '\\%03o' % ord(c)
            else:
                s = s + c
        return s + '"'
    else:
        return '"' + str(data) + '"'

def ExportData(data):
    return '\n'.join(
        [', '.join(
                map(ExportVal, row)
            ) for row in data]
    )
