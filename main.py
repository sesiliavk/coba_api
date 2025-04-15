# import package
#FastAPI nama class fastapi untuk modulnya

from fastapi import FastAPI, HTTPException, Header
import pandas as pd

password = 'secret123'
# create FastAPI object
app = FastAPI()

# endpoint adalah sebuah istilah alamat sebuah halaman tertentu yang bisa di akses oleh klien
# create endpoint untuk mendapatkan data di halaman awal/utama
# bisa ('/')
@app.get("/") 
def getData(): # function handler -> untuk menhandle request dari endpoint
    return{
        'message':'hello world'
    }

# endpoint untuk ambil dati di csv
@app.get("/data")
def getCsv(): # function handler -> untuk menhandle request dari endpoint
    # 1. baca data dari csv
    df = pd.read_csv("data.csv")

    # 2. Tampilkan response berupa data csv json
    return df.to_dict(orient="records")

@app.get("/data/{name}")
def getDataByName(name: str): # function handler -> untuk menhandle request dari endpoint
    # 1. baca data dari csv
    df = pd.read_csv("data.csv")
    #2. filter data by name
    result = df[df['name']== name] 

    # 3. check apakah hasil filter > 0 (ada)
    if len(result) > 0:
    # 2. Tampilkan response berupa data csv json
        return result.to_dict(orient="records")
    else:
        # tampilkan pesan error
        raise HTTPException(status_code=404, detail='data '+name+' Tidak Ditemukan')

@app.delete("/data/{name}")
def deletDataByName(name: str, api_key: str = Header(None)): # function handler -> untuk menhandle request dari endpoint
    # check auth

    if api_key != None and api_key==password:
        # 1. baca data dari csv
        df = pd.read_csv("data.csv")
        #2. filter data by name
        result = df[~(df['name']== name)] 
        # 3. replace cvs exixting -> data yang di filter akan hilang
        result.to_csv('data.csv', index=False)
        # 4. Tampilkan response berupa data csv json
        return result.to_dict(orient="records")
    else:
        raise HTTPException(status_code=403, detail="password salah")