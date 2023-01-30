import pytest
from kanon.calendars import Calendar, Date
from kanon.units import Sexagesimal

from kanon_api.core.ephemerides.ascendant import ascendant
from kanon_api.core.ephemerides.houses import HouseMethods
from kanon_api.core.ephemerides.table_classes import (
    Jupiter,
    Mars,
    Mercury,
    Saturn,
    Venus,
)
from kanon_api.core.ephemerides.tables import TableSets
from kanon_api.core.ephemerides.true_position import (
    moon_true_pos,
    planet_true_pos,
    sun_true_pos,
)
from kanon_api.units import degree

julian_calendar = Calendar.registry["Julian A.D."]


@pytest.mark.parametrize(
    "ts, ymd, result",
    [
        (TableSets.parisian_alphonsine_tables, (1327, 7, 3), "01,48 ; 37,55"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), "05,18 ; 09,54"),
        (TableSets.toledan_tables, (1327, 7, 3), "13 ; 35,23"),
        (TableSets.toledan_tables, (10, 2, 13), "04,07 ; 42,54"),
    ],
)
def test_true_sun(ts, ymd, result):
    date = Date(julian_calendar, ymd)

    res = sun_true_pos(ts, date.days_from_epoch())
    assert round(res.value, 2) == Sexagesimal(result)


@pytest.mark.parametrize(
    "ts, ymd, result",
    [
        (TableSets.parisian_alphonsine_tables, (1327, 7, 3), "4,19;35,55"),
        (TableSets.parisian_alphonsine_tables, (1403, 3, 12), "3,28;15,28"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), "01,14 ; 42,27"),
        (TableSets.parisian_alphonsine_tables, (1327, 7, 11), "5,57 ; 18,24"),
        # ERROR: astropy.units.core.UnitConversionError
        # (TableSets.toledan_tables, (1327, 7, 3), "4,19;35,55"),
        # (TableSets.toledan_tables, (1403, 3, 12), "3,28;15,28"),
        # (TableSets.toledan_tables, (10, 2, 13), "01,14 ; 42,27"),
        # (TableSets.toledan_tables, (1327, 7, 11), "5,57 ; 18,24"),
    ],
)
def test_true_moon(ts, ymd, result):
    date = Date(julian_calendar, ymd)

    res = moon_true_pos(ts, date.days_from_epoch())
    assert round(res.value, 2) == Sexagesimal(result)


@pytest.mark.parametrize(
    "planet, ymd, result",
    [
        (TableSets.parisian_alphonsine_tables(Mars), (1327, 7, 3), "2,14;52,23"),
        (TableSets.parisian_alphonsine_tables(Mars), (10, 2, 13), "05,40 ; 42,26"),
        (TableSets.parisian_alphonsine_tables(Saturn), (1327, 7, 3), "1,47;5,1"),
        (TableSets.parisian_alphonsine_tables(Jupiter), (1327, 7, 3), "2,14;35,29"),
        (TableSets.parisian_alphonsine_tables(Mercury), (1327, 7, 3), "2,13;5,1"),
        (TableSets.parisian_alphonsine_tables(Venus), (1327, 7, 3), "2,1;27,13"),
        (TableSets.parisian_alphonsine_tables(Venus), (7, 2, 23), "01 ; 07,13"),
        (TableSets.parisian_alphonsine_tables(Mercury), (7, 3, 26), "05,38 ; 38,43"),
        # ERROR: AttributeError: '<Planet>' object has no attribute 'min_prop'
        # (TableSets.toledan_tables(Mars), (1327, 7, 3), "2,14;52,23"),
        # (TableSets.toledan_tables(Mars), (10, 2, 13), "05,40 ; 42,26"),
        # (TableSets.toledan_tables(Saturn), (1327, 7, 3), "1,47;5,1"),
        # (TableSets.toledan_tables(Jupiter), (1327, 7, 3), "2,14;35,29"),
        # (TableSets.toledan_tables(Mercury), (7, 3, 26), "05,38 ; 38,43"),
        # (TableSets.toledan_tables(Mercury), (1327, 7, 3), "2,13;5,1"),
        # (TableSets.toledan_tables(Venus), (7, 2, 23), "01 ; 07,13"),
        # (TableSets.toledan_tables(Venus), (1327, 7, 3), "2,1;27,13"),
    ],
)
def test_planet_true_pos(planet, ymd, result):
    date = Date(julian_calendar, ymd)

    res = planet_true_pos(date.days_from_epoch(), planet)
    assert round(res.value, 2) == Sexagesimal(result)


