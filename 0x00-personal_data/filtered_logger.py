#!/usr/bin/env python3
"""
A module for logs filtering.
"""
import os
import re
import logging
import mysql.connector
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """
    Function that filters a log line.

    Args:
        fields (List[str]): A list of field names to filter.
        redaction (str): The string to replace filtered fields with.
        message (str): The log message to filter.
        separator (str): The separator used to split
        the log message into fields.

    Returns:
        str: The filtered log message.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    Function that creates a new logger for user data.

    Returns:
        logging.Logger: The logger object for user data.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Function that creates a connector to a database.

    Returns:
        mysql.connector.connection.MySQLConnection:
        The database connection object.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """
    Function that logs the information about user records in a table.

    This function retrieves user records from a
    database table and logs the information
    using a logger. It fetches the specified fields
    from the table, constructs a log
    message for each record, and handles the log record
    using the info_logger.

    Args:
        None

    Returns:
        None
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """
    Class for redacting Formatter.

    Attributes:
        REDACTION (str): The string used for redaction.
        FORMAT (str): The format string for the log message.
        FORMAT_FIELDS (tuple): The fields used in the log format.
        SEPARATOR (str): The separator used in the log message.

    Args:
        fields (List[str]): The list of fields to be redacted.

    Methods:
        format(record: logging.LogRecord) -> str:
            Formats a LogRecord by redacting specified fields.

    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a LogRecord by redacting specified fields.

        Args:
            record (logging.LogRecord): The LogRecord to be formatted.

        Returns:
            str: The formatted log message with redacted fields.

        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
