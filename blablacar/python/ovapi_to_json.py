import requests
import json
from datetime import date

class OVAPIClientException(requests.exceptions.RequestException):
    """Exception class for OVAPI client"""
    pass

class OVAPIClient:
    """OVAPI client for fetching public transport lines data"""
    BASE_URL = "http://v0.ovapi.nl"
    ENDPOINT_LINE = BASE_URL + "/line/"

    # Define the schema for the expected data structure
    LINE_SCHEMA = {
        "LineWheelchairAccessible": str,
        "TransportType": str,
        "DestinationName50": str,
        "DataOwnerCode": str,
        "DestinationCode": str,
        "LinePublicNumber": str,
        "LinePlanningNumber": str,
        "LineName": str,
        "LineDirection": int
    }

    def get_lines(self):
        """Fetches lines data from OVAPI"""
        endpoint = self.ENDPOINT_LINE

        # This part of the code tries to get the response from the API and raises and error when it fails.
        try:
            response = requests.request("GET",endpoint)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise  OVAPIClientException(e)

        # Returns the data from the API as a json file
        return response.json()

    def validate_line_data(self, line_data):
        """Validates that the line data matches the expected schema"""
        try:
            # Validate that the line data matches the expected schema
            for key, expected_type in self.LINE_SCHEMA.items():
                if key not in line_data:
                    raise ValueError(f"Missing key '{key}' in line data")
                if not isinstance(line_data[key], expected_type):
                    raise ValueError(f"Unexpected data type for key '{key}' in line data")
            return True
        except ValueError as e:
            print(e)
            return False

    def flatten_json(self):
        """Flattens the received json, to set it up for Big Query"""
        lines = self.get_lines()
        lines_with_date = []
        skipped_lines = []
        for line in lines:
            line_data = lines[line]
            try:
                # Validate the line data
                self.validate_line_data(line_data)
                # Flattens the different lines
                # Adds the execution_date to keep the history of the API calls
                line_data["execution_date"] = str(date.today())
                # Reorder the keys so that "line" comes first
                reordered_data = {"line": line}
                reordered_data.update(line_data)
                lines_with_date.append(reordered_data)
            except Exception as e:
                # If there was an error, skip this line and log the error
                skipped_lines.append({"line": line, "error": str(e)})

        json_str = "\n".join([json.dumps(line) for line in lines_with_date])
        return json_str

# Example usage
# client = OVAPIClient()
# lines_json = client.flatten_json()
# with open("lines.json", "w") as f:
#     f.write(lines_json)
# print(lines_json)
