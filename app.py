import numpy as np
import pandas as pd
import math
from flask import Flask, redirect, render_template, url_for,request,session

import fractions

app = Flask(__name__)
app.secret_key = 'hello'

randomIndex = [0, 0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.54, 1.56, 1.57, 1.59]

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/index1.html')
def index1():
    return render_template('index1.html')


@app.route('/ghichupa.html')
def ghichupa():
    return render_template('ghichupa.html')

@app.route("/input_matrix", methods=["POST"])
def input():
    if request.method == "POST":
        ten_tieu_chi = request.form["number"]
        tc = request.form["number"].split(", ")
        number = (len(tc))
        return render_template("input_matrix.html", number = number, tc = tc, ten_tieu_chi = ten_tieu_chi)
    else: 
        return "Something went wrong!"
        

@app.route("/sum", methods=["POST"])
def sum():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSo = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("criteria_CR.html" , number = number, ten_tieu_chi = ten_tieu_chi, tc = tc, arr = arr, tong = tong, brr = brr, trongSo = trongSo, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)


@app.route("/input_alternative", methods=["POST"])
def input_alternative():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]

    return render_template("input_alternative.html", number = number, tc = tc, trongSo = trongSo, ten_tieu_chi = ten_tieu_chi)

@app.route("/input_pa1_CR", methods=["POST"])
def input_pa1_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    return render_template("input_pa1_CR.html", number = number, tc = tc, trongSo = trongSo, ten_tieu_chi = ten_tieu_chi)

@app.route("/pa1_CR", methods=["POST"])
def pa1_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSoTg = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("pa1_CR.html" , number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, arr = arr, tong = tong, brr = brr, trongSoTg = trongSoTg, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)
  
@app.route("/input_pa2_CR", methods=["POST"])
def input_pa2_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    return render_template("input_pa2_CR.html", number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg)

@app.route("/pa2_CR", methods=["POST"])
def pa2_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSoMt = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("pa2_CR.html" , number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, arr = arr, tong = tong, brr = brr, trongSoMt = trongSoMt, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)
  

@app.route("/input_pa3_CR", methods=["POST"])
def input_pa3_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    return render_template("input_pa3_CR.html", number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt)

@app.route("/pa3_CR", methods=["POST"])
def pa3_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSoCt = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("pa3_CR.html" , number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, arr = arr, tong = tong, brr = brr, trongSoCt = trongSoCt, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)


@app.route("/input_pa4_CR", methods=["POST"])
def input_pa4_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    trongSoCt = request.form["trongSoCt"]
    return render_template("input_pa4_CR.html", number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, trongSoCt = trongSoCt)

@app.route("/pa4_CR", methods=["POST"])
def pa4_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    trongSoCt = request.form["trongSoCt"]
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSoTb = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("pa4_CR.html" , number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, trongSoCt = trongSoCt, arr = arr, tong = tong, brr = brr, trongSoTb = trongSoTb, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)
  

@app.route("/input_pa5_CR", methods=["POST"])
def input_pa5_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    trongSoCt = request.form["trongSoCt"]
    trongSoTb = request.form["trongSoTb"]
    return render_template("input_pa5_CR.html", number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, trongSoCt = trongSoCt, trongSoTb = trongSoTb)

@app.route("/pa5_CR", methods=["POST"])
def pa5_CR():
    ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    trongSoCt = request.form["trongSoCt"]
    trongSoTb = request.form["trongSoTb"]
    def input_array():
        arr = [[0 for i in range(number)] for j in range(number)]
        a2rr = [[0 for i in range(number)] for j in range(number)]
        for i in range(number):
            for j in range(number):
                if i == j:
                    arr[i][j] = float(1)
                if i <  j:
                    arr[i][j] = round(float(fractions.Fraction(request.form["value" + str(i) + str(j)])), 4)
                    # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                    a2rr[i][j] = arr[i][j]
                    while arr[i][j] < (1/9) or arr[i][j] > (9):
                        arr[i][j] = round(float(fractions.Fraction(2)), 4)
                        # arr[i][j] = round(float(fractions.Fraction(input())), 4)
                        a2rr[i][j] = arr[i][j]
                if i >  j:
                    arr[i][j] = round((1/a2rr[j][i]), 4)
        return arr
    
    # Tính tổng theo cột
    def tinh_tong(arr):
        tong = []
        for j in range(number):
            tongCot = 0
            for i in range(number):
                tongCot = round(tongCot + arr[i][j], 4)

            tong.append(tongCot)
        return tong
        
    # Chuẩn hóa ma trận theo tổng
    def chuan_hoa_array(arr):
        brr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                brr[i][j] = round((arr[i][j] / tinh_tong(arr)[j]), 4)
        return brr

    # Tính trọng số
    def tinh_trong_so(brr):
        trongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + brr[i][j]

            trongSo.append(round((tongHang/number), 4))

        return trongSo

    # Chuẩn hóa ma trận theo trọng số
    def ma_tran_trong_so(arr, brr):
        crr = [[0 for i in range(number)] for j in range(number)]
        for j in range(number):
            for i in range(number):
                crr[i][j] = round((arr[i][j] * tinh_trong_so(brr)[j]), 4)
        return crr

    # Tính tổng trọng số
    def tinh_tong_trong_so(arr, brr):
        tongTrongSo = []
        for i in range(number):
            tongHang = 0
            for j in range(number):
                tongHang = tongHang + ma_tran_trong_so(arr, brr)[i][j]
            tongTrongSo.append(round(tongHang, 4))
        return tongTrongSo
    
    # Tính vector nhất quán
    def tinh_vector_nhat_quan(arr, brr):
        vectorNhatQuan = []
        for i in range(number):
            vectorHang = tinh_tong_trong_so(arr, brr)[i] / tinh_trong_so(brr)[i]
            vectorNhatQuan.append(round(vectorHang, 4))
        return vectorNhatQuan

    def tinh_lamda_max(arr, brr):
        lamdaMax = 0
        for i in range(number):
            lamdaMax = lamdaMax + tinh_vector_nhat_quan(arr, brr)[i]
        lamdaMax = round((lamdaMax/number), 4)
        return lamdaMax

    def tinh_chi_so_nhat_quan(lamdaMax):
        chiSoNhatQuan = round(((lamdaMax - number) / (number - 1)), 4)
        return chiSoNhatQuan

    def tinh_ty_so_nhat_quan(chiSoNhatQuan):
        tySoNhatQuan = round((chiSoNhatQuan/randomIndex[number]), 4)
        return tySoNhatQuan
    
    arr = input_array()
    tong = tinh_tong(arr)
    brr = chuan_hoa_array(arr)
    trongSoDk = tinh_trong_so(brr)
    crr =  ma_tran_trong_so(arr, brr)
    lamdaMax = tinh_lamda_max(arr, brr)
    chiSoNhatQuan = tinh_chi_so_nhat_quan(lamdaMax)
    tySoNhatQuan = tinh_ty_so_nhat_quan(chiSoNhatQuan)

    return render_template("pa5_CR.html" , number = number, tc = tc, ten_tieu_chi = ten_tieu_chi, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, trongSoCt = trongSoCt, trongSoTb = trongSoTb, arr = arr, tong = tong, brr = brr, trongSoDk = trongSoDk, crr = crr, lamdaMax = lamdaMax, chiSoNhatQuan = chiSoNhatQuan, tySoNhatQuan = tySoNhatQuan)


