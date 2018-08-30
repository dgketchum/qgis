# ===============================================================================
# Copyright 2018 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import os
from lxml import etree
import nose

print "=================================="
print "lxml version: ", etree.__version__
print "=================================="


def test_html():
    html_str = """
    <td><a href=''>a1</a></td>
    <td><a href=''>a2</a></td>
    """
    doc = etree.HTML(html_str.strip())
    elms = doc.xpath("//a[1]")
    assert len(elms) == 2, """xpath `//a[1]` shall return 2 elements"""
    assert all(elm.tag == "a" for elm in elms), "all returned elements shall be `a`"
    assert elms[0].text == "a1"
    assert elms[1].text == "a2"


def test_xml():
    xml_str = """
    <root>
        <td><a href=''>a1</a></td>
        <td><a href=''>a2</a></td>
    </root>
    """
    doc = etree.fromstring(xml_str.strip())
    elms = doc.xpath("//a[1]")
    assert len(elms) == 2, """xpath `//a[1]` shall return 2 elements"""
    assert all(elm.tag == "a" for elm in elms), "all returned elements shall be `a`"
    assert elms[0].text == "a1"
    assert elms[1].text == "a2"


nose.main()
if __name__ == '__main__':
    pass
# ========================= EOF ====================================================================
