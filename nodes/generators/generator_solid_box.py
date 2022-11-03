# -*- coding: utf-8 -*-
###################################################################################
#
#  generator_solid_box.py
#
#  Copyright (c) 2022 Ronny Scharf-Wildenhain <ronny.scharf08@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###################################################################################
from typing import Union

from FreeCAD import Vector
import Part
import awkward as ak

from core.nodes_conf import register_node
from core.nodes_default_node import FCNNodeModel
from core.nodes_utils import simplify, flatten, map_objects

from nodes_locator import icon


@register_node
class SolidBox(FCNNodeModel):

    icon: str = icon("nodes_default.png")
    op_title: str = "Solid Box"
    op_category: str = "Generator"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[("Width", True,), ("Length", True), ("Height", True), ("Pos", True)],
                         outputs_init_list=[("Box", True)])

        self.grNode.resize(100, 125)
        for socket in self.inputs + self.outputs:
            socket.setSocketPosition()

        self.width_list: list = []
        self.length_list: list = []
        self.height_list: list = []

    def make_occ_box(self, position: Union[tuple, Vector]) -> Part.Shape:
        width, length, height = self.width_list.pop(0), self.length_list.pop(0), self.height_list.pop(0)
        if type(position) is tuple:
            return Part.makeBox(width, length, height, Vector(position))
        else:
            return Part.makeBox(width, length, height, position)

    def eval_operation(self, sockets_input_data: list) -> list:
        width: list = sockets_input_data[0] if len(sockets_input_data[0]) > 0 else [10]
        length: list = sockets_input_data[1] if len(sockets_input_data[1]) > 0 else [10]
        height: list = sockets_input_data[2] if len(sockets_input_data[2]) > 0 else [10]
        pos: list = sockets_input_data[3] if len(sockets_input_data[3]) > 0 else [(0, 0, 0)]

        # Force array broadcast
        pos_list: list = list(simplify(pos)) if type(pos) is tuple else flatten(pos)
        pos_idx_list: list = list(range(len(pos_list)))
        width, length, height, pos_idx_list = ak.broadcast_arrays(width, length, height, pos_idx_list)

        self.width_list = ak.flatten(width, axis=None).tolist()
        self.length_list = ak.flatten(length, axis=None).tolist()
        self.height_list = ak.flatten(height, axis=None).tolist()

        return [map_objects(pos, object, self.make_occ_box)]
