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
from xmltodict import parse, unparse


def modify_qgs(template, input):

    document_file = open(template)
    original_doc = document_file.read()
    document_file.close()

    original_doc.replace('source="/home/dgketchum/IrrigationGIS/tests/qgis/LC08_041027_20150807',
                         '')

    output = os.path.join(input, '{}_calbration_map.qgs'.format(os.path.basename(input)))
    new_data = unparse(qgs)
    with open(output, 'w') as f:
        f.write(new_data)


if __name__ == '__main__':
    home = os.path.expanduser('~')
    path = os.path.join(home, 'IrrigationGIS', 'tests', 'qgis')
    t = os.path.join(path, 'qgs_template.qgs')
    targets = []
    for r, d, f in os.walk(path):
        if 'ETRF' in d:
            targets.append(r)
            print(r, d, f)
            modify_qgs(t, r)

# ========================= EOF ====================================================================
