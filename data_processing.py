import pandas as pd
import logging
from api import get_permit_details
import json
from tqdm import tqdm  # For progress bars
import time

# Process the initial data and prepare the DataFrame
def process_initial_data(values):
    try:
        logging.debug("Processing initial data into DataFrame.")
        df = pd.DataFrame(values)
        logging.debug(f"Initial DataFrame shape: {df.shape}")
        # Rename columns
        df.rename(
            columns={
                "FullPermitNumber_Click": "Permit ID",
                "PermitTypeDescription": "Permit type",
                "ProposedUseDescription": "Proposed Use",
                "StructureTypeDescription": "Structure Type",
                "WorkTypeDescription": "Work Type",
                "StatusDescription": "Status",
                "DateIssued": "Date Issued",
                "Address": "Project Address",
            },
            inplace=True,
        )
        # Remove columns
        df.drop(
            columns=[col for col in ["FullPermitNumber", "FullPermitNumber_Clickable"] if col in df.columns],
            inplace=True,
        )
        # Modify 'Permit ID' column
        df["Permit ID"] = df["Permit ID"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else "")
        # Add new empty columns
        for col in ["Job Cost", "Company Name", "Email", "Phone", "Contractor Name", "License number"]:
            df[col] = ""
        # Reorder columns
        desired_order = [
            "Project Address",
            "Date Issued",
            "Permit type",
            "Proposed Use",
            "Status",
            "Structure Type",
            "Work Type",
            "Job Cost",
            "Company Name",
            "Email",
            "Phone",
            "Contractor Name",
            "License number",
            "Permit ID",
        ]
        df = df[[col for col in desired_order if col in df.columns]]
        logging.debug(f"Processed DataFrame shape: {df.shape}")
        return df
    except Exception as e:
        logging.exception("Error processing initial data.")
        return pd.DataFrame()

# Process permit details and populate the DataFrame
def process_permit_details(df):
    try:
        logging.info("Processing permit details for each record.")
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing permits"):
            permit_id_hex = row["Permit ID"]
            try:
                # Convert hex string to decimal
                permit_id_decimal = int(permit_id_hex, 16)
            except ValueError:
                logging.warning(f"Invalid Permit ID '{permit_id_hex}' at index {index}")
                continue
            # Fetch additional data
            permit_details = get_permit_details(permit_id_decimal)
            if permit_details:
                # Extract and populate the data
                df.at[index, "Job Cost"] = permit_details.get("TotalCost", "")
                permit_companies = permit_details.get("PermitCompanies") or []
                if permit_companies:
                    company_info = permit_companies[0]
                    company = company_info.get("Company") or {}
                    contractor = company_info.get("Contractor") or {}
                    contractor_license = company_info.get("ContractorQaLicense") or {}
                    df.at[index, "Company Name"] = company.get("DisplayName", "")
                    df.at[index, "Email"] = company.get("Email", "")
                    # Get phone number if available
                    phone_numbers = company.get("UserPhoneNumbers") or []
                    if phone_numbers:
                        phone_number = phone_numbers[0].get("PhoneNumber", {}).get("Number", "")
                        df.at[index, "Phone"] = phone_number
                    df.at[index, "Contractor Name"] = contractor.get("DisplayName", "")
                    df.at[index, "License number"] = contractor_license.get("LicenseNumber", "")
            else:
                logging.warning(f"Could not retrieve details for Permit ID {permit_id_decimal}")
            # Optional: Add a delay to prevent overloading the server
            time.sleep(0.1)
        logging.info("Completed processing permit details.")
        return df
    except Exception as e:
        logging.exception("Error processing permit details.")
        return df

# Save data to Excel
def save_to_excel(df, filename_base):
    try:
        excel_filename = f"{filename_base}.xlsx"
        df.to_excel(excel_filename, index=False)
        logging.info(f"Data successfully saved to {excel_filename}")
    except Exception as e:
        logging.exception("Error saving data to Excel.")

# Save data to JSON
def save_to_json(data, filename_base):
    try:
        json_filename = f"{filename_base}.json"
        with open(json_filename, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data successfully saved to {json_filename}")
    except Exception as e:
        logging.exception("Error saving data to JSON.")
