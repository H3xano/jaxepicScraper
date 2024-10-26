import requests
import logging
import json

# API endpoint and headers
url = "https://jaxepicsapi.coj.net/api/AdvancedSearches/Advanced"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://jaxepics.coj.net",
    "Referer": "https://jaxepics.coj.net/",
    "Connection": "keep-alive",
}

# Function to make POST requests to get permit listings
def get_results(page, pageSize, config):
    params = {
        "page": page,
        "pageSize": pageSize,
        "filter": "",
        "sortActive": "FullPermitNumber",
        "sortDirection": "asc",
        "forSpreadSheet": "false",
    }

    # Base data payload with dynamic dates from config
    data = {
        "SavedSearchColumns": [{"ColumnId": i} for i in range(1, 9)],
        "SavedSearchFilters": [
            {
                # Date Issued Filter
                "SavedSearchFilterId": 0,
                "SavedSearchId": 0,
                "ColumnId": 7,
                "Column": {
                    "ColumnId": 7,
                    "Name": "DateIssued",
                    "DisplayName": "Date Issued",
                    "DataType": "date",
                    "Default": True,
                    "LkpColumnOperators": [
                        {
                            "ColumnOperatorID": 0,
                            "OperatorId": 10,
                            "Default": True,
                            "Operator": {
                                "OperatorId": 10,
                                "OperatorName": "Between",
                                "LkpOperatorControls": [
                                    {
                                        "OperatorControlId": 0,
                                        "ControlField": {
                                            "ControlFieldId": 3980,
                                            "ControlFieldDescription": "Search Date Spread",
                                            "IsActive": True,
                                            "IsRequired": True,
                                            "Editable": True,
                                            "Field": {
                                                "FieldId": 3874,
                                                "FieldBind": "object.DateSpread",
                                                "FieldDescription": "Search Date Spread",
                                                "IsActive": True,
                                            },
                                        },
                                    }
                                ],
                            },
                        }
                    ],
                },
                "OperatorId": 10,
                "Obj": {
                    "DateSpread": {
                        "lowerBound": config['start_date_iso'],
                        "upperBound": config['end_date_iso'],
                    }
                },
                "Completed": True,
                "DateEntered": config['current_date_str'],
                "DateUpdated": config['current_date_str'],
                "EvalValueString": json.dumps({
                    "DateSpread": {
                        "lowerBound": config['start_date_iso'],
                        "upperBound": config['end_date_iso']
                    }
                }),
                "IsActive": True,
                "SavedSearch": None,
            },
            {
                # Permit Type Filter
                "SavedSearchFilterId": 0,
                "SavedSearchId": 0,
                "ColumnId": 2,
                "Column": {
                    "ColumnId": 2,
                    "Name": "PermitTypeDescription",
                    "DisplayName": "Permit Type",
                    "Default": True,
                    "LkpColumnOperators": [
                        {
                            "ColumnOperatorID": 0,
                            "OperatorId": 18,
                            "Default": True,
                            "Operator": {
                                "OperatorId": 18,
                                "OperatorName": "Equals",
                                "LkpOperatorControls": [
                                    {
                                        "OperatorControlId": 0,
                                        "ControlField": {
                                            "ControlFieldId": 3984,
                                            "ControlFieldDescription": "Search Select",
                                            "IsActive": True,
                                            "IsRequired": True,
                                            "Editable": True,
                                            "Field": {
                                                "FieldId": 3877,
                                                "FieldBind": "object.selection",
                                                "FieldDescription": "Search Select",
                                                "IsActive": True,
                                                "DropdownBind": "MntPermitType",
                                            },
                                        },
                                    }
                                ],
                            },
                        }
                    ],
                },
                "OperatorId": 18,
                "Obj": {"selection": 1},
                "Completed": True,
                "DateEntered": config['current_date_str'],
                "DateUpdated": config['current_date_str'],
                "EvalValueString": json.dumps({"selection": 1}),
                "IsActive": True,
                "SavedSearch": None,
            },
        ],
        "UserSavedSearches": [],
        "TableId": 82,
    }

    try:
        logging.debug(f"Requesting page {page} with pageSize {pageSize}.")
        response = requests.post(
            url,
            headers=headers,
            params=params,
            json=data,
            timeout=60,
        )
        response.raise_for_status()
        logging.debug(f"Received response for page {page}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get results for page {page}: {e}")
        return None

# Function to get additional data for each permit
def get_permit_details(permit_id_decimal):
    permit_url = f"https://jaxepicsapi.coj.net/api/Permits/{permit_id_decimal}"
    try:
        logging.debug(f"Requesting details for Permit ID {permit_id_decimal}.")
        response = requests.get(
            permit_url,
            headers=headers,
            timeout=60,
        )
        response.raise_for_status()
        logging.debug(f"Received details for Permit ID {permit_id_decimal}.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get details for Permit ID {permit_id_decimal}: {e}")
        return None