@app.route("/diem_phuong_an", methods=["POST"])
def diem_phuong_an():
    # ten_tieu_chi = request.form["tc"]
    tc = request.form["tc"].split(", ")
    number = int(request.form["number"])
    trongSo = request.form["trongSo"]
    trongSoTg = request.form["trongSoTg"]
    trongSoMt = request.form["trongSoMt"]
    trongSoCt = request.form["trongSoCt"]
    trongSoTb = request.form["trongSoTb"]
    trongSoDk = request.form["trongSoDk"]

    pa_list = []

    trongSoList = list((trongSo.replace("[", "").replace("]", "")).split(", "))
    FtrongSoList = []
    for i in range(len(trongSoList)):
        FtrongSoList.append(float(trongSoList[i]))

    trongSoTgList = list((trongSoTg.replace("[", "").replace("]", "")).split(", "))
    FtrongSoTgList = []
    for i in range(len(trongSoTgList)):
        FtrongSoTgList.append(float(trongSoTgList[i]))
    pa_list.append(FtrongSoTgList)

    trongSoMtList = list((trongSoMt.replace("[", "").replace("]", "")).split(", "))
    FtrongSoMtList = []
    for i in range(len(trongSoMtList)):
        FtrongSoMtList.append(float(trongSoMtList[i]))
    pa_list.append(FtrongSoMtList)

    trongSoCtList = list((trongSoCt.replace("[", "").replace("]", "")).split(", "))
    FtrongSoCtList = []
    for i in range(len(trongSoCtList)):
        FtrongSoCtList.append(float(trongSoCtList[i]))
    pa_list.append(FtrongSoCtList)

    trongSoTbList = list((trongSoTb.replace("[", "").replace("]", "")).split(", "))
    FtrongSoTbList = []
    for i in range(len(trongSoTgList)):
        FtrongSoTbList.append(float(trongSoTbList[i]))
    pa_list.append(FtrongSoTbList)

    trongSoDkList = list((trongSoDk.replace("[", "").replace("]", "")).split(", "))
    FtrongSoDkList = []
    for i in range(len(trongSoDkList)):
        FtrongSoDkList.append(float(trongSoDkList[i]))
    pa_list.append(FtrongSoDkList)

    arr = [[0 for i in range(5)] for j in range(4)]

    for i in range(len(pa_list)):
        for j in range(len(pa_list[i])):
            arr[j][i] = pa_list[i][j]

    def tinh_diem_so_phuong_an(arr_pa, FtrongSoList):
        diemSoPA = []
        for i in range(4):
            tichMaTran = 0
            for j in range(5):
                tich = arr_pa[i][j] * FtrongSoList[j]
                tichMaTran = round((tichMaTran + tich), 4)

            diemSoPA.append(tichMaTran)
        return diemSoPA

    pa = ['Phương án 1', 'Phương án 2', 'Phương án 3', 'Phương án 4']
    diemSoPA = tinh_diem_so_phuong_an(arr, FtrongSoList)
    
    return render_template("diem_phuong_an.html", pa = pa, diemSoPA = diemSoPA, number = number, tc = tc, trongSo = trongSo, trongSoTg = trongSoTg, trongSoMt = trongSoMt, trongSoCt = trongSoCt, trongSoTb = trongSoTb, trongSoDk = trongSoDk, pa_list = pa_list, FtrongSoList = FtrongSoList, arr = arr)
  
  
if __name__=='__main__':
    app.run(debug=True)