#!/usr/bin/env python
# coding: utf-8

# Copyright 2022 University of Warwick, University of York
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ctypes as ct
import numpy as np
from enum import IntEnum
from .loadlib import sdf_lib

#try:
#    import xarray as xr
#
#    got_xarray = True
#except ImportError:
#    print("WARNING: xarray not installed. Generating plain numpy arrays.")
#    got_xarray = False


# Enum representation using ct
class SdfBlockType(IntEnum):
    SDF_BLOCKTYPE_SCRUBBED = -1
    SDF_BLOCKTYPE_NULL = 0
    SDF_BLOCKTYPE_PLAIN_MESH = 1
    SDF_BLOCKTYPE_POINT_MESH = 2
    SDF_BLOCKTYPE_PLAIN_VARIABLE = 3
    SDF_BLOCKTYPE_POINT_VARIABLE = 4
    SDF_BLOCKTYPE_CONSTANT = 5
    SDF_BLOCKTYPE_ARRAY = 6
    SDF_BLOCKTYPE_RUN_INFO = 7
    SDF_BLOCKTYPE_SOURCE = 8
    SDF_BLOCKTYPE_STITCHED_TENSOR = 9
    SDF_BLOCKTYPE_STITCHED_MATERIAL = 10
    SDF_BLOCKTYPE_STITCHED_MATVAR = 11
    SDF_BLOCKTYPE_STITCHED_SPECIES = 12
    SDF_BLOCKTYPE_SPECIES = 13
    SDF_BLOCKTYPE_PLAIN_DERIVED = 14
    SDF_BLOCKTYPE_POINT_DERIVED = 15
    SDF_BLOCKTYPE_CONTIGUOUS_TENSOR = 16
    SDF_BLOCKTYPE_CONTIGUOUS_MATERIAL = 17
    SDF_BLOCKTYPE_CONTIGUOUS_MATVAR = 18
    SDF_BLOCKTYPE_CONTIGUOUS_SPECIES = 19
    SDF_BLOCKTYPE_CPU_SPLIT = 20
    SDF_BLOCKTYPE_STITCHED_OBSTACLE_GROUP = 21
    SDF_BLOCKTYPE_UNSTRUCTURED_MESH = 22
    SDF_BLOCKTYPE_STITCHED = 23
    SDF_BLOCKTYPE_CONTIGUOUS = 24
    SDF_BLOCKTYPE_LAGRANGIAN_MESH = 25
    SDF_BLOCKTYPE_STATION = 26
    SDF_BLOCKTYPE_STATION_DERIVED = 27
    SDF_BLOCKTYPE_DATABLOCK = 28
    SDF_BLOCKTYPE_NAMEVALUE = 29

class SdfGeometry(IntEnum):
    SDF_GEOMETRY_NULL = 0
    SDF_GEOMETRY_CARTESIAN = 1
    SDF_GEOMETRY_CYLINDRICAL = 2
    SDF_GEOMETRY_SPHERICAL = 3

class SdfStagger(IntEnum):
    SDF_STAGGER_CELL_CENTRE = 0
    SDF_STAGGER_FACE_X = 1
    SDF_STAGGER_FACE_Y = 2
    SDF_STAGGER_FACE_Z = 3
    SDF_STAGGER_EDGE_X = 4
    SDF_STAGGER_EDGE_Y = 5
    SDF_STAGGER_EDGE_Z = 6
    SDF_STAGGER_VERTEX = 7

class SdfDataType(IntEnum):
    SDF_DATATYPE_NULL = 0
    SDF_DATATYPE_INTEGER4 = 1
    SDF_DATATYPE_INTEGER8 = 2
    SDF_DATATYPE_REAL4 = 3
    SDF_DATATYPE_REAL8 = 4
    SDF_DATATYPE_REAL16 = 5
    SDF_DATATYPE_CHARACTER = 6
    SDF_DATATYPE_LOGICAL = 7
    SDF_DATATYPE_OTHER = 8

