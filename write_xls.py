import xlwt


def write_xls(path, codetable):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet', cell_overwrite_ok=True)
    rownum = 0
    for row in codetable:
        cellnum = 0
        for cell in row:
            sheet1.write(rownum, cellnum, cell)
            cellnum += 1
        rownum += 1

    f.save(path)

