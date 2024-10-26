from datetime import datetime
BANNER = r'''
            __                                        
        __ / /__ ___ __                               
       / // / _ `/\ \ /                               
       \___/\_,_//_\_\                                
   _______  _________    ____                         
  / __/ _ \/  _/ ___/___/ __/__________ ____  ___ ____
 / _// ___// // /__/___/\ \/ __/ __/ _ `/ _ \/ -_) __/
/___/_/  /___/\___/   /___/\__/_/  \_,_/ .__/\__/_/   
                                      /_/             
'''

def setup_config(start_date_str, end_date_str):
    # Validate and format dates
    try:
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    # Format dates for API payload
    start_date_iso = start_date_obj.strftime("%Y-%m-%dT00:00:00.000Z")
    end_date_iso = end_date_obj.strftime("%Y-%m-%dT23:59:59.999Z")

    # Get current date for DateEntered and DateUpdated fields
    current_date_str = datetime.now().strftime("%a %b %d %Y")

    # Format date for filename
    def format_date_for_filename(date_obj):
        return date_obj.strftime("%Y%m%d")

    filename_base = f"{format_date_for_filename(start_date_obj)}_{format_date_for_filename(end_date_obj)}"

    config = {
        'start_date_str': start_date_str,
        'end_date_str': end_date_str,
        'start_date_iso': start_date_iso,
        'end_date_iso': end_date_iso,
        'current_date_str': current_date_str,
        'filename_base': filename_base
    }

    return config
