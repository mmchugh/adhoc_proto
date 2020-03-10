import io
import struct
import unittest

import parser


class TestParser(unittest.TestCase):

    def test_bad_magic_string_raises(self):
        magic_string = b"7SPM"
        arbitrary_version = b"\x01"
        arbitrary_count = 99

        data = io.BytesIO(
            struct.pack(
                ">4scI", magic_string, arbitrary_version, arbitrary_count
            )
        )

        with self.assertRaises(parser.InvalidFileException):
            parser.TransactionRecordsData.parse_header(data)

    def test_valid_header_parses(self):
        magic_string = b"MPS7"
        arbitrary_version = b"\x01"
        arbitrary_count = 99

        data = io.BytesIO(
            struct.pack(
                ">4scI", magic_string, arbitrary_version, arbitrary_count
            )
        )
        records = parser.TransactionRecordsData.parse_header(data)

        self.assertEqual(records, arbitrary_count)

    def test_correct_record_is_returned(self):
        transaction_type = b"\x00"
        arbitrary_timestamp = 42
        arbitrary_user_id = 1234
        arbitrary_amount = 10.50
        data = io.BytesIO(
            struct.pack(
                ">cIQd",
                transaction_type,
                arbitrary_timestamp,
                arbitrary_user_id,
                arbitrary_amount,
            )
        )

        record = parser.TransactionRecordsData.parse_row(data)

        self.assertEqual(record.record_type, transaction_type)
        self.assertEqual(record.record_name, "Debit")

    def test_can_parse_debit(self):
        arbitrary_timestamp = 42
        arbitrary_user_id = 1234
        arbitrary_amount = 10.50
        data = io.BytesIO(
            struct.pack(
                ">IQd", arbitrary_timestamp, arbitrary_user_id, arbitrary_amount
            )
        )
        record = parser.DebitRecord(data)

        self.assertEqual(record.timestamp, arbitrary_timestamp)
        self.assertEqual(record.user_id, arbitrary_user_id)
        self.assertEqual(record.amount, arbitrary_amount)

    def test_can_parse_credit(self):
        arbitrary_timestamp = 42
        arbitrary_user_id = 1234
        arbitrary_amount = 10.50
        data = io.BytesIO(
            struct.pack(
                ">IQd", arbitrary_timestamp, arbitrary_user_id, arbitrary_amount
            )
        )
        record = parser.CreditRecord(data)

        self.assertEqual(record.timestamp, arbitrary_timestamp)
        self.assertEqual(record.user_id, arbitrary_user_id)
        self.assertEqual(record.amount, arbitrary_amount)

    def test_can_parse_start_autopay(self):
        arbitrary_timestamp = 42
        arbitrary_user_id = 1234
        data = io.BytesIO(
            struct.pack(">IQ", arbitrary_timestamp, arbitrary_user_id)
        )
        record = parser.StartAutopayRecord(data)

        self.assertEqual(record.timestamp, arbitrary_timestamp)
        self.assertEqual(record.user_id, arbitrary_user_id)

    def test_can_parse_end_autopay(self):
        arbitrary_timestamp = 42
        arbitrary_user_id = 1234
        data = io.BytesIO(
            struct.pack(">IQ", arbitrary_timestamp, arbitrary_user_id)
        )
        record = parser.EndAutopayRecord(data)

        self.assertEqual(record.timestamp, arbitrary_timestamp)
        self.assertEqual(record.user_id, arbitrary_user_id)


if __name__ == '__main__':
    unittest.main()
