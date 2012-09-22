#-*- encoding: utf8 -*-
import pep8
import StringIO
import sys
import os
import tempfile

def pep8parser(strings):
    """
    Convert strings from pep8 results to list of dictionaries
    """
    result_list = []
    for s in strings[1:]:
        temp = s.split(":")
        if len(temp) < 4:
            continue
        temp_dict = {'type': temp[3][1],
                     'code': temp[3][2:5],
                     'line': temp[1],
                     'place': temp[2],
                     'text': temp[3][6:]}
        result_list.append(temp_dict)
    return result_list


def check_text(text, temp_dir, add_options=None):
    """
    check text for pep8 requirements
    """
    #prepare code
    code_file, code_filename = tempfile.mkstemp(dir=temp_dir)
    with open(code_filename, 'w') as code_file:
        code_file.write(text.decode('utf8'))
    #initialize pep8 checker
    pep8style = pep8.StyleGuide(parse_argv=False, config_file=False)
    options = pep8style.options
    if add_options:
        options._update_careful(add_options)
    checker = pep8.Checker(code_filename, options=options)
    #redirect print and get result
    temp_outfile = StringIO.StringIO()
    sys.stdout = temp_outfile
    checker.check_all()
    sys.stdout = sys.__stdout__
    result = temp_outfile.buflist[:]
    #clear all
    temp_outfile.close()
    code_file.close()
    os.remove(code_filename)
    result_dict = pep8parser(result)
    return result_dict


if __name__ == '__main__':
    pass
