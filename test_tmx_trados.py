"""Provide tests for tmx-tradosizer."""
from to_tmx import tmx_tradosizer


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
    test3 = """<prop type="x-filename:SingleString">"""

    assert test1 in tmx_res
    assert test2 in tmx_res
    assert test3 in tmx_res

    test4 = """<prop type="x-filename:SingleString">some file name.tmx</prop>"""
    assert test4 in tmx_res

    test5 = 'some file name.tmx'
    assert test5 in tmx_res
