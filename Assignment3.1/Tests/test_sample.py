import parser
def parse():
    x,y = parser_test.parse_svn()
    print(x)
    return x,y

def test_message():
    x = parser_test.parse_svn()
    svn_log = x[1]
    assert svn_log[0]["message"] == "adding 2.1"

def test_message2():
    x = parser_test.parse_svn()
    svn_log = x[1]
    assert svn_log[1]["message"] == "Assignment2.0"

def test_author():
    x = parser_test.parse_svn()
    svn_log = x[1]
    assert svn_log[0]["author"] == "festekj2"
    assert svn_log[1]["author"] == "festekj2"

def test_date():
    x = parser_test.parse_svn()
    svn_log = x[1]
    assert svn_log[0]["date"] == "2016-03-03T09:20:55.634947Z"
    assert svn_log[1]["date"] == "2016-02-25T22:51:35.968479Z"

def test_revision():
    x = parser_test.parse_svn()
    svn_log = x[1]
    assert svn_log[0]["revision"] == "7852"
    assert svn_log[1]["revision"] == "7094"


def test_list_assignment():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[0]["assignment"] == "Assignment1.0"
def test_list_file():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[1]["filepath"] == "Assignment1.0/.idea"
def test_list_type():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[0]["kind"] == "dir"
    assert svn_list[1]["kind"] == "dir"
def test_list_author():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[0]["author"] == "festekj2"
    assert svn_list[1]["author"] == "festekj2"
def test_list_revision():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[0]["revision"] == "3503"
    assert svn_list[1]["revision"] == "3503"
def test_list_date():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[0]["date"] == "2016-02-04T20:48:48.414829Z"
    assert svn_list[1]["date"] == "2016-02-04T20:48:48.414829Z"
def test_list_belong():
    x = parser_test.parse_svn()
    svn_list = x[0]
    assert svn_list[1]["belongs"] == "Assignment1.0"