@pytest.mark.parametrize(
    "ts, date, hours, latitude, result",
    [
        (TableSets.parisian_alphonsine_tables, (1327, 7, 3), 0.5, 31, "03,17 ; 23,48"),
        (TableSets.parisian_alphonsine_tables, (1327, 7, 3), 0.6, 31, "03,47 ; 46,58"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), 0.5, 43, "01,15 ; 04,33"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), 0.5, 30, "01,06 ; 00,53"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), 0.5, 10, "58 ; 58,47"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), 0.5, 49, "01,20 ; 23,13"),
        (TableSets.parisian_alphonsine_tables, (10, 2, 13), 0.5, 48, "01,20 ; 23,13"),
        (TableSets.toledan_tables, (1327, 7, 3), 0.5, 31, "01,54 ; 23,19"),
        (TableSets.toledan_tables, (1327, 7, 3), 0.6, 31, "02,24 ; 32,18"),
        (TableSets.toledan_tables, (10, 2, 13), 0.5, 43, "05,18 ; 31,15"),
        (TableSets.toledan_tables, (10, 2, 13), 0.5, 30, "05,25 ; 43,00"),
        (TableSets.toledan_tables, (10, 2, 13), 0.5, 10, "05,30 ; 27,47"),
        (TableSets.toledan_tables, (10, 2, 13), 0.5, 49, "05,13 ; 24,05"),
        (TableSets.toledan_tables, (10, 2, 13), 0.5, 48, "05,13 ; 24,05"),
    ],
)
def test_ascendant(ts, date, hours, latitude, result):
    degree_ascension = ascendant(
        ts, Date(julian_calendar, date, hours * 24).days_from_epoch(), latitude
    )

    assert round(Sexagesimal(degree_ascension.value, 2), 2) == Sexagesimal(result)


@pytest.mark.parametrize(
    "ts, method, result2, result8",
    [
        (
            TableSets.parisian_alphonsine_tables,
            HouseMethods.M1,
            "05,03 ; 23",
            "02,03 ; 23",
        ),
        (
            TableSets.parisian_alphonsine_tables,
            HouseMethods.M2,
            "05,05 ; 27",
            "02,05 ; 27",
        ),
        (
            TableSets.parisian_alphonsine_tables,
            HouseMethods.M5,
            "04,52 ; 29",
            "01,52 ; 29",
        ),
        (
            TableSets.parisian_alphonsine_tables,
            HouseMethods.M6,
            "04,56 ; 38",
            "01,56 ; 38",
        ),
        (
            TableSets.toledan_tables,
            HouseMethods.M1,
            "05,03 ; 23",
            "02,03 ; 23",
        ),
        (
            TableSets.toledan_tables,
            HouseMethods.M2,
            "05,05 ; 27",
            "02,05 ; 27",
        ),
        (
            TableSets.toledan_tables,
            HouseMethods.M5,
            "04,52 ; 29",
            "01,52 ; 29",
        ),
        (
            TableSets.toledan_tables,
            HouseMethods.M6,
            "04,56 ; 38",
            "01,56 ; 38",
        ),
    ],
)
def test_houses(ts, method: HouseMethods, result2, result8):
    asc = 236 + Sexagesimal("0;38")
    houses = method(ts, asc * degree, float(Sexagesimal("39;51")))
    assert len(houses) == 12
    assert round(Sexagesimal(houses[2], 1)) == Sexagesimal(result2)
    assert round(Sexagesimal(houses[8], 1)) == Sexagesimal(result8)