_np_datatypes = [0, np.int32, np.int64, np.float32, np.float64, \
                 np.longdouble, np.byte, np.int32, bool, 0]
_ct_datatypes = [0, ct.c_int32, ct.c_int64, ct.c_float, ct.c_double, \
                 ct.c_longdouble, ct.c_char, ct.c_bool, 0]

# Constants
SDF_READ = 1
SDF_WRITE = 2
SDF_MAXDIMS = 4

class SdfBlock(ct.Structure):
    pass  # Forward declaration for self-referencing structure

class SdfFile(ct.Structure):
    pass  # Forward declaration for function pointer compatibility

SdfBlock._fields_ = [
    ("extents", ct.POINTER(ct.c_double)),
    ("dim_mults", ct.POINTER(ct.c_double)),
    ("station_x", ct.POINTER(ct.c_double)),
    ("station_y", ct.POINTER(ct.c_double)),
    ("station_z", ct.POINTER(ct.c_double)),
    ("mult", ct.c_double),
    ("time", ct.c_double),
    ("time_increment", ct.c_double),
    ("dims", ct.c_int64 * SDF_MAXDIMS),
    ("local_dims", ct.c_int64 * SDF_MAXDIMS),
    ("block_start", ct.c_int64),
    ("next_block_location", ct.c_int64),
    ("data_location", ct.c_int64),
    ("inline_block_start", ct.c_int64),
    ("inline_next_block_location", ct.c_int64),
    ("summary_block_start", ct.c_int64),
    ("summary_next_block_location", ct.c_int64),
    ("nelements", ct.c_int64),
    ("nelements_local", ct.c_int64),
    ("data_length", ct.c_int64),
    ("nelements_blocks", ct.POINTER(ct.c_int64)),
    ("data_length_blocks", ct.POINTER(ct.c_int64)),
    ("array_starts", ct.POINTER(ct.c_int64)),
    ("array_ends", ct.POINTER(ct.c_int64)),
    ("array_strides", ct.POINTER(ct.c_int64)),
    ("global_array_starts", ct.POINTER(ct.c_int64)),
    ("global_array_ends", ct.POINTER(ct.c_int64)),
    ("global_array_strides", ct.POINTER(ct.c_int64)),
    ("ndims", ct.c_int32),
    ("geometry", ct.c_int32),
    ("datatype", ct.c_int32),
    ("blocktype", ct.c_int32),
    ("info_length", ct.c_int32),
    ("type_size", ct.c_int32),
    ("stagger", ct.c_int32),
    ("datatype_out", ct.c_int32),
    ("type_size_out", ct.c_int32),
    ("nstations", ct.c_int32),
    ("nvariables", ct.c_int32),
    ("step", ct.c_int32),
    ("step_increment", ct.c_int32),
    ("dims_in", ct.POINTER(ct.c_int32)),
    ("station_nvars", ct.POINTER(ct.c_int32)),
    ("variable_types", ct.POINTER(ct.c_int32)),
    ("station_index", ct.POINTER(ct.c_int32)),
    ("station_move", ct.POINTER(ct.c_int32)),
    ("nm", ct.c_int),
    ("n_ids", ct.c_int),
    ("opt", ct.c_int),
    ("ng", ct.c_int),
    ("nfaces", ct.c_int),
    ("ngrids", ct.c_int),
    ("offset", ct.c_int),
    ("ngb", ct.c_int * 6),
    ("const_value", ct.c_char * 16),
    ("id", ct.c_char_p),
    ("units", ct.c_char_p),
    ("mesh_id", ct.c_char_p),
    ("material_id", ct.c_char_p),
    ("vfm_id", ct.c_char_p),
    ("obstacle_id", ct.c_char_p),
    ("station_id", ct.c_char_p),
    ("name", ct.c_char_p),
    ("material_name", ct.c_char_p),
    ("must_read", ct.c_char_p),
    ("dim_labels", ct.POINTER(ct.c_char_p)),
    ("dim_units", ct.POINTER(ct.c_char_p)),
    ("station_ids", ct.POINTER(ct.c_char_p)),
    ("variable_ids", ct.POINTER(ct.c_char_p)),
    ("station_names", ct.POINTER(ct.c_char_p)),
    ("material_names", ct.POINTER(ct.c_char_p)),
    ("node_list", ct.POINTER(ct.c_int)),
    ("boundary_cells", ct.POINTER(ct.c_int)),
    ("grids", ct.POINTER(ct.c_void_p)),
    ("data", ct.c_void_p),
    ("done_header", ct.c_bool),
    ("done_info", ct.c_bool),
    ("done_data", ct.c_bool),
    ("dont_allocate", ct.c_bool),
    ("dont_display", ct.c_bool),
    ("dont_own_data", ct.c_bool),
    ("use_mult", ct.c_bool),
    ("next_block_modified", ct.c_bool),
    ("rewrite_metadata", ct.c_bool),
    ("in_file", ct.c_bool),
    ("ng_any", ct.c_bool),
    ("no_internal_ghost", ct.c_bool),
    ("next", ct.POINTER(SdfBlock)),
    ("prev", ct.POINTER(SdfBlock)),
    ("subblock", ct.POINTER(SdfBlock)),
    ("subblock2", ct.POINTER(SdfBlock)),
    ("populate_data", ct.CFUNCTYPE(ct.POINTER(SdfBlock), ct.POINTER(SdfFile), ct.POINTER(SdfBlock))),
    ("cpu_split", ct.c_int * SDF_MAXDIMS),
    ("starts", ct.c_int * SDF_MAXDIMS),
    ("proc_min", ct.c_int * 3),
    ("proc_max", ct.c_int * 3),
    ("ndim_labels", ct.c_int),
    ("ndim_units", ct.c_int),
    ("nstation_ids", ct.c_int),
    ("nvariable_ids", ct.c_int),
    ("nstation_names", ct.c_int),
    ("nmaterial_names", ct.c_int),
    ("option", ct.c_int),
    ("mimetype", ct.c_char_p),
    ("checksum_type", ct.c_char_p),
    ("checksum", ct.c_char_p),
    ("mmap", ct.c_char_p),
    ("mmap_len", ct.c_int64),
    ("derived", ct.c_bool),
]

