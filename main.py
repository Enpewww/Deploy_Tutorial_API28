## Import FastAPI
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

# Fast API -> class membuat API
app = FastAPI()

# Buat key untuk akses data rahasia
api_key = "admin28gacor"

# api function -> get, put, post, delete

# Membuat endpoint
# @object.function_api_type("url")
@app.get('/')
def home():
    return{"message": "Yak, Selamat Datang"}

# Menjalankan API
# uvicorn nama_file_tanpa_py: nama_object --reload
#uvicorn main:app --reload

# membuat endpoint untuk membaca data
@app.get("/data")
def readData():
    # read file by pandas in csv
    df = pd.read_csv("dataToko.csv")
    # output
    return df.to_dict(orient="records")

# endpoint lainnya tambahan (penggunaan get)
@app.get("/data/{user_input}")
def searchdata(user_input: int):
    # baca file
    df = pd.read_csv("dataToko.csv")
    # bikin filter
    filter = df[df["id"] == user_input]
    # buat kondisi
    if len(filter) == 0:
        raise HTTPException(status_code = 404, detail="Barangnya ketilep")
    # bikin return untuk kondisi yang ada di idnya 
    return filter.to_dict(orient="records")

# Endpoint lagi untuk update data (penggunaan post)
@app.post("/items/{item_name}")
def updateData(item_id: int, item_name: str, item_price: int):
    # baca file 
    df = pd.read_csv("dataToko.csv")
    # data tambahan
    update_data = {
        "id": item_id,
        "namaBarang" : item_name,
        "harga" : item_price
    }
    # convert dict to dataframe
    update_data_df = pd.DataFrame(update_data, index=[0])
    # gabungkan menggunakan concat
    df = pd.concat([df, update_data_df], ignore_index=True)
    # simpan data terupdate
    df.to_csv("dataToko.csv", index=False)

    # output
    return{"message": f"barang ketilep dengan nama {item_name} sudah ketemu"}

# Endpoint lagi untuk update atau replace data yang sudah ada (penggunaan put)
@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: int):
    # baca file 
    df = pd.read_csv("dataToko.csv")
    # data tambahan
    update_data = {
        "id": item_id,
        "namaBarang" : item_name,
        "harga" : item_price
    }

    # create condition for checking existing data
    if update_data["id"] not in df["id"].values:
        print("id barang tidak ada yak")
    else:
        # update data
        df.loc[df["id"] == update_data["id"], "namaBarang"] = update_data["namaBarang"]
        df.loc[df["id"] == update_data["id"], "harga"] = update_data["harga"]

    # simpan data update ke csv
    df.to_csv("dataToko.csv", index=False)

    # output
    return{"message": f"item dengan nama {item_name} udah ke update yak"}

# Buat endpoint untuk read data rahasia
@app.get("/datarahasia")
def readSecret(password: str = Header(None)):
    # baca data rahasia
    df_income = pd.read_csv('dataIncome.csv')
    # kondisi untuk mathcing password input with api_key
    if password != api_key or password is None:
        raise HTTPException(status_code=401, detail = "Akses gabisa ya!")
    
    # output
    return df_income.to_dict(orient="records")