"""Tests for distance conflict detection used by generate_bom."""

from src.agents.tools.utils.distance_utils import (
    extract_distances_meters,
    find_distance_conflict,
    format_meters,
    is_multivalue_or_fuzzy,
)


def test_extract_basic_units():
    assert extract_distances_meters("120km DDM") == {120000.0}
    assert extract_distances_meters("khoảng cách 40km") == {40000.0}
    assert extract_distances_meters("300m") == {300.0}
    assert extract_distances_meters("0.5km") == {500.0}
    assert extract_distances_meters("3M") == {3.0}
    assert extract_distances_meters("no distance here") == set()


def test_the_real_incident_is_caught():
    # Agent asked for 120km in notes but resolved a 40km SKU.
    notes = "1000BASE-BX-U, 1550nm TX / 1490nm RX, LC, 120km DDM, single fiber"
    conflict = find_distance_conflict(notes, "40km")
    assert conflict is not None
    req, sku = conflict
    assert format_meters(req) == "120km"
    assert format_meters(sku) == "40km"


def test_matching_distance_is_not_a_conflict():
    notes = "1000BASE-BX-D, Tx1490nm/Rx1550nm, LC, 120km DDM, single fiber"
    assert find_distance_conflict(notes, "120km") is None


def test_tolerates_spacing_and_case():
    assert find_distance_conflict("need 40 km reach", "40KM") is None
    assert find_distance_conflict("need 40 km reach", "80 km") is not None


def test_no_distance_in_request_is_not_a_conflict():
    assert find_distance_conflict("Juniper BiDi single fiber", "40km") is None


def test_fuzzy_sku_distance_is_skipped():
    # Multi-value / parametric / N/A distances must never trigger a block.
    assert is_multivalue_or_fuzzy("300m (OM3), 400m (OM4)")
    assert is_multivalue_or_fuzzy("L meters")
    assert is_multivalue_or_fuzzy("N/A")
    assert is_multivalue_or_fuzzy("")
    assert find_distance_conflict("need 10m patchcord", "L meters") is None
    assert find_distance_conflict("100G MPO 300m", "300m (OM3), 400m (OM4)") is None


def test_multivalue_request_is_skipped():
    # If the request text itself lists several distances, stay conservative.
    assert find_distance_conflict("10km or 40km options", "40km") is None



def test_conflict_still_detected_for_wrong_variant():
    # The pure conflict detector still flags a clear mismatch; the decision to
    # block vs allow (based on whether a closer catalog variant exists) is made
    # in generate_bom._find_distance_mismatch, which is covered by integration
    # tests against the real catalog.
    assert find_distance_conflict("LC, 120km DDM", "40km") is not None
    assert find_distance_conflict("SFP+ 120km 10GE", "80km") is not None