SdfFile._fields_ = [
    ("dbg_count", ct.c_int64),
    ("sdf_lib_version", ct.c_int32),
    ("sdf_lib_revision", ct.c_int32),
    ("sdf_extension_version", ct.c_int32),
    ("sdf_extension_revision", ct.c_int32),
    ("file_version", ct.c_int32),
    ("file_revision", ct.c_int32),
    ("dbg", ct.c_char_p),
    ("dbg_buf", ct.c_char_p),
    ("extension_names", ct.POINTER(ct.c_char_p)),
    ("time", ct.c_double),
    ("first_block_location", ct.c_int64),
    ("summary_location", ct.c_int64),
    ("start_location", ct.c_int64),
    ("soi", ct.c_int64),
    ("sof", ct.c_int64),
    ("current_location", ct.c_int64),
    ("jobid1", ct.c_int32),
    ("jobid2", ct.c_int32),
    ("endianness", ct.c_int32),
    ("summary_size", ct.c_int32),
    ("block_header_length", ct.c_int32),
    ("string_length", ct.c_int32),
    ("id_length", ct.c_int32),
    ("code_io_version", ct.c_int32),
    ("step", ct.c_int32),
    ("nblocks", ct.c_int32),
    ("nblocks_file", ct.c_int32),
    ("error_code", ct.c_int32),
    ("rank", ct.c_int),
    ("ncpus", ct.c_int),
    ("ndomains", ct.c_int),
    ("rank_master", ct.c_int),
    ("indent", ct.c_int),
    ("print", ct.c_int),
    ("buffer", ct.c_char_p),
    ("filename", ct.c_char_p),
    ("done_header", ct.c_bool),
    ("restart_flag", ct.c_bool),
    ("other_domains", ct.c_bool),
    ("use_float", ct.c_bool),
    ("use_summary", ct.c_bool),
    ("use_random", ct.c_bool),
    ("station_file", ct.c_bool),
    ("swap", ct.c_bool),
    ("inline_metadata_read", ct.c_bool),
    ("summary_metadata_read", ct.c_bool),
    ("inline_metadata_invalid", ct.c_bool),
    ("summary_metadata_invalid", ct.c_bool),
    ("tmp_flag", ct.c_bool),
    ("metadata_modified", ct.c_bool),
    ("can_truncate", ct.c_bool),
    ("first_block_modified", ct.c_bool),
    ("code_name", ct.c_char_p),
    ("error_message", ct.c_char_p),
    ("blocklist", ct.POINTER(SdfBlock)),
    ("tail", ct.POINTER(SdfBlock)),
    ("current_block", ct.POINTER(SdfBlock)),
    ("last_block_in_file", ct.POINTER(SdfBlock)),
    ("mmap", ct.c_char_p),
    ("ext_data", ct.c_void_p),
    ("stack_handle", ct.c_void_p),
    ("array_count", ct.c_int),
    ("fd", ct.c_int),
    ("purge_duplicated_ids", ct.c_int),
    ("internal_ghost_cells", ct.c_int),
    ("ignore_nblocks", ct.c_int)
]

