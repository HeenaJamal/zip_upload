# main.py
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import zipfile
import io
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, MetaData, Integer, String, Float, Text
from database import get_db, engine
from models import CSVDataEntry

app = FastAPI()

@app.post("/upload-zip/")
async def upload_zip_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the ZIP file
        contents = await file.read()
        zip_file = zipfile.ZipFile(io.BytesIO(contents))

        metadata = MetaData()
        metadata.bind = engine

        for file_name in zip_file.namelist():
            if file_name.endswith('.csv'):
                with zip_file.open(file_name) as csv_file:
                    df = pd.read_csv(csv_file)

                    # Dynamically create table based on CSV structure
                    table_name = f"csvdata_{file_name.split('.')[0]}"
                    columns = [
                        Column("id", Integer, primary_key=True)
                    ]

                    # Add columns dynamically based on CSV header
                    for col in df.columns:
                        # Set column type based on data type inference
                        if pd.api.types.is_integer_dtype(df[col]):
                            col_type = Integer
                        elif pd.api.types.is_float_dtype(df[col]):
                            col_type = Float
                        else:
                            col_type = Text

                        columns.append(Column(col, col_type))

                    # Dynamically create table with inferred columns
                    table = Table(table_name, metadata, *columns)
                    metadata.create_all(engine)

                    # Insert data into the newly created table
                    for _, row in df.iterrows():
                        row_data = {col: row[col] for col in df.columns}
                        db.execute(table.insert().values(**row_data))
                    
                    db.commit()

        return JSONResponse(content={"message": "Data from ZIP uploaded successfully!"}, status_code=201)
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=400)
