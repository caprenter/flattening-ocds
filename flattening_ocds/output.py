"""Code to output a parsed flattened JSON schema in various spreadsheet
formats."""

import xlsxwriter
import csv
import os


class SpreadsheetOutput(object):
    # output_name is given a default here, partly to help with tests,
    # but should have been defined by the time we get here.
    def __init__(self, parser, main_sheet_name='main', output_name='release'):
        self.parser = parser
        self.main_sheet_name = main_sheet_name
        self.output_name = output_name

    def open(self):
        pass

    def write_sheet(self, sheet_name, sheet_header):
        raise NotImplementedError

    def write_sheets(self):
        self.open()

        self.write_sheet(self.main_sheet_name, self.parser.main_sheet)
        for sheet_name, sheet_header in sorted(self.parser.sub_sheets.items()):
            self.write_sheet(sheet_name, sheet_header)

        self.close()

    def close(self):
        pass


class XlsxOutput(SpreadsheetOutput):
    def open(self):
        self.workbook = xlsxwriter.Workbook(self.output_name+'.xlsx')

    def write_sheet(self, sheet_name, sheet_header):
        worksheet = self.workbook.add_worksheet(sheet_name)
        for i, field in enumerate(sheet_header):
            worksheet.write(0, i, field)

    def close(self):
        self.workbook.close()


class CSVDirectoryOutupt(SpreadsheetOutput):
    def open(self):
        try:
            os.makedirs(self.output_name)
        except OSError:
            pass

    def write_sheet(self, sheet_name, sheet_header):
        with open(os.path.join(self.output_name, sheet_name+'.csv'), 'w') as csv_file:
            csv_sheet = csv.writer(csv_file)
            csv_sheet.writerow(sheet_header)


FORMATS = {
    'xlsx': XlsxOutput,
    'csv': CSVDirectoryOutupt
}