class RunInfo(ct.Structure):
    _fields_ = [
        ("defines", ct.c_int64),
        ("version", ct.c_int32),
        ("revision", ct.c_int32),
        ("compile_date", ct.c_int32),
        ("run_date", ct.c_int32),
        ("io_date", ct.c_int32),
        ("minor_rev", ct.c_int32),
        ("commit_id", ct.c_char_p),
        ("sha1sum", ct.c_char_p),
        ("compile_machine", ct.c_char_p),
        ("compile_flags", ct.c_char_p),
    ]


class BlockList:
    """Contains all the blocks"""
    def __init__(self, filename, convert=False, derived=True):
        clib = sdf_lib
        self._clib = clib
        clib.sdf_open.restype = ct.POINTER(SdfFile)
        #clib.sdf_open.restype = ct.c_void_p
        clib.sdf_open.argtypes = [ct.c_char_p, ct.c_int, ct.c_int, ct.c_int]
        clib.sdf_stack_init.argtypes = [ct.c_void_p]
        #clib.sdf_read_blocklist.argtypes = [ct.POINTER(SdfFile)]
        clib.sdf_read_blocklist.argtypes = [ct.c_void_p]
        clib.sdf_read_blocklist_all.argtypes = [ct.c_void_p]
        clib.sdf_helper_read_data.argtypes = [ct.c_void_p, ct.POINTER(SdfBlock)]
        clib.sdf_free_block_data.argtypes = [ct.c_void_p, ct.POINTER(SdfBlock)]

        h = clib.sdf_open(filename.encode("utf-8"), 0, 1, 0)
        if h is None or not bool(h):
            raise Exception(f"Failed to open file: '{filename}'")

        if convert:
            h.contents.use_float = True

        h._clib = clib
        self._handle = h
        clib.sdf_stack_init(h)
        if derived:
            clib.sdf_read_blocklist_all(h)
        else:
            clib.sdf_read_blocklist(h)


        block = h.contents.blocklist
        meshes = []
        mesh_vars = []
        for n in range(h.contents.nblocks):
            block = block.contents
            block._handle = h
            blocktype = block.blocktype
            name = get_member_name(block.name)
            if blocktype == SdfBlockType.SDF_BLOCKTYPE_RUN_INFO:
                self.Run_info = get_run_info(block)
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_CONSTANT:
                self.__dict__[name] = BlockConstant(block)
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_PLAIN_VARIABLE:
                self.__dict__[name] = BlockPlainVariable(block)
                mesh_vars.append(self.__dict__[name])
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_POINT_VARIABLE:
                self.__dict__[name] = BlockPointVariable(block)
                mesh_vars.append(self.__dict__[name])
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_PLAIN_MESH:
                self.__dict__[name] = BlockPlainMesh(block)
                meshes.append(self.__dict__[name])
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_POINT_MESH:
                self.__dict__[name] = BlockPointMesh(block)
                meshes.append(self.__dict__[name])
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_NAMEVALUE:
                self.__dict__[name] = BlockNameValue(block)
            elif blocktype == SdfBlockType.SDF_BLOCKTYPE_ARRAY:
                self.__dict__[name] = BlockArray(block)
            #else:
            #    print(name,SdfBlockType(blocktype).name)
            block = block.next

        for var in mesh_vars:
            gid = var.grid_id
            for mesh in meshes:
                if mesh.id == gid:
                    var._grid = mesh
                    break

    def __del__(self):
        self._clib.sdf_stack_destroy.argtypes = [ct.c_void_p]
        self._clib.sdf_close.argtypes = [ct.c_void_p]
        self._clib.sdf_stack_destroy(self._handle)
        self._clib.sdf_close(self._handle)


