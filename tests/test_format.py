import pytest

import sqlparse
from sqlparse.exceptions import SQLParseError


class TestFormat:
    def test_keywordcase(self):
        sql = 'select * from bar; -- select foo\n'
        file = open('/home/patrick/projs/sqlparse/data.sql',mode='r')

        # read all lines at once
        all_of_it = file.read()

        # close the file
        file.close()
        res = sqlparse.format(all_of_it, identifier_case='upper')
        print(res)
        

        f = open("/home/patrick/projs/sqlparse/data.out.sql", "w")
        f.write(res)
        f.close()