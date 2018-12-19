from unittest import TestCase

import tie.meta_data as md


class TestMetaData(TestCase):

    def test_serialize(self):
        data = md.MetaData(["foo", "bar", "foo bar", "äöü", "'", '"'], "42")
        serialized: str = data.serialize()
        self.assertEqual('{"tags": ["foo", "bar", "foo bar", "\\u00e4\\u00f6\\u00fc", "\'", "\\""], "ver": "42"}', serialized)
        deserialized = md.deserialize(serialized)
        self.assertEqual(data.tags, deserialized.tags)

    def test_deserialize_malformed_json(self):
        serialized: str = '{foo bar'
        self.assertRaises(md.InvalidMetaDataError, lambda: md.deserialize(serialized))

    def test_deserialize_invalid_meta_data(self):
        serialized: str = '{"blubb": ["foo", "bar"]}'
        self.assertRaises(md.InvalidMetaDataError, lambda: md.deserialize(serialized))
