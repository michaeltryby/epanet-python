import os

import pytest
import numpy as np

from epanet.output import OutputMetadata
from epanet.output import output


DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
OUTPUT_FILE_EXAMPLE1 = os.path.join(DATA_PATH, 'net1.out')
OUTPUT_FILE_FAIL = os.path.join(DATA_PATH, 'nodata.out')


def test_create_delete():
    _handle = output.create_handle()
    output.delete_handle(_handle)

def test_open_close():
    _handle = output.create_handle()
    output.open_file(_handle, OUTPUT_FILE_EXAMPLE1)
    output.close_file(_handle)
    output.delete_handle(_handle)

def test_clear_check():
    _handle = output.create_handle()

    output.clear_error(_handle)
    output.open_file(_handle, OUTPUT_FILE_FAIL)
    message = output.check_error(_handle)

    output.delete_handle(_handle)


@pytest.fixture()
def handle(request):
    _handle = output.create_handle()
    output.open_file(_handle, OUTPUT_FILE_EXAMPLE1)

    def close():
        output.close_file(_handle)
        output.delete_handle(_handle)

    request.addfinalizer(close)
    return _handle


def test_output_metadata(handle):

    om = OutputMetadata(handle)

    ref = {
        output.NodeAttribute.DEMAND:      ("Demand",          "gal/min"),
        output.NodeAttribute.HEAD:        ("Head",            "ft"),
        output.NodeAttribute.PRESSURE:    ("Pressure",        "psi"),
        output.NodeAttribute.QUALITY:     ("Quality",         "mg/L"),

        output.LinkAttribute.FLOW:        ("Flow",            "gal/min"),
        output.LinkAttribute.VELOCITY:    ("Velocity",        "ft/sec"),
        output.LinkAttribute.HEADLOSS:    ("Unit Headloss",   "ft/1000ft"),
        output.LinkAttribute.AVG_QUALITY: ("Quality",         "mg/L"),
        output.LinkAttribute.STATUS:      ("Status",          ""),
        output.LinkAttribute.SETTING:     ("Setting",         ""),
        output.LinkAttribute.RX_RATE:     ("Reaction Rate",   "mg/hr"),
        output.LinkAttribute.FRCTN_FCTR:  ("Friction Factor", "unitless")}

    for attr in output.NodeAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]

    for attr in output.LinkAttribute:
        temp = om.get_attribute_metadata(attr)
        assert temp == ref[attr]


def test_getnetsize(handle):
    # node, tank, link, pump, valve
    ref_array = np.array([11, 2, 13, 1, 0])

    netsize_list = output.get_net_size(handle)
    assert len(netsize_list) == 5

    assert np.array_equal(netsize_list, ref_array)


def test_getelementname(handle):
    ref_index = 1
    ref_name = "10"

    name = output.get_elem_name(handle, output.ElementType.NODE, ref_index)
    assert name == ref_name


def test_getnodeSeries(handle):

    ref_array = np.array(
        [119.25731,
        120.45029,
        121.19854,
        122.00622,
        122.37414,
        122.8122,
        122.82034,
        122.90379,
        123.40434,
        123.81807])

    array = output.get_node_series(handle, 2, output.NodeAttribute.PRESSURE, 0, 10)
    assert len(array) == 10

    assert np.allclose(array, ref_array)


def test_getlinkseries(handle):
    pass

def test_getnodeattribute(handle):
    ref_array = np.array([ 1., 0.44407997, 0.43766347, 0.42827705, 0.41342604,
        0.42804748, 0.44152543, 0.40502965, 0.38635802, 1., 0.96745253])

    array = output.get_node_attribute(handle, 1, output.NodeAttribute.QUALITY)
    assert len(array) == 11
    assert np.allclose(array, ref_array)


def test_getlinkattribute(handle):
    ref_array = np.array([ 1848.58117676, 1220.42736816, 130.11161804,
        187.68930054, 119.88839722, 40.46448898, -748.58111572, 478.15377808,
        191.73458862, 30.11160851, 140.4644928, 59.53551483, 1848.58117676])

    array = output.get_link_attribute(handle, 1, output.LinkAttribute.FLOW)
    assert len(array) == 13
    assert np.allclose(array, ref_array)


def test_getnoderesult(handle):
    pass

def test_getlinkresult(handle):
    pass
