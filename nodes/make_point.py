# -*- coding: utf-8 -*-
###################################################################################
#
#  make_sphere.py
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
from FreeCAD import Vector
import Part

from fcn_conf import register_node
from fcn_base_node import FCNNode
from fcn_locator import icon
from fcn_utils import flatten_to_vectors


@register_node
class MakePoint(FCNNode):

    icon: str = icon("fcn_default.png")
    op_title: str = "Make Point"
    op_category = "FreeCAD"
    content_label_objname: str = "fcn_node_bg"

    def __init__(self, scene):
        super().__init__(scene=scene,
                         inputs_init_list=[(1, "Pos", 0, 0, True, ("int", "float"))],
                         outputs_init_list=[(5, "Shp", 0, 0, True, ("Shape", ))],
                         width=150)

    def eval_operation(self, sockets_input_data: list) -> list:
        position_list: list = sockets_input_data[0]

        vertex_list = []
        vector_pos_list = flatten_to_vectors(position_list)

        for vec in vector_pos_list:
            vertex = Part.Point(Vector(vec)).toShape()
            vertex_list.append(vertex)

        return [vertex_list]
