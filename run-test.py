from __future__ import print_function


import os
import subprocess
import tabulate
from os import listdir
from os.path import isfile, join


class RunTest:
    '''
    Assumption is that the tests are named the same as the file they are testing
    except with a prepended 'test_'
    '''
    def __init__(self):
        self.files_to_test = []
        self.options = ''  # '--coverage'
        self.trial_run = 'trial {} tests/test_'.format(self.options)
        self.results = []
        self.match_covered = "'/>>>>>>/d;/^\s*$/d;/\s*#/d;/\s*:param/d;s/^[ \t]*//;/^[^0-9]/d'"
        self.match_total = r"'/^\s*$/d;/\s*#/d;s/^[ \t]*//;/\s*:param/d;/\s*:return/d;/\s*\x27\x27\x27/d;'"
        # cat | sed | wc -l
        self.cat = 'cat _trial_temp/coverage/'
        self.total_result = {"loc": 0, "covered": 0}

    def run_all_tests(self):
        os.system(self.trial_run+'*'+'.py')

    def genarate_line_count_cmd(self, file_name, matches):
        return self.cat + file_name + '.cover |' + 'sed ' + matches + '| wc -l'

    def parse_coverage_file(self, file_name):
        str_total_lines_cov = self.genarate_line_count_cmd(file_name, self.match_covered)
        str_total_lines = self.genarate_line_count_cmd(file_name, self.match_total)

        total_lines_cov = int(subprocess.check_output(str_total_lines_cov, shell=True))
        total_lines_code = int(subprocess.check_output(str_total_lines, shell=True))
        try:
            percentage = (total_lines_cov/float(total_lines_code)) * 100
        except ZeroDivisionError:
            percentage = 0

        result = [file_name, total_lines_code, total_lines_cov, percentage]

        self.total_result['loc'] += total_lines_code
        self.total_result['covered'] += total_lines_cov

        self.results.append(result)

    def output_results(self):
        try:
            per = (self.total_result['covered'] /
                   float(self.total_result['loc'])) * 100
        except ZeroDivisionError:
            per = 0

        print('Results: ')
        print('')
        self.results.append(['----------', '----------', '----------', '----------'])
        self.results.append(['Total:', self.total_result['loc'],
                             self.total_result['covered'], per])
        print(tabulate.tabulate(self.results, headers=["file_name",
                                                       "total lines of code",
                                                       "covered lines",
                                                       "Percent"]))

    def get_file_names(self):
        path = join(os.getcwd(), 'tests')
        allfiles = [f for f in listdir(path) if isfile(join(path, f))]
        validfiles = [self.strip_name(f) for f in allfiles
                      if f.endswith('.py') and not f.startswith('__init__')]
        return validfiles

    def strip_name(self, name):
        name = name.replace('test_', '')
        name = name.strip('.py')
        return name

    def run(self):
        self.files_to_test = self.get_file_names()
        self.run_all_tests()
        for f in self.files_to_test:
            self.parse_coverage_file(f)
        self.output_results()

if __name__ == "__main__":
    rt = RunTest()
    rt.run()