class Block:
    """SDF block type
    Contains the data and metadata for a single
    block from an SDF file.
    """
    def __init__(self, block):
        self._handle = block._handle
        self._id = block.id.decode()
        self._name = block.name.decode()
        self._datatype = _np_datatypes[block.datatype_out]
        self._data_length = block.data_length
        self._dims = tuple(block.dims[:block.ndims])
        self._contents = block
        self._owndata = True

    def __del__(self):
        if not self._owndata and self._data is not None:
            clib = self._handle._clib
            clib.sdf_free_block_data(self._handle, self._contents)

    def _numpy_from_buffer(self, data, blen):
        buffer_from_memory = ct.pythonapi.PyMemoryView_FromMemory
        buffer_from_memory.restype = ct.py_object
        dtype = self._datatype
        if dtype == np.byte:
            dtype = np.dtype('|S1')
        totype = _ct_datatypes[self._contents.datatype]
        cast = ct.cast(data, ct.POINTER(totype))
        buf = buffer_from_memory(cast, blen)
        self._owndata = False
        return np.frombuffer(buf, dtype)

    @property
    def data(self):
        """Block data contents"""
        return self._data

    @property
    def datatype(self):
        """Data type"""
        return self._datatype

    @property
    def data_length(self):
        """Data size"""
        return self._data_length

    @property
    def dims(self):
        """Data dimensions"""
        return self._dims

    @property
    def id(self):
        """Block id"""
        return self._id

    @property
    def name(self):
        """Block name"""
        return self._name



class BlockConstant(Block):
    """Constant block class"""
    def __init__(self, block):
        super().__init__(block)
        offset = getattr(SdfBlock, 'const_value').offset
        self._datatype = _np_datatypes[block.datatype]
        totype = _ct_datatypes[block.datatype]
        self._data = totype.from_buffer(block, offset).value


class BlockPlainVariable(Block):
    def __init__(self, block):
        super().__init__(block)
        self._data = None

    @property
    def data(self):
        """Block data contents"""
        if self._data is None:
            clib = self._handle._clib
            clib.sdf_helper_read_data(self._handle, self._contents)
            blen = np.dtype(self._datatype).itemsize
            for d in self.dims:
                blen *= d
            array = self._numpy_from_buffer(self._contents.data, blen)
            self._data = array.reshape(self.dims, order='F')
        return self._data

    @property
    def grid(self):
        """Associated mesh"""
        return self._grid

    @property
    def grid_id(self):
        """Associated mesh id"""
        return self._contents.mesh_id.decode()

    @property
    def mult(self):
        """Multiplication factor"""
        return self._contents.mult

    @property
    def stagger(self):
        """Grid stagger"""
        return SdfStagger(self._contents.stagger)

    @property
    def units(self):
        """Units of variable"""
        return self._contents.units.decode()


