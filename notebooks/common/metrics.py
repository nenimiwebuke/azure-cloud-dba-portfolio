"""
Simple operational metrics used by Northstar notebooks.
"""


def print_metric(name: str, value):
    print(f"{name:.<45} {value}")


def print_summary(
    records_read,
    records_written,
    rejected_records,
):
    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    print_metric("Records Read", records_read)
    print_metric("Records Written", records_written)
    print_metric("Rejected Records", rejected_records)

    print("=" * 60)
