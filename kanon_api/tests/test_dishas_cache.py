import importlib
import json
import pathlib
import shutil
import sys
from unittest import mock

from kanon_api import settings
from kanon_api.core.ephemerides.table_classes import TABLE_SET_DIRECTORY
from kanon_api.core.ephemerides.tables import TableSets

cache_dir = pathlib.Path("dishas_cache")


def test_dishas_cache():

    settings.PRODUCTION = True

    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    if "kanon_api.core.ephemerides.tables" in sys.modules:
        import kanon_api.core.ephemerides.tables

        importlib.reload(kanon_api.core.ephemerides.tables)

    import kanon_api.core.ephemerides.tables

    assert cache_dir.exists()

    cached_tables = []

    def get_int_leaves(tree):
        if isinstance(tree, dict):
            for value in tree.values():
                yield from get_int_leaves(value)
        elif isinstance(tree, int):
            yield tree

    for file in TableSets:
        data = json.loads((TABLE_SET_DIRECTORY / f"{file.value}.json").read_text())
        cached_tables.extend(get_int_leaves(data))

    files = list(cache_dir.glob("*"))

    assert len(files) > 0
    assert len(files) == len(set(cached_tables))

    mock_open: mock.MagicMock = mock.MagicMock(wraps=open)

    with mock.patch("builtins.open", mock_open):
        importlib.reload(kanon_api.core.ephemerides.tables)

    assert mock_open.call_count == len(cached_tables)

    settings.PRODUCTION = False