class BlockPlainMesh(Block):
    def __init__(self, block):
        super().__init__(block)
        self._data = None
        self._units = tuple([block.dim_units[i].decode() for i in range(block.ndims)])
        self._labels = tuple([block.dim_labels[i].decode() for i in range(block.ndims)])
        self._mult = None
        if bool(block.dim_mults):
            self._mult = tuple(block.dim_mults[:block.ndims])
        self._extents = tuple(block.extents[:2*block.ndims])

    @property
    def data(self):
        """Block data contents"""
        if self._data is None:
            clib = self._handle._clib
            clib.sdf_helper_read_data(self._handle, self._contents)
            grids = []
            for i, d in enumerate(self.dims):
                blen = np.dtype(self._datatype).itemsize * d
                array = self._numpy_from_buffer(self._contents.grids[i], blen)
                grids.append(array)
            self._data = tuple(grids)
        return self._data

    @property
    def extents(self):
        """Axis extents"""
        return self._extents

    @property
    def geometry(self):
        """Domain geometry"""
        return SdfGeometry(self._contents.geometry)

    @property
    def labels(self):
        """Axis labels"""
        return self._labels

    @property
    def mult(self):
        """Multiplication factor"""
        return self._mult

    @property
    def units(self):
        """Units of variable"""
        return self._units


class BlockPointMesh(BlockPlainMesh):
    def __init__(self, block):
        super().__init__(block)

    @property
    def species_id(self):
        """Species ID"""
        return self._contents.material_id.decode()


class BlockPointVariable(BlockPlainVariable):
    def __init__(self, block):
        super().__init__(block)

    @property
    def species_id(self):
        """Species ID"""
        return self._contents.material_id.decode()


class BlockNameValue(Block):
    def __init__(self, block):
        super().__init__(block)
        self._dims = (block.ndims,)
        vals = {}
        for n in range(block.ndims):
            val = None
            if block.datatype == SdfDataType.SDF_DATATYPE_CHARACTER:
                p = ct.cast(block.data, ct.POINTER(ct.c_char_p))
                val = p[n].decode()
            else:
                dt = _ct_datatypes[block.datatype]
                val = ct.cast(block.data, ct.POINTER(dt))[n]
            nid = get_member_name(block.material_names[n])
            vals[nid] = val
            self.__dict__[nid] = val
        self._data = vals


class BlockArray(Block):
    def __init__(self, block):
        super().__init__(block)
        self._data = None

    @property
    def data(self):
        """Block data contents"""
        if self._data is None:
            clib = self._handle._clib
            clib.sdf_helper_read_data(self._handle, self._contents)
            blen = np.dtype(self._datatype).itemsize
            for d in self.dims:
                blen *= d
            array = self._numpy_from_buffer(self._contents.data, blen)
            self._data = array.reshape(self.dims, order='F')
        return self._data


def get_run_info(block):
    from datetime import datetime
    r = ct.cast(block.data, ct.POINTER(RunInfo)).contents
    ri = {}
    ri['version'] = f"{r.version}.{r.revision}.{r.minor_rev}"
    ri['commit_id'] = r.commit_id.decode()
    ri['sha1sum'] = r.sha1sum.decode()
    ri['compile_machine'] = r.compile_machine.decode()
    ri['compile_flags'] = r.compile_flags.decode()
    ri['compile_date'] = datetime.utcfromtimestamp(r.compile_date).strftime('%c')
    ri['run_date'] = datetime.utcfromtimestamp(r.run_date).strftime('%c')
    ri['io_data'] = datetime.utcfromtimestamp(r.io_date).strftime('%c')
    return ri

def get_member_name(name):
    sname = name.decode()
    return ''.join([i if ((i >= "a" and i <= "z") or (i >= "A" and i <= "Z") \
                    or (i >= "0" and i <= "9")) else "_" \
                    for i in sname])

def read(filename, convert=False, derived=True):
    """Reads the SDF data and returns a dictionary of NumPy arrays.

    Parameters
    ----------
    filename : string
        The name of the SDF file to open.
    convert : bool, optional
        Convert double precision data to single when reading file.
    derived : bool, optional
        Include derived variables in the data structure.
    """

    return BlockList(filename, convert, derived)
