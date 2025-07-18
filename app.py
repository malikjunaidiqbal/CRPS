import logging
import json
import joblib
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import os
from typing import Optional
import uvicorn
import pandas as pd
from predictions import area_mapping, crime_code_mapping, high_risk_json
from datetime import datetime, timedelta

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create the app object
app = FastAPI()

# Load the pre-trained XGBoost model (replace with the correct path)
# try:
#     model = joblib.load('xgboost_model.joblib')
#     logging.info("Model loaded successfully.")
# except Exception as e:
#     logging.error(f"Error loading model: {e}")
#     raise HTTPException(status_code=500, detail="Model loading failed.")

def parse_date(date_str):
    """
    Parse date string in the format 'DD/MM/YYYY'
    
    Args:
        date_str (str): Date string in 'DD/MM/YYYY' format
    
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        return None

def get_date_range(filter_param):
    """
    Determine the date range based on the filter parameter
    
    Args:
        filter_param (str): Filter parameter 
    
    Returns:
        tuple: Start and end dates for the filter
    """
    today = datetime.now()
    
    if filter_param == 'today':
        return today, today + timedelta(days=1)
    elif filter_param == 'aweek':
        return today, today + timedelta(days=7)
    elif filter_param == 'twoweeks':
        return today, today + timedelta(days=14)
    elif filter_param == 'amonth':
        return today, today + timedelta(days=30)
    else:
        return None, None

# Define the input data structure using Pydantic models
class CrimeData(BaseModel):
    AREA: int
    Crm_Cd: int
    Vict_Sex: int
    Vict_Descent: int
    Weapon_Desc: int
    case_solved: int


# Index route
@app.get("/")
def health_check():
    logging.info("Received request at '/' endpoint.")
    return {"message": "Server is live!"}


@app.get("/predictions")
def fetch_high_risk_predictions(filter: Optional[str] = Query(None, description="Filter predictions by date range")):
    try:
        # Convert JSON string to Python list
        predictions = json.loads(high_risk_json)
        
        # Set default filter to 'amonth' if no filter is provided
        if filter is None:
            filter = 'amonth'
        
        # Validate filter parameter
        valid_filters = ['today', 'aweek', 'twoweeks', 'amonth']
        
        if filter not in valid_filters:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid filter. Must be one of {', '.join(valid_filters)}"
            )
        
        # Get date range for filtering
        start_date, end_date = get_date_range(filter)
        
        if start_date is None or end_date is None:
            raise HTTPException(
                status_code=400, 
                detail="Invalid date range"
            )

        # Group predictions by AREA NAME with consolidated information
        grouped_predictions = {}
        for pred in predictions:
            # Parse prediction date
            pred_date = parse_date(pred['dates'])
            
            # Skip if date is invalid or outside the range
            if not pred_date or pred_date < start_date or pred_date >= end_date:
                continue
            
            key = pred['AREA NAME']
            
            if key not in grouped_predictions:
                # Create a new entry if it doesn't exist
                grouped_predictions[key] = {
                    'dates': [pred['dates']],
                    'AREA NAME': pred['AREA NAME'],
                    'Crm Cd Desc': [pred['Crm Cd Desc']],
                    'Risk': pred['Risk'],
                    'Probability': [pred['Probability']]
                }
            else:
                # Append information to existing entry
                # Avoid duplicate dates
                if pred['dates'] not in grouped_predictions[key]['dates']:
                    grouped_predictions[key]['dates'].append(pred['dates'])
                
                # Avoid duplicate crime descriptions
                if pred['Crm Cd Desc'] not in grouped_predictions[key]['Crm Cd Desc']:
                    grouped_predictions[key]['Crm Cd Desc'].append(pred['Crm Cd Desc'])
                
                # Add probability
                grouped_predictions[key]['Probability'].append(pred['Probability'])
        
        # Convert grouped predictions to a list
        response = {
            "predictions": list(grouped_predictions.values())
        }
        
        return JSONResponse(content=response)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error fetching high-risk data: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Crime frequency graph data
graph_data_1 = {
    "data": [
        {
            "type": "scatter",
            "mode": "lines+markers",
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "y": [10, 15, 13, 9, 12, 14, 11, 17, 16, 19, 18, 20],
            "line": {"color": "dodgerblue", "width": 3},
            "marker": {"size": 8},
        }
    ],
    "layout": {
        "height": 600,
        "width": 800,
        "template": "plotly_white",
        "title": "Monthly Crime Frequency for Year 2024",
        "xaxis": {
            "title": "Month",
            "tickmode": "array",
            "tickvals": list(range(1, 13)),
            "ticktext": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
        },
        "yaxis": {"title": "Number of Crimes"},
    },
}

# Gender distribution pie chart data
graph_data_2 = {
    "data": [
        {
            "type": "pie",
            "values": [500, 300, 100],
            "labels": ["M = Male", "F = Female", "X = Unknown"],
            "hoverinfo": "label+percent",
            "hole": 0.3,
        }
    ],
    "layout": {
        "height": 600,
        "width": 800,
        "template": "plotly_white",
        "title": "Distribution of Victims Affected by Crime (Gender)",
        "showlegend": True,
    },
}

# Risky area names bar chart data
df = pd.read_csv("df1.csv")
area_names = df["AREA NAME"].value_counts().index.tolist()
values = df["AREA NAME"].value_counts().values.tolist()
quartiles = df["AREA NAME"].value_counts().quantile([0.25, 0.5, 0.75])


def classify_quartile(value):
    if value <= quartiles[0.5]:
        return "0 to 50%"
    else:
        return "50 to 100%"


quartiles_percentage = pd.Series(values).apply(classify_quartile)
colors = {"0 to 50%": "orange", "50 to 100%": "red"}

graph_data_3 = {
    "data": [
        {
            "type": "bar",
            "x": area_names,
            "y": values,
            "marker": {"color": quartiles_percentage.map(colors).tolist()},
        }
    ],
    "layout": {
        "height": 600,
        "width": 800,
        "template": "plotly_white",
        "title": "Risky Area Names with Percentage Distribution",
        "xaxis": {"title": "Area Name"},
        "yaxis": {"title": "Crime Count"},
    },
}


# Endpoint for the crime frequency graph
@app.get("/crime_frequency_graph")
def get_crime_frequency_graph():
    logging.info("Returning graph data for the 2024 monthly crime frequency.")
    return JSONResponse(content=graph_data_1)


# Endpoint for the gender distribution pie chart
@app.get("/gender_distribution_graph")
def get_gender_distribution_graph():
    logging.info("Returning graph data for gender distribution in crime victims.")
    return JSONResponse(content=graph_data_2)


# Endpoint for the risky area names bar chart
@app.get("/risky_areas_graph")
def get_risky_areas_graph():
    logging.info("Returning graph data for risky area names.")
    return JSONResponse(content=graph_data_3)


@app.get("/city_crime_mapping")
def get_city_crime_mapping():
    return {"city_names": area_mapping, "crime_types": crime_code_mapping}


CSV_FILE = "dataset.csv"


# Define the data model with optional fields except for the required ones
class CrimeRecord(BaseModel):
    AREA_NAME: str = Field(..., description="Area Name")
    Crm_Cd_Desc: str = Field(..., description="Crime Code Description")
    DATE_OCC: Optional[str] = None

    DR_NO: Optional[int] = None
    Date_Rptd: Optional[str] = None
    TIME_OCC: Optional[int] = None
    AREA: Optional[int] = None
    Rpt_Dist_No: Optional[int] = None
    Part_1_2: Optional[int] = None
    Crm_Cd: Optional[int] = None
    Mocodes: Optional[str] = None
    Vict_Age: Optional[int] = None
    Vict_Sex: Optional[str] = None
    Vict_Descent: Optional[str] = None
    Premis_Cd: Optional[int] = None
    Premis_Desc: Optional[str] = None
    Weapon_Used_Cd: Optional[str] = None
    Weapon_Desc: Optional[str] = None
    Status: Optional[str] = None
    Status_Desc: Optional[str] = None
    Crm_Cd_1: Optional[int] = None
    Crm_Cd_2: Optional[int] = None
    Crm_Cd_3: Optional[int] = None
    Crm_Cd_4: Optional[int] = None
    LOCATION: Optional[str] = None
    Cross_Street: Optional[str] = None
    LAT: Optional[float] = None
    LON: Optional[float] = None


# Endpoint to add a new record
@app.post("/crime_reporting")
def crime_reporting(record: CrimeRecord):
    try:
        # Check if the file exists
        if not os.path.exists(CSV_FILE):
            # Create an empty dataframe with the required columns
            columns = [
                "DR_NO",
                "Date Rptd",
                "DATE OCC",
                "TIME OCC",
                "AREA",
                "AREA NAME",
                "Rpt Dist No",
                "Part 1-2",
                "Crm Cd",
                "Crm Cd Desc",
                "Mocodes",
                "Vict Age",
                "Vict Sex",
                "Vict Descent",
                "Premis Cd",
                "Premis Desc",
                "Weapon Used Cd",
                "Weapon Desc",
                "Status",
                "Status Desc",
                "Crm Cd 1",
                "Crm Cd 2",
                "Crm Cd 3",
                "Crm Cd 4",
                "LOCATION",
                "Cross Street",
                "LAT",
                "LON",
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(CSV_FILE, index=False)

        # Read the existing dataset
        df = pd.read_csv(CSV_FILE)

        # Add the new record
        new_record = pd.DataFrame([record.model_dump()])
        df = pd.concat([df, new_record], ignore_index=True)

        # Save the updated dataset
        df.to_csv(CSV_FILE, index=False)

        return {"message": "Record added successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API with uvicorn
if __name__ == "__main__":
    logging.info("Starting FastAPI application.")
    uvicorn.run(app, host="0.0.0.0", port=8000)