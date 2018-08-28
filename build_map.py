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
    existing_map = os.path.join(template, 'qgs_template.qgs')

    document_file = open(existing_map)
    original_doc = document_file.read()
    document_file.close()

    qgs = parse(original_doc)
    key = qgs['qgis']['layer-tree-group']['layer-tree-layer']

    sources = {'cold': os.path.join(input, 'PIXELS', 'cold.shp'),
               'hot': os.path.join(input, 'PIXELS', 'hot.shp'),
               'hot_pixel_suggestion': os.path.join(input, 'PIXEL_REGIONS',
                                                    'hot_pixel_suggestion.img'),
               'cold_pixel_suggestion': os.path.join(input, 'PIXEL_REGIONS',
                                                     'cold_pixel_suggestion.img'),
               'region_mask': os.path.join(input, 'PIXEL_REGIONS', 'region_mask.img'),
               'ndvi_toa': os.path.join(input, 'INDICES', 'ndvi_toa.img'),
               'ts': os.path.join(input, 'ts.img'),
               'albedo_at_sur': os.path.join(input, 'albedo_at_sur.img'),
               'et_rf': os.path.join(input, 'ETRF', 'et_rf.img')}

    for item in key:
        name = item['@name']
        path = sources[name]
        item['@source'] = path

    output = os.path.join(input, 'calbration_map.qgs')
    new_data = unparse(qgs)
    with open(output, 'w') as f:
        f.write(new_data)


if __name__ == '__main__':
    home = os.path.expanduser('~')
    path = os.path.join(home, 'IrrigationGIS', 'tests', 'qgis')
    dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    for d in dirs:
        modify_qgs(path, d)
# ========================= EOF ====================================================================
