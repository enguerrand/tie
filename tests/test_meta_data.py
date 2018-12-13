from unittest import TestCase

from pytag.meta_data import MetaData


class TestMetaData(TestCase):

    def test_serialize(self):
        data = MetaData(["foo", "bar", "foo bar", "äöü", "'", '"'])
        serialized: str = data.serialize()
        self.assertEqual('{"tags": ["foo", "bar", "foo bar", "\\u00e4\\u00f6\\u00fc", "\'", "\\""]}', serialized)
        deserialized = MetaData.deserialize(serialized)
        self.assertEqual(data.tags, deserialized.tags)
