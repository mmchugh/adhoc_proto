import struct


class InvalidFileException(Exception):
    pass


class TransactionRecordsData:

    def __init__(self, filepath):
        self.records = []

        with open(filepath, 'rb') as data_file:
            self.total_records = self.parse_header(data_file)
            while len(self.records) < self.total_records:
                self.records.append(self.parse_row(data_file))

    @staticmethod
    def parse_header(data_file):
        """
        Parse the values and verify correctness of a header from given data.
        Format:
          4 byte magic string "MPS7" | 1 byte version | 4 byte (uint32) count

        Returns the count of records indicated by the header.
        """

        header_format = ">4scI"
        header = data_file.read(struct.calcsize(header_format))
        filetype, version, records = struct.unpack(header_format, header)
        if not filetype == b"MPS7":
            raise InvalidFileException

        # Only 1 known version, so no need to do anything special with it

        return records

    @staticmethod
    def parse_row(data_file):
        transaction_type = data_file.read(1)

        if transaction_type not in ROW_PARSERS:
            raise InvalidFileException

        return ROW_PARSERS[transaction_type](data_file)


class DebitRecord:
    record_name = "Debit"
    record_type = b"\x00"
    record_format = ">IQd"

    def __init__(self, data_file):
        self.row = data_file.read(struct.calcsize(self.record_format))
        self.timestamp, self.user_id, self.amount = struct.unpack(
            self.record_format, self.row
        )


class CreditRecord:
    record_name = "Credit"
    record_type = b"\x01"
    record_format = ">IQd"

    def __init__(self, data_file):
        self.row = data_file.read(struct.calcsize(self.record_format))
        self.timestamp, self.user_id, self.amount = struct.unpack(
            self.record_format, self.row
        )


class StartAutopayRecord:
    record_name = "StartAutopay"
    record_type = b"\x02"
    record_format = ">IQ"

    def __init__(self, data_file):
        self.row = data_file.read(struct.calcsize(self.record_format))
        self.timestamp, self.user_id = struct.unpack(
            self.record_format, self.row
        )


class EndAutopayRecord:
    record_name = "EndAutopay"
    record_type = b"\x03"
    record_format = ">IQ"

    def __init__(self, data_file):
        self.row = data_file.read(struct.calcsize(self.record_format))
        self.timestamp, self.user_id = struct.unpack(
            self.record_format, self.row
        )


available_records = (
    DebitRecord,
    CreditRecord,
    StartAutopayRecord,
    EndAutopayRecord,
)

ROW_PARSERS = {record.record_type: record for record in available_records}
