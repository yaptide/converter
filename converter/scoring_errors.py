def output_detector_error(output_name: str, detector_uuid: str | None) -> ValueError:
    """Error for an output whose detector is not selected or no longer exists."""
    if not detector_uuid:
        return ValueError(f'Output "{output_name}" has no detector selected.')
    return ValueError(f'Output "{output_name}" uses a detector that does not exist (uuid {detector_uuid}).')


def quantity_filter_error(quantity_name: str, output_name: str, filter_uuid: str | None) -> ValueError:
    """Error for a quantity whose filter is not selected or no longer exists."""
    quantity = f'Quantity "{quantity_name}" in output "{output_name}"'
    if not filter_uuid:
        return ValueError(f"{quantity} has Filter checked but no filter selected.")
    return ValueError(f"{quantity} uses a filter that does not exist (uuid {filter_uuid}).")
