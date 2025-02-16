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

_module_name = "sdfr"

from .SDF import read
from .sdf_helper import *
from .loadlib import (
    __library_commit_date__,
    __library_commit_id__,
    #__build_date__,
)

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(_module_name)
except PackageNotFoundError:
    __version__ = "2.6.12"

__all__ = [
    "SDF",
    "__library_commit_date__",
    "__library_commit_id__",
    "__version__",
    #"__build_date__",
]
