# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd
# buat object/instance
app = FastAPI()

# create API Key
API_Key = "hck024data"

#create endpoint home
@app.get("/")
def home():
    return {"message": "Selamat datang di Toko Dzaki"}

#create endpoint data
@app.get("/data")
def read_data():
    df = pd.read_csv("data.csv")
    #convert data frame to dictionary, with orient="record" for each row
    return df.to_dict(orient="records")
    # return df.to_json()

#create endpoint data with parameter value=id
@app.get("/data/{number_id}")
def read_item(number_id: int):
    df = pd.read_csv("data.csv")
    #filter data by id
    filter_data = df[df["id"] == number_id]

    # check if filter data is empty
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="Oops! Data Not Found!")
    # tampilkan filter data yang diconvert ke dict
    return filter_data.to_dict(orient="records")

# create end point update (put) file csv.data
@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    df = pd.read_csv("data.csv")

    # create new dataframe with updated input
    updated_df = pd.DataFrame({
        "id": number_id,
        "nama_barang": nama_barang,
        "harga": harga
    }, index=[0])

    # updated_df = pd.DataFrame([{
    #     "id": number_id,
    #     "nama_barang": nama_barang,
    #     "harga": harga
    # }])

    #merge updated data frame dengan dataframe original
    df = pd.concat([df, updated_df], ignore_index=True)

    # save updated data frame to csv
    df.to_csv('data.csv', index=False)
    return {"message": f"Item with ID {number_id} has been updated successfully."}

@app.get("/secret")
def secret_is_out(api_key: str = Header(None)):
    secret_df = pd.read_csv("secret_data.csv")
    #check if statement untuk nilai API_Key
    if api_key != API_Key:
        raise HTTPException(status_code=401, detail="API Key tidak valid.")
    
    return secret_df.to_dict(orient="records")