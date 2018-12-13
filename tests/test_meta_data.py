from unittest import TestCase

import pytag.meta_data as md


class TestMetaData(TestCase):

    def test_serialize(self):
        data = md.MetaData(["foo", "bar", "foo bar", "äöü", "'", '"'])
        serialized: str = data.serialize()
        self.assertEqual('{"tags": ["foo", "bar", "foo bar", "\\u00e4\\u00f6\\u00fc", "\'", "\\""]}', serialized)
        deserialized = md.deserialize(serialized)
        self.assertEqual(data.tags, deserialized.tags)
