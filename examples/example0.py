# -*- coding: utf-8 -*-

import os
import copy
from datetime import datetime
from xltpl.writer import BookWriter
from xltpl.writerx import BookWriter as BookWriterx


def write_test(writer_cls, tpl_fname, result_fname0, result_fname1):
    pth = os.path.dirname(__file__)
    fname = os.path.join(pth, tpl_fname)
    writer = writer_cls(fname)
    writer.jinja_env.globals.update(dir=dir, getattr=getattr)

    now = datetime.now()

    person_info = {'address': u'福建行中书省福宁州傲龙山庄', 'name': u'龙傲天', 'fm': 178, 'date': now}
    person_info2 = {'address': u'Somewhere over the rainbow', 'name': u'Hello Wizard', 'fm': 156, 'date': now}
    rows = [['1', '1', '1', '1', '1', '1', '1', '1', ],
            ['1', '1', '1', '1', '1', '1', '1', '1', ],
            ['1', '1', '1', '1', '1', '1', '1', '1', ],
            ['1', '1', '1', '1', '1', '1', '1', '1', ],
             [1, 1, 1, 1, 1, 1, 1, 1, ],
             [1, 1, 1, 1, 1, 1, 1, 1, ],
             [1, 1, 1, 1, 1, 1, 1, 1, ],
             [1, 1, 1, 1, 1, 1, 1, 1, ],
             [1, 1, 1, 1, 1],
            ]
    person_info['rows'] = rows
    person_info['tpl_idx'] = 0
    person_info2['rows'] = rows
    person_info2['tpl_name'] = 'en'
    person_info3 = copy.copy(person_info2)
    person_info3['sheet_name'] = 'hello sheet'
    person_info4 = copy.copy(person_info2)
    person_info4['tpl_name'] = 'ex'
    person_info4['sheet_name'] = 'cols'
    payloads = [person_info, person_info2, person_info3, person_info4]
    writer.render_book(payloads=payloads)
    fname = os.path.join(pth, result_fname0)
    writer.save(fname)
    payloads = [person_info3, person_info, person_info2]
    writer.render_book(payloads=payloads)
    writer.render_sheet(person_info2, 'form2', 1)
    fname = os.path.join(pth, result_fname1)
    writer.save(fname)


if __name__ == "__main__":
    tpl_name = 'example.xls'
    result_fname0 = 'result00.xls'
    result_fname1 = 'result01.xls'
    writer_cls = BookWriter
    write_test(writer_cls, tpl_name, result_fname0, result_fname1)

    tpl_name = 'example.xlsx'
    result_fname0 = 'result00.xlsx'
    result_fname1 = 'result01.xlsx'
    writer_cls = BookWriterx
    write_test(writer_cls, tpl_name, result_fname0, result_fname1)
