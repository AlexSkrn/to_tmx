"""Provide tests for tmx-tradosizer."""
# import pytest
from to_tmx import tmx_tradosizer
from to_tmx import to_tmx


def test_build_trg_file_name_single_input(tmpdir):
    """Function should return correct filename from a single input."""
    trg_file = tmpdir.join('eng_rus.txt')
    expected = "eng_rus.tmx"
    head, tail = to_tmx.build_trg_file_name(trg_file)
    assert tail == expected
    assert head == tmpdir.strpath


def test_build_trg_file_name_double_input(tmpdir):
    """Function should return correct filename from a two-file input."""
    src_file_eng = tmpdir.join('eng.txt')
    src_file_rus = tmpdir.join('rus.txt')
    expected = "eng-rus.tmx"
    head, tail = to_tmx.build_trg_file_name(src_file_eng, src_file_rus)
    assert tail == expected
    assert head == tmpdir.strpath


def test_to_tmx_create_tmx(tmpdir):
    """create_tmx() should create a file which should contain a certain string."""
    # Creates 2 temp files with specific content
    eng_file = tmpdir.join('eng.txt')
    rus_file = tmpdir.join('rus.txt')
    eng_file.write("Line 1\nLine 2")
    rus_file.write("Строка 1\nСтрока 2".encode("utf-32-be"))
    # This should create 1 more file in the temp dir
    to_tmx.create_tmx(eng_file, rus_file)
    assert len(tmpdir.listdir()) == 3
    for f in tmpdir.visit("*eng-rus.tmx"):
        assert "Line 1" in f.read()


def test_to_tmx_create_tmx_single_file(tmpdir):
    """create_tmx() should create a file which should contain a certain string."""
    # Creates 2 temp files with specific content
    eng_rus_file = tmpdir.join('english_russian.txt')
    eng_rus_file.write("Line 1-1\tLine 1-2")
    # eng_rus_file.write("Line 1\tСтрока 1".encode("utf-32-be"))
    # eng_rus_file.write("Line 2\tСтрока 2".encode("utf-32-be"))
    # This should create 1 more file in the temp dir
    to_tmx.create_tmx(eng_rus_file)
    assert len(tmpdir.listdir()) == 2
    for f in tmpdir.visit("*english_russian.tmx"):
        assert "Line 1" in f.read()


def test_add_tree_elements():
    """The tree should contain certain elements."""
    import io
    tmx = """<?xml version='1.0' encoding='UTF-8'?>
    <tmx version="1.4">
      <header srclang="en-US" />
      <body>
        <tu>
          <tuv xml:lang="EN-US">
            <seg>The White House</seg>
          </tuv>
          <tuv xml:lang="RU-RU">
            <seg>Белый дом</seg>
          </tuv>
        </tu>
        <tu>
          <tuv xml:lang="EN-US">
            <seg>Office of the Press Secretary</seg>
          </tuv>
          <tuv xml:lang="RU-RU">
            <seg>Офис пресс-секретаря</seg>
          </tuv>
        </tu>
      </body>
    </tmx>
    """
    # f = io.StringIO(tmx)

    tree = tmx_tradosizer.add_tree_elements(tmx, 'some file name.tmx')
    # Save the modifed tmx file
    toF = io.BytesIO()
    tree.write(toF, encoding='UTF-8', xml_declaration=True)

    tmx_res = toF.getvalue().decode('utf-8')
    print(tmx_res)

    test1 = """<header creationtool="SDL Language Platform" o-tmf="SDL TM8 Format" srclang="en-US">"""
    test2 = """<prop type="x-Recognizers">RecognizeAll</prop>"""
    test3 = """<prop type="x-filename:MultipleString">"""

    assert test1 in tmx_res
    assert test2 in tmx_res
    assert test3 in tmx_res

    test4 = """<prop type="x-filename:MultipleString">some file name.tmx</prop>"""
    assert test4 in tmx_res

    test5 = 'some file name.tmx'
    assert test5 in tmx_res
