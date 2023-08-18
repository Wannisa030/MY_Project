# เกี่ยวกับรูปภาพ
import cv2
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import csv
# เกี่ยวกับไฟล์
import pandas as pd
import os
import base64
import re
from os import path
from werkzeug.utils import secure_filename
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
# เกี่ยวกับฐานข้อมูล
import pymysql
import json
import mysql.connector
from flask_mysqldb import MySQL
import requests
# เว็บและทั่วไป
from math import ceil
from flask import Flask,render_template,request,redirect,url_for,flash,session,make_response,jsonify, send_file
import datetime
import secrets
import io
import time
import random
import string
# OCR
import pytesseract as tess 
from pytesseract import Output
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#---------- run app ----------
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'img')

#---------- DB config database sql ----------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rov'
}
conn = mysql.connector.connect(**db_config)

#---------- function ----------
# <<<< เกี่ยวกับฐานข้อมูล>>>>
# ดึงข้อมูลชื่อ hero จาก database
def get_dropdown_data_hero():
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # ดึงข้อมูลจากฐานข้อมูล
    query = "SELECT hero_name FROM tb_hero"
    cursor.execute(query)
    result = cursor.fetchall()
    # ปิดการเชื่อมต่อ
    cursor.close()
    conn.close()
    # แปลงผลลัพธ์เป็นลิสต์ของข้อมูล
    dropdown_data_hero = [row[0] for row in result]
    return dropdown_data_hero

# ดึงข้อมูลชื่อ position จาก database
def get_dropdown_data_position():
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # ดึงข้อมูลจากฐานข้อมูล
    query = "SELECT position_name FROM tb_position"
    cursor.execute(query)
    result = cursor.fetchall()
    # ปิดการเชื่อมต่อ
    cursor.close()
    conn.close()
    # แปลงผลลัพธ์เป็นลิสต์ของข้อมูล
    dropdown_data_position = [row[0] for row in result]
    return dropdown_data_position

# ดึงข้อมูลชื่อ player จาก database
def get_dropdown_data_player():
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # ดึงข้อมูลจากฐานข้อมูล
    query = "SELECT name_player FROM tb_player"
    cursor.execute(query)
    result = cursor.fetchall()
    # ปิดการเชื่อมต่อ
    cursor.close()
    conn.close()
    # แปลงผลลัพธ์เป็นลิสต์ของข้อมูล
    dropdown_data_player = [row[0] for row in result]
    return dropdown_data_player

# ดึงข้อมูลชื่อ team จาก database
def get_dropdown_data_team():
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # ดึงข้อมูลจากฐานข้อมูล
    query = "SELECT team_name FROM tb_team"
    cursor.execute(query)
    result = cursor.fetchall()
    # ปิดการเชื่อมต่อ
    cursor.close()
    conn.close()
    # แปลงผลลัพธ์เป็นลิสต์ของข้อมูล
    dropdown_data_team = [row[0] for row in result]
    return dropdown_data_team

# ฟังก์ชันตรวจสอบชื่อผู้เล่นในฐานข้อมูล
def check_name_player(player_name):
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    #ทำการเช็คข้อมูลโดยที่ เมื่อเกิดข้อผิดพลาด ขะไม่หยุดทำงาน
    try:
        query = "SELECT * FROM tb_player WHERE name_player = %s"
        cursor.execute(query, (player_name,))
        result = cursor.fetchone()
        # ปิดการเชื่อมต่อ
        cursor.close()
        conn.close()
        return result is not None
    except mysql.connector.Error as error:
        print("Error while executing query:", error)
        return False
    
# ฟังก์ชันตรวจสอบชื่อผู้เล่นในทีมที่ต้องการบันทึก
def check_player_team(player_name, team_name):
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # ทำการเช็คข้อมูลโดยที่ เมื่อเกิดข้อผิดพลาด ขะไม่หยุดทำงาน
    try:
        # ค้นหา team_id จากตาราง tb_team ที่มีชื่อทีมเหมือนกับ team_name ที่ระบุเข้ามา
        query_team_id = "SELECT team_id FROM tb_team WHERE team_name = %s"
        cursor.execute(query_team_id, (team_name,))
        team_id = cursor.fetchone()
        # ตรวจสอบว่ามีข้อมูลในฐานข้อมูลไหม
        if team_id:
            # หากพบ team_id ในตาราง tb_team
            query = "SELECT * FROM tb_player WHERE name_player = %s AND team_id = %s"
            cursor.execute(query, (player_name, team_id[0]))  # ใช้ team_id ที่ได้จากการค้นหาใน tb_team
            result = cursor.fetchone()
        else:
            # หากไม่พบ team_id ในตาราง tb_team
            result = None
        # ปิดการเชื่อมต่อ
        cursor.close()
        conn.close()
        # ส่งค่าเมื่อไม่พบข้อมูล
        return result is not None
    except mysql.connector.Error as error:
        print("Error while executing query:", error)
        return False

# ฟังก์ชันตรวจสอบชื่อทีมเป็น id
def get_team_id_by_name(cursor, team_name):
    query_team_id = "SELECT team_id FROM tb_team WHERE team_name = %s"
    cursor.execute(query_team_id, (team_name,))
    team_id = cursor.fetchone()
    return team_id[0] if team_id else None

# ฟังก์ชันตรวจสอบชื่อผลคะแนนเป็น id
def get_score_id_by_name(cursor, score_name):
    query_score_id = "SELECT score_id FROM score_result WHERE sc_name = %s"
    cursor.execute(query_score_id, (score_name,))
    score_id = cursor.fetchone()
    return score_id[0] if score_id else None

# ฟังก์ชันตรวจสอบชื่อฮีโร่เป็น id
def get_hero_id_by_name(cursor, hero_name):
    query_hero_id = "SELECT hero_id FROM tb_hero WHERE hero_name = %s"
    cursor.execute(query_hero_id, (hero_name,))
    hero_id = cursor.fetchone()
    return hero_id[0] if hero_id else None

# ฟังก์ชันตรวจสอบชื่อผู้เล่นเป็น id
def get_player_id_by_name(cursor, name_player):
    query_player_id = "SELECT player_id FROM tb_player WHERE name_player = %s"
    cursor.execute(query_player_id, (name_player,))
    player_id = cursor.fetchone()
    return player_id[0] if player_id else None

# ฟังก์ชันตรวจสอบตำแหน่งเป็น id
def get_position_id_by_name(cursor, name_positions):
    query_position_id = "SELECT position_id FROM tb_position WHERE position_name = %s"
    cursor.execute(query_position_id, (name_positions,))
    position_id = cursor.fetchone()
    return position_id[0] if position_id else None

# สร้างฟังก์ชันตรวจสอบสถานะการเข้าสู่ระบบ
def is_logged_in():
    return 'logged_in' in session and session['logged_in']

# <<<< เกี่ยวกับรูป>>>>
# เปลี่ยน file เป็น IMG
def origin(file):
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    return img

# filter details
def dash_details(img):
    #filter blue
    img_color_extract_blue = cv2.inRange(img,np.array([127,0,0]), np.array([255,255,255]))
    #filter red
    img_color_extract_red = cv2.inRange(img,np.array([0,0,127]), np.array([255,255,255]))
    # mix 2 filter
    merge_img = cv2.addWeighted(img_color_extract_blue ,0.6,img_color_extract_red,0.6,1)
    # invert
    diff_img = cv2.bitwise_not(merge_img)
    # filter Noise
    pre_img_result = cv2.adaptiveThreshold(diff_img,255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,50)
    return pre_img_result

# filter statistics
def dash_statistics(img):
    #filter blue
    img_color_extract_blue = cv2.inRange(img,np.array([127,0,0]), np.array([255,255,255]))
    #filter red
    img_color_extract_red = cv2.inRange(img,np.array([0,0,127]), np.array([255,255,255]))
    # mix 2 filter
    merge_img = cv2.addWeighted(img_color_extract_blue, 0.75, img_color_extract_red, 0.75, 1)
    # invert
    diff_img = cv2.bitwise_not(merge_img)
    #create kernel clear noise
    kernel_clear_noise = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    #erode to dark the font
    diff_img_font_bigger = cv2.erode(diff_img, kernel_clear_noise)
    #dark the img
    _, pre_img_result = cv2.threshold(diff_img_font_bigger,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return pre_img_result

# <<<< เกี่ยวกับจัดการรูปแบบข้อมูล >>>>
def generate_random_filename():
    # สร้างชื่อไฟล์สุ่ม
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))

# filter cleaning text
def cleaning_text(text,step,groups,teamA,teamB):
    # กรณีชื่อ
    if step == 0:
        # case player
        result_cleaning = None
        #filter text and number lang thai,japan,china,kao,eng ,france
        filter_text = re.findall("[a-zA-Z\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9fก-๙\d._]+", text)
        #Check the text and combine the text into a sentence.
        if len(filter_text)>1:
            result_cleaning = ''.join(filter_text)
        else:
            if len(filter_text) == 0:
                result_cleaning = ''
            else:
                result_cleaning = filter_text[0]
        #เช็คและจัดการ แบ่งเป็นทีม A,B
        if(groups <= 4):
            for index, key in enumerate(teamA):
                if index == step:
                    teamA[key].append(result_cleaning)
        else:
            for index, key in enumerate(teamA):
                if index == step:
                    teamB[key].append(result_cleaning)
    
    #กรณีที่เป็นเลขจำนวนเต็ม
    elif step > 0 and step < 5 or step in [6,8,10]:
        # filter int number
        result_cleaning = re.findall("\d+",text)
        if len(result_cleaning) > 0:
            result_cleaning = result_cleaning[0]
            #เช็คและจัดการ แบ่งเป็นทีม A,B
            if(groups <= 4):
                for index,key in enumerate(teamA):
                    if index == step:
                        teamA[key].append(result_cleaning)
            else:
                for index, key in enumerate(teamA):
                    if index == step:
                        teamB[key].append(result_cleaning)
        else:
            if(groups <= 4):
                for index, key in enumerate(teamA):
                    if index == step:
                        teamA[key].append('')
            else:
                for index, key in enumerate(teamA):
                    if index == step:
                        teamB[key].append('')

    # กรณีเลขทศนิยม
    else:
        cleaning_text_result = re.findall("[\d+\%]",text)
        result_cleaning = ''
        # ถ้าในข้อความนั้นไม่มี % ให้เพิ่ม % เข้าไป
        if '%' not in cleaning_text_result and len(cleaning_text_result) > 0:
            cleaning_text_result.append('%')
        else:
            for index, value in enumerate(cleaning_text_result):
                if value == '%' and index+1 != len(cleaning_text_result):
                    cleaning_text_result.pop(index)
                    cleaning_text_result.append('%')
        # เช็คตัวเลขที่มีจำนวนมากกว่า 4 ให้ลบ
        if len(cleaning_text_result) > 4:
            cleaning_text_result.pop(0)
        # ใส่จุดทศนิยม
        if(len(cleaning_text_result) > 0):
            cleaning_text_result.insert(-2,".")
            pure_text = ''.join(cleaning_text_result[:-1:])
            try:
                result_cleaning = float(pure_text)
            except ValueError:
                result_cleaning = 0.0
        else:
            result_cleaning = 0.0
        #เช็คและจัดการ แบ่งเป็นทีม A,B
        if(groups <= 4):
            for index, key in enumerate(teamA):
                if index == step:
                    teamA[key].append(result_cleaning)
        else:
            for index, key in enumerate(teamA):
                if index == step:
                    teamB[key].append(result_cleaning)

#---------- Display ----------
#---------- Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
            # สร้างคำสั่ง SQL 
            with conn.cursor() as cur:
                sql = "SELECT * FROM tb_user WHERE username=%s AND password=%s"
                cur.execute(sql, (username, password))
                user = cur.fetchone()
            # เช็คเงื่อนไข 
            if user:
                session['logged_in'] = True
                return {'message': 'Login successful'}
            else:
                return {'error': 'Invalid credentials'}, 401
        except Exception as e:
            return {'error': 'An error occurred'}, 500
    return render_template('login.html')

# ---------- Display Logout
@app.route('/logout')
def logout():
    # ทำการล็อกเอาท์และลบสถานะการเข้าสู่ระบบออกจาก session
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# ---------- Display profile
@app.route('/profile')
def profile():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
                cur.execute("SELECT * FROM tb_user")
                user = cur.fetchone()

    return render_template('profile.html', user=user,)

# ---------- Display update_profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    user_id = request.form['user_id']
    username = request.form['username']
    password = request.form['password']
    
    # ตรวจสอบความยาวของรหัสผ่าน
    if len(password) < 8:
        return jsonify({"message": "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร", "status": "error"})

    # อัปเดตข้อมูลในฐานข้อมูล
    with conn.cursor() as cur:
        sql = """
            UPDATE tb_user
            SET username = %s, password = %s
            WHERE user_id = %s;
        """

        cur.execute(sql, (username, password, user_id))
        # บันทึกการเปลี่ยนแปลงในฐานข้อมูล
        conn.commit()

    # เพิ่มข้อความแจ้งเตือนในฝั่งของ Flask
    return jsonify({"message": "บันทึกข้อมูลสำเร็จ", "status": "success"})


#---------- Display main 
@app.route("/")
def index():
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                        tb.team_name AS team_name,
                        SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) AS count_2_in_team,
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END) AS count_3_in_team,
                        (SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) + 
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END)) AS total_count
                    FROM (
                        SELECT team_a AS team, resultsA AS results_2, resultsA AS results_3 FROM tb_result
                        UNION ALL
                        SELECT team_b AS team, resultsB AS results_2, resultsB AS results_3 FROM tb_result
                    ) AS trA
                    LEFT JOIN tb_team tb ON trA.team = tb.team_id
                    WHERE trA.results_2 = 2 OR trA.results_3 = 3
                    GROUP BY tb.team_name;
                    """)
        rows = cur.fetchall()
    # ตรวจสอบสถานะการเข้าสู่ระบบและกำหนดค่าให้กับตัวแปร logged_in
    logged_in = 'logged_in' in session and session['logged_in']
    return render_template('index.html', data=rows, logged_in=logged_in)

# ---------- Display สมาชิกทั้งหมด
@app.route("/teammem")
def teammem():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                        p.player_id, p.name, p.surname, p.name_player, p.id_gameplayer, 
                        t.team_name, s.school_name FROM tb_player p 
                        JOIN tb_team t ON p.team_id = t.team_id 
                        JOIN tb_schools s ON p.school_id = s.school_id 
                        """)
        rows = cur.fetchall()       
        cur.execute("SELECT school_name FROM tb_schools")
        result = cur.fetchall()
        school_names = [row[0] for row in result]
        cur.execute("SELECT team_name FROM tb_team")
        result = cur.fetchall()
        team_names = [row[0] for row in result]
        logged_in = session.get('logged_in', False)

        return render_template('team-member.html', data=rows, logged_in=logged_in,school_names=school_names, team_names=team_names)

#---------- Display ฟอร์มเพิ่มสมาชิก    
@app.route("/add")
def add():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    # รับค่า team_name และ school_name จาก Query Parameter ถ้าไม่มีให้ใช้ค่าเริ่มต้น
    team_name = request.args.get('team_name', 'default_team_name')
    school_name = request.args.get('school_name', 'default_school_name')

    # กรองข้อมูลที่ตรงกับทีมและโรงเรียนที่เลือกเก็บไว้ในตัวแปร filtered_data
    with conn.cursor() as cur:
        cur.execute("""SELECT p.player_id, p.name, p.surname, p.name_player, p.id_gameplayer, t.team_name, 
                    s.school_name FROM tb_player p 
                    JOIN tb_team t ON p.team_id = t.team_id 
                    JOIN tb_schools s ON p.school_id = s.school_id 
                    WHERE t.team_name = %s AND s.school_name = %s""", (team_name, school_name))
        
        rows = cur.fetchall()

        cur.execute("SELECT school_name FROM tb_schools")
        result = cur.fetchall()
        school_names = [row[0] for row in result]
        
        cur.execute("SELECT team_name FROM tb_team")
        result = cur.fetchall()
        team_names = [row[0] for row in result]

        logged_in = session.get('logged_in', False)
    # ส่งข้อมูลที่กรองแล้วไปยังหน้า addmember.html
    return render_template('addmember.html', logged_in=logged_in,team_name=team_name, school_name=school_name, data=rows, team_names=team_names, school_names=school_names)


#---------- Display ฟอร์มเพิ่มสมาชิก
@app.route("/insert", methods=['POST'])
def insert():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        name_player = request.form.get("name_player")
        id_gameplayer = request.form.get("id_gameplayer")
        team_name = request.form.get("team_name")
        school_name = request.form.get("school_name")

        with conn.cursor() as cur:
            # ตรวจสอบว่าทีมมีอยู่ในฐานข้อมูลหรือไม่
            cur.execute("SELECT COUNT(*) FROM tb_team WHERE team_name = %s", (team_name,))
            exists_team = cur.fetchone()[0]

            # ตรวจสอบว่าโรงเรียนมีอยู่ในฐานข้อมูลหรือไม่
            cur.execute("SELECT COUNT(*) FROM tb_schools WHERE school_name = %s", (school_name,))
            exists_school = cur.fetchone()[0]

            if not exists_team:
                # ทีมไม่มีอยู่ในฐานข้อมูล แสดง SweetAlert2 เตือน
                return jsonify({"message": "ไม่พบทีมที่เลือกในระบบ กรุณาเลือกทีมใหม่", "status": "warning"})

            if not exists_school:
                # โรงเรียนไม่มีอยู่ในฐานข้อมูล แสดง SweetAlert2 เตือน
                return jsonify({"message": "ไม่พบโรงเรียนที่เลือกในระบบ กรุณาเลือกโรงเรียนใหม่", "status": "warning"})

            # ดึง team_id และ school_id จากตาราง tb_team และ tb_schools โดยใช้ชื่อทีมและโรงเรียน
            cur.execute("SELECT team_id FROM tb_team WHERE team_name = %s", (team_name,))
            team_id = cur.fetchone()[0]

            cur.execute("SELECT school_id FROM tb_schools WHERE school_name = %s", (school_name,))
            school_id = cur.fetchone()[0]

            # เพิ่มข้อมูลผู้เล่นในตาราง tb_player
            sql = "INSERT INTO tb_player (name, surname, name_player, id_gameplayer, team_id, school_id) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (name, surname, name_player, id_gameplayer, team_id, school_id)
            cur.execute(sql, data)
            conn.commit()

        # กลับไปที่ URL ของหน้า add และส่งค่า team_name และ school_name กลับไปด้วย
        return redirect(url_for('add', team_name=team_name, school_name=school_name))

#---------- Display ลบสมาชิก
@app.route("/delete/<int:player_id>", methods=["DELETE"])
def delete(player_id):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
        sql = """
            DELETE FROM tb_player
            WHERE player_id = %s
        """
        cur.execute(sql, (player_id,))
        conn.commit()

    return jsonify({"message": "ลบสมาชิกสำเร็จ", "status": "success"})

#---------- Display อัปเดตplayer    
@app.route('/update', methods=['POST'])
def update():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    player_id = request.form['player_id']
    name = request.form['name']
    surname = request.form['surname']
    name_player = request.form['name_player']
    id_gameplayer = request.form['id_gameplayer']
    team_name = request.form['team_name']
    school_name = request.form['school_name']

    # อัปเดตข้อมูลในฐานข้อมูล
    with conn.cursor() as cur:
        sql = """
            UPDATE tb_player
            SET name = %s, surname = %s, name_player = %s, id_gameplayer = %s,
                team_id = (SELECT team_id FROM tb_team WHERE team_name = %s),
                school_id = (SELECT school_id FROM tb_schools WHERE school_name = %s)
            WHERE player_id = %s
        """

        cur.execute(sql, (name, surname, name_player, id_gameplayer, team_name, school_name, player_id))
                # บันทึกการเปลี่ยนแปลงในฐานข้อมูล
        conn.commit()

    # เพิ่มข้อความแจ้งเตือนในฝั่งของ Flask
    return jsonify({"message": "แก้ไขข้อมูลสำเร็จ", "status": "success"})

#---------- Display ทีม
@app.route("/team")
def team():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tb_team")
        rows = cur.fetchall()

        logged_in = session.get('logged_in', False)
    return render_template('team.html', data=rows,logged_in=logged_in)

#---------- Display สมาชิกในทีม
@app.route('/member/<team_name>')
def member(team_name):
    with conn.cursor() as cur:
        # แก้ไข SQL โดยใช้ JOIN เพื่อรวมข้อมูลจาก tb_player, tb_team, และ tb_schools
        cur.execute("""
                        SELECT
                            p.name,
                            p.surname,
                            p.name_player,
                            p.id_gameplayer,
                            s.school_name,
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2,
                                (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name, 
                            ROUND(AVG(b.kill), 1) AS avg_kill,
                            ROUND(AVG(b.dead), 1) AS avg_dead,
                            ROUND(AVG(b.assist), 1) AS avg_assist,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio,
                            ROUND(AVG(b.money), 1) AS avg_money,
                            ROUND(AVG(b.point), 1) AS avg_point,
                            ROUND(AVG(b.mvp), 0) AS avg_mvp,
                            ROUND(AVG(b.damage), 1) AS avg_damage,
                            ROUND(AVG(b.damage_), 1) AS avg_damage_,
                            ROUND(AVG(b.take_damage), 1) AS avg_take_damage,
                            ROUND(AVG(b.take_damage_), 1) AS avg_take_damage_,
                            ROUND(AVG(b.teamfight), 1) AS avg_teamfight,
                            ROUND(AVG(b.teamfight_), 1) AS avg_teamfight_,
                            (
                                SELECT h.hero_name
                                FROM tb_match
                                INNER JOIN tb_hero AS h ON tb_match.hero_id = h.hero_id 
                                WHERE player_id = p.player_id
                                GROUP BY h.hero_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_hero_name
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        INNER JOIN tb_schools AS s ON p.school_id = s.school_id
                        WHERE t.team_name = %s
                        GROUP BY p.name, p.surname, p.name_player, p.id_gameplayer, s.school_name

                    """, (team_name,))
        rows = cur.fetchall()
        logged_in = session.get('logged_in', False)
    return render_template('member.html', data=rows, logged_in=logged_in,team_name=team_name)

#---------- Display ทีมad
@app.route("/teamad")
def teamad():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
        cur.execute("SELECT t.team_id, t.team_name, s.school_name FROM tb_team t JOIN tb_schools s ON t.school_id = s.school_id")
        rows = cur.fetchall()
        
        cur.execute("SELECT school_name FROM tb_schools")
        result = cur.fetchall()
        school = [row[0] for row in result]
        return render_template('teamad.html', data=rows, school=school)

#---------- Display เพิ่มทีม
@app.route("/addt", methods=["POST"])
def addt():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    team_name = request.form.get("team_name")
    school_name = request.form.get("school_name")

    with conn.cursor() as cur:
        # ตรวจสอบว่าทีมมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_team WHERE team_name = %s", (team_name,))
        exists = cur.fetchone()[0]

        if exists:
            # ทีมมีอยู่แล้ว แสดง SweetAlert2 เตือน
            return jsonify({"message": "ชื่อทีมนี้มีอยู่ในระบบแล้ว", "status": "warning"})

        # ตรวจสอบว่าโรงเรียนมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_schools WHERE school_name = %s", (school_name,))
        exists_school = cur.fetchone()[0]

        if not exists_school:
            # ไม่พบโรงเรียนที่เลือกในฐานข้อมูล แสดง SweetAlert2 เตือน
            return jsonify({"message": "โรงเรียนที่เลือกไม่มีในระบบ กรุณาเลือกโรงเรียนใหม่", "status": "warning"})

        # เพิ่มข้อมูลทีมลงในฐานข้อมูล
        sql_insert = "INSERT INTO tb_team (team_name, school_id) VALUES (%s, (SELECT school_id FROM tb_schools WHERE school_name = %s))"
        data_insert = (team_name, school_name)
        cur.execute(sql_insert, data_insert)
        conn.commit()

        # เพิ่มทีมสำเร็จ แสดง SweetAlert2 สำเร็จ
        return jsonify({"message": "เพิ่มทีมสำเร็จ", "status": "success"})

#---------- Display แก้ไขทีม
@app.route('/updatet', methods=['POST'])
def updatet():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    team_id = request.form['team_id']
    team_name = request.form['team_name']
    school_name = request.form['school_name']

    with conn.cursor() as cur:
        # ตรวจสอบว่าทีมมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_team WHERE team_id = %s", (team_id,))
        exists = cur.fetchone()[0]

        if not exists:
            # ไม่พบทีมที่ต้องการอัปเดต แสดง SweetAlert2 เตือน
            return jsonify({"message": "ไม่พบทีมที่ต้องการอัปเดต", "status": "warning"})

        # ตรวจสอบว่าโรงเรียนมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_schools WHERE school_name = %s", (school_name,))
        exists_school = cur.fetchone()[0]

        if not exists_school:
            # ไม่พบโรงเรียนที่เลือกในฐานข้อมูล แสดง SweetAlert2 เตือน
            return jsonify({"message": "โรงเรียนที่เลือกไม่มีในระบบ กรุณาเลือกโรงเรียนใหม่", "status": "warning"})

        # อัปเดตข้อมูลทีมในตาราง tb_team
        sql_update_team = "UPDATE tb_team SET team_name = %s, school_id = (SELECT school_id FROM tb_schools WHERE school_name = %s) WHERE team_id = %s"
        data_update_team = (team_name, school_name, team_id)
        cur.execute(sql_update_team, data_update_team)

        # อัปเดต school_id ของผู้เล่นในตาราง tb_player
        sql_update_player = "UPDATE tb_player SET school_id = (SELECT school_id FROM tb_schools WHERE school_name = %s) WHERE team_id = %s"
        data_update_player = (school_name, team_id)
        cur.execute(sql_update_player, data_update_player)

        conn.commit()

    # เพิ่มข้อความแจ้งเตือนในฝั่งของ Flask
    return jsonify({"message": "แก้ไขข้อมูลสำเร็จ", "status": "success"})

#---------- Display ลบทีม
@app.route("/deletet/<int:team_id>", methods=["DELETE"])
def deletet(team_id):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
        sql = """
            DELETE FROM tb_player 
            WHERE team_id = %s
        """
        cur.execute(sql, (team_id,))

        sql = """
            DELETE FROM tb_team
            WHERE team_id = %s
        """
        cur.execute(sql, (team_id,))
        conn.commit()

    return jsonify({"message": "ลบทีมสำเร็จ", "status": "success"})

#---------- Display โรงเรียน
@app.route("/school")
def school():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tb_schools")
        rows = cur.fetchall()
        
        cur.execute("SELECT name_th FROM provinces")
        result = cur.fetchall()
        provinces = [row[0] for row in result]

        return render_template('school.html', data=rows, provinces=provinces)

#---------- Display เพิ่มโรงเรียน
@app.route("/addsc", methods=["POST"])
def addsc():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    school_name = request.form.get("school_name")
    city = request.form.get("city")

    with conn.cursor() as cur:
        # ตรวจสอบว่าโรงเรียนมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_schools WHERE school_name = %s", (school_name,))
        exists = cur.fetchone()[0]

        if exists:
            # โรงเรียนมีอยู่แล้ว แสดง SweetAlert2 เตือน
            return jsonify({"message": "โรงเรียนนี้มีอยู่ในระบบแล้ว", "status": "warning"})

        # เพิ่มข้อมูลโรงเรียนลงในฐานข้อมูล
        sql_insert = "INSERT INTO tb_schools (school_name, city) VALUES (%s, %s)"
        data_insert = (school_name, city)
        cur.execute(sql_insert, data_insert)
        conn.commit()

        # เพิ่มโรงเรียนสำเร็จ แสดง SweetAlert2 สำเร็จ
        return jsonify({"message": "เพิ่มโรงเรียนสำเร็จ", "status": "success"})
    
#---------- Display แก้ไขโรงเรียน
@app.route('/updatesc', methods=['POST'])
def updatesc():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    school_id = request.form['school_id']
    school_name = request.form['school_name']
    city = request.form['city']

    with conn.cursor() as cur:
        # ตรวจสอบว่าโรงเรียนมีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_schools WHERE school_name = %s AND school_id != %s", (school_name, school_id))
        exists = cur.fetchone()[0]

        if exists:
            # โรงเรียนมีอยู่แล้ว แสดง SweetAlert2 เตือน
           return jsonify({"message": "ชื่อโรงเรียนซ้ำ กรุณาตรวจสอบข้อมูล", "status": "warning"})

          
        sql = """
            UPDATE tb_schools
            SET school_name = %s, city = %s
            WHERE school_id = %s
        """
        data = (school_name, city, school_id)
        cur.execute(sql, data)
        conn.commit()

    # เพิ่มข้อความแจ้งเตือนในฝั่งของ Flask
    return jsonify({"message": "แก้ไขข้อมูลสำเร็จ", "status": "success"})

#---------- Display ลบโรงเรียน
@app.route("/deletesc/<int:school_id>", methods=["DELETE"])
def deletesc(school_id):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    with conn.cursor() as cur:
        sql = """
            DELETE FROM tb_player
            WHERE school_id = %s
        """
        cur.execute(sql, (school_id,))
        sql = """
            DELETE FROM tb_team
            WHERE school_id = %s
        """
        cur.execute(sql, (school_id,))

        sql = """
            DELETE FROM tb_schools
            WHERE school_id = %s
        """
        cur.execute(sql, (school_id,))
        conn.commit()

    return jsonify({"message": "ลบโรงเรียนสำเร็จ", "status": "success"})

#---------- Display กติกา ad
@app.route('/rulec')
def rulec():
    filenames = ['rule_1.jpg', 'rule_2.jpg', 'rule_3.jpg', 'rule_4.jpg', 'rule_5.jpg', 'rule_6.jpg', 'rule_7.jpg', 'rule_8.jpg', 'rule_9.jpg', 'rule_10.jpg']  # ใส่รายชื่อของรูปภาพที่อัปโหลดมา
    # กรองรูปภาพที่มีอยู่จริงในรายการ filenames
    existing_filenames = [filename for filename in filenames if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))]

    logged_in = 'logged_in' in session and session['logged_in']
    return render_template('rule_copy.html', logged_in=logged_in,filenames=existing_filenames)

#---------- Display กติกา
@app.route('/rule')
def rule():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:    
        return redirect(url_for('login'))
    filenames = ['rule_1.jpg', 'rule_2.jpg', 'rule_3.jpg', 'rule_4.jpg', 'rule_5.jpg', 'rule_6.jpg', 'rule_7.jpg', 'rule_8.jpg', 'rule_9.jpg', 'rule_10.jpg']
    existing_filenames = [filename for filename in filenames if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))]

    return render_template('rule.html', filenames=existing_filenames)

#---------- Display รูปกติกา
@app.route('/upload_img_add_rule', methods=['GET', 'POST'])
def upload_img_add_rule():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # ตรวจสอบว่ามีไฟล์ที่อัปโหลดหรือไม่
        if 'file' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('file')  # รับภาพทั้งหมดที่อัปโหลดมา
        filenames = []  # เก็บชื่อไฟล์ภาพที่บันทึก

        for idx, file in enumerate(files, start=1):
            if file:
                # ตรวจสอบจำนวนรูปภาพที่อัปโหลด ห้ามเกิน 10 รูป
                if idx > 10:
                    flash('คุณสามารถอัปโหลดรูปภาพได้ไม่เกิน 10 รูป')
                    break

                # สร้างชื่อไฟล์
                filename = f'rule_{idx}.jpg'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                filenames.append(filename)

        return render_template('rule.html', filenames=filenames)
    return redirect(url_for('rule'))
    
#---------- Display ลบรูปกติกา
@app.route('/delete_image_rule/<filename>', methods=['DELETE'])
def delete_image_rule(filename):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    try:
        # ลบไฟล์รูปภาพ
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(filepath)
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}
    
#---------- Display ตารางการแข่งขัน ad
@app.route('/schedulec')
def schedulec():
    filenames = ['schedule_1.jpg', 'schedule_2.jpg', 'schedule_3.jpg', 'schedule_4.jpg', 'schedule_5.jpg', 'schedule_6.jpg', 'schedule_7.jpg', 'schedule_8.jpg', 'schedule_9.jpg', 'schedule_10.jpg']  # ใส่รายชื่อของรูปภาพที่อัปโหลดมา
    # กรองรูปภาพที่มีอยู่จริงในรายการ filenames
    existing_filenames = [filename for filename in filenames if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))]

    logged_in = 'logged_in' in session and session['logged_in']

    return render_template('schedule_copy.html', logged_in=logged_in,filenames=existing_filenames)

#---------- Display ตารางการแข่งขัน
@app.route('/schedule')
def schedule():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    filenames = ['schedule_1.jpg', 'schedule_2.jpg', 'schedule_3.jpg', 'schedule_4.jpg', 'schedule_5.jpg', 'schedule_6.jpg', 'schedule_7.jpg', 'schedule_8.jpg', 'schedule_9.jpg', 'schedule_10.jpg']  # ใส่รายชื่อของรูปภาพที่อัปโหลดมา
    # กรองรูปภาพที่มีอยู่จริงในรายการ filenames
    existing_filenames = [filename for filename in filenames if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))]

    return render_template('schedule.html', filenames=existing_filenames)

#---------- Display รูปตารางการแข่งขัน
@app.route('/upload_img_add_schedule',  methods=['GET','POST'])
def upload_img_add_schedule():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # ตรวจสอบว่ามีไฟล์ที่อัปโหลดหรือไม่
        if 'file' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('file')  # รับภาพทั้งหมดที่อัปโหลดมา
        filenames = []  # เก็บชื่อไฟล์ภาพที่บันทึก

        for idx, file in enumerate(files, start=1):
            if file:
                # สร้างชื่อไฟล์
                filename = f'schedule_{idx}.jpg'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                filenames.append(filename)

                # หยุดการบันทึกหากถึงภาพที่ 10
                if idx == 10:
                    break

        return render_template('schedule.html', filenames=filenames)

#---------- Display ลบรูปตารางการแข่งขัน
@app.route('/delete_image_schedule/<filename>', methods=['DELETE'])
def delete_image_schedule(filename):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    try:
        # ลบไฟล์รูปภาพ
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(filepath)
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}

#---------- Display Hero
@app.route('/hero')
def hero():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor () as cur:
        cur =conn.cursor()
        cur.execute("SELECT * FROM tb_hero GROUP BY hero_name")
        rows=cur.fetchall()
      
    return render_template('hero.html',data=rows)

#---------- Display เพิ่มHero
@app.route("/addhero", methods=["POST"])
def addhero():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    hero_name = request.form.get("hero_name")

    with conn.cursor() as cur:
        # ตรวจสอบว่า hero มีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_hero WHERE hero_name = %s", (hero_name,))
        exists = cur.fetchone()[0]

        if exists:
            # hero มีอยู่แล้ว แสดง SweetAlert2 เตือน
            return jsonify({"message": "hero นี้มีอยู่ในระบบแล้ว", "status": "warning"})

        # เพิ่มข้อมูล hero ลงในฐานข้อมูล
        sql_insert = "INSERT INTO tb_hero (hero_name) VALUES ( %s)"
        data_insert = (hero_name)
        cur.execute(sql_insert, data_insert)
        conn.commit()

        # เพิ่ม hero สำเร็จ แสดง SweetAlert2 สำเร็จ
        return jsonify({"message": "เพิ่ม hero สำเร็จ", "status": "success"})

#---------- Display แก้ไขHero
@app.route('/updatehero', methods=['POST'])
def updatehero():
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    hero_id = request.form['hero_id']
    hero_name = request.form['hero_name']

    with conn.cursor() as cur:
        # ตรวจสอบว่า hero มีอยู่ในฐานข้อมูลหรือไม่
        cur.execute("SELECT COUNT(*) FROM tb_hero WHERE hero_name = %s AND hero_id != %s", (hero_name, hero_id))
        exists = cur.fetchone()[0]

        if exists:
            #  hero มีอยู่แล้ว แสดง SweetAlert2 เตือน
           return jsonify({"message": "ชื่อ hero ซ้ำ กรุณาตรวจสอบข้อมูล", "status": "warning"})
        sql = """
            UPDATE tb_hero
            SET hero_name = %s
            WHERE hero_id = %s
        """
        data = (hero_name, hero_id)
        cur.execute(sql, data)
        conn.commit()

    # เพิ่มข้อความแจ้งเตือนในฝั่งของ Flask
    return jsonify({"message": "แก้ไขข้อมูลสำเร็จ", "status": "success"})

#---------- Display ลบHero
@app.route("/deletehero/<int:hero_id>", methods=["DELETE"])
def deletehero(hero_id):
        # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor() as cur:
        sql = """
            DELETE FROM tb_hero
            WHERE hero_id = %s
        """
        cur.execute(sql, (hero_id,))
        conn.commit()

    return jsonify({"message": "ลบ Hero สำเร็จ", "status": "success"})

#---------- Display ออกรายงาน
@app.route("/report")
def report():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    with conn.cursor () as cur:
        # ดึงข้อมูลจากตารางtb_player
        sql1 = """SELECT 
                        p.player_id, p.name, p.surname, p.name_player, p.id_gameplayer, 
                        t.team_name, s.school_name FROM tb_player p 
                        JOIN tb_team t ON p.team_id = t.team_id 
                        JOIN tb_schools s ON p.school_id = s.school_id 
                        """
        cur.execute(sql1)
        data1 = cur.fetchall()

        # ดึงข้อมูลจากตาราง tb_schools
        sql2 = "SELECT * FROM tb_schools"
        cur.execute(sql2)
        data2 = cur.fetchall()

        #ดึงข้อมูลจากตาราง tb_team
        sql3 = """SELECT t.team_id, t.team_name, s.school_name 
                    FROM tb_team t JOIN tb_schools s 
                    ON t.school_id = s.school_id
                    """
        
        cur.execute(sql3)
        data3 = cur.fetchall()

        # รายละเอียดการแข่งขัน
        sql4 ="""SELECT
                    a.name_player,
                    b.kill,
                    b.dead,
                    b.assist,
                    ROUND((b.kill + b.dead) / b.assist, 1) AS ratio,
                    b.money,
                    b.point,
                    b.mvp,
                    b.damage,
                    b.damage_,
                    b.take_damage,
                    b.take_damage_,
                    b.teamfight,
                    b.teamfight_
                FROM tb_player AS a
                INNER JOIN tb_match AS b
                ON a.player_id = b.player_id
               """
        cur.execute(sql4)
        data4 = cur.fetchall()

        # สรุปรวมรายละเอียดการแขงขันของผู้เข้าแข่งขัน
        sql5 = """SELECT
                            p.name_player,
                            (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name, 
                            ROUND(AVG(b.kill), 1) AS avg_kill,
                            ROUND(AVG(b.dead), 1) AS avg_dead,
                            ROUND(AVG(b.assist), 1) AS avg_assist,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio,
                            ROUND(AVG(b.money), 1) AS avg_money,
                            ROUND(AVG(b.point), 1) AS avg_point,
                            ROUND(AVG(b.mvp), 0) AS avg_mvp,
                            ROUND(AVG(b.damage), 1) AS avg_damage,
                            ROUND(AVG(b.damage_), 1) AS avg_damage_,
                            ROUND(AVG(b.take_damage), 1) AS avg_take_damage,
                            ROUND(AVG(b.take_damage_), 1) AS avg_take_damage_,
                            ROUND(AVG(b.teamfight), 1) AS avg_teamfight,
                            ROUND(AVG(b.teamfight_), 1) AS avg_teamfight_,
                             (
                                SELECT h.hero_name
                                FROM tb_match
                                INNER JOIN tb_hero AS h ON tb_match.hero_id = h.hero_id 
                                WHERE player_id = p.player_id
                                GROUP BY h.hero_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_hero_name,  
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2                            
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        GROUP BY p.name_player
                        ORDER BY avg_ratio DESC;
                    """
        cur.execute(sql5)
        data5 = cur.fetchall()

        # เปรียบเทียบผู้เข้าแข่งขันที่เล่นตำแหน่งเดียวกัน
        sql6 = """SELECT
                            p.name_player,
                            (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name,
                            ROUND(AVG(b.kill), 1) AS avg_kill,
                            ROUND(AVG(b.dead), 1) AS avg_dead,
                            ROUND(AVG(b.assist), 1) AS avg_assist,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio,
                            ROUND(AVG(b.mvp), 0) AS avg_mvp,
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2,
                            ROUND((COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) / COUNT(*)) * 100, 1)
                            AS win_2_percentage
                            
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        GROUP BY p.name_player
                        ORDER BY avg_ratio DESC;

                        
                    """
        cur.execute(sql6)
        data6 = cur.fetchall()
        # อัตราการชนะของฮีโร่ที่ผู้เข้าแข่งขันใช้แข่งขัน
        sql7 = """SELECT
                    h.hero_name,
                    ROUND(AVG((m.kill + m.dead) / m.assist), 1) AS kda_ratio,
                    SUM(CASE WHEN m.win = 2 THEN 1 ELSE 0 END) AS count_win_2,
                    ROUND((SUM(CASE WHEN m.win = 2 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 1) 
                    AS win_percentage_2_vs_total,
                    COUNT(*) AS total_matches
                FROM tb_match AS m
                INNER JOIN tb_hero AS h ON m.hero_id = h.hero_id
                GROUP BY h.hero_name
                ORDER BY count_win_2 DESC, win_percentage_2_vs_total DESC;
                """
        
        cur.execute(sql7)
        data7 = cur.fetchall()
        # ตารางผลการแข่งขัน
        sql8 = """SELECT 
                        tb.team_name AS team,
                        SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) AS count_2_in_team,
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END) AS count_3_in_team,
                        (SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) + 
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END)) AS total_count
                    FROM (
                        SELECT team_a AS team, resultsA AS results_2, resultsA AS results_3 FROM tb_result
                        UNION ALL
                        SELECT team_b AS team, resultsB AS results_2, resultsB AS results_3 FROM tb_result
                    ) AS trA
                    LEFT JOIN tb_team tb ON trA.team = tb.team_id
                    WHERE trA.results_2 = 2 OR trA.results_3 = 3
                    GROUP BY tb.team_name
                    ORDER BY count_2_in_team DESC;
                    """
        cur.execute(sql8)
        data8 = cur.fetchall()

        tableSelect = request.form.get("tableSelect", "school")  # ถ้าไม่ได้เลือกตารางใดเลย ให้เลือกตาราง school เป็นค่าเริ่มต้น

        return render_template('report.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7,data8=data8,tableSelect=tableSelect)

#---------- Display download-team
@app.route('/download_team')
def download_team():
    with conn.cursor() as cur:
        cur.execute("SELECT t.team_id, t.team_name, s.school_name FROM tb_team t JOIN tb_schools s ON t.school_id = s.school_id")
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=["team_id", "team_name", "school_name"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["team_name","school_name"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "team_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "team_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"team_id_sequence": "ลำดับ", "team_name": "ชื่อทีม", "school_name": "โรงเรียน"}, inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "team_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)

#---------- Display download-player
@app.route('/download_player')
def download_player():
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                        p.player_id, p.name, p.surname, p.name_player, p.id_gameplayer, 
                        t.team_name, s.school_name FROM tb_player p 
                        JOIN tb_team t ON p.team_id = t.team_id 
                        JOIN tb_schools s ON p.school_id = s.school_id 
                        """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=["player_id", "name", "surname","name_player","id_gameplayer","school_name","team_name"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = [ "name","surname","name_player","id_gameplayer","team_name"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "player_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "player_id_sequence", range(1, len(df) + 1))
    
    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"player_id_sequence": "ลำดับ", "name": "ชื่อ", "surname": "นามสกุล", "name_player": "ชื่อที่ใช้ในการแข่งขัน", 
                       "id_gameplayer": "ID ที่ใช้ในการแข่งขัน", "team_name": "ทีม"}, inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "player_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)

#---------- Display download-school
@app.route('/download_school')
def download_school():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tb_schools")
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=["school_id", "school_name", "city"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = [ "school_name","city"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "school_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "school_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"school_id_sequence": "ลำดับ", "school_name": "ชื่อโรงเรียน", "city": "จังหวัด"}, inplace=True)


    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "school_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)
    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)



#---------- Display download-result
@app.route('/download_result')
def download_result():
    with conn.cursor() as cur:
        cur.execute("""SELECT
                    a.name_player,
                    b.kill,
                    b.dead,
                    b.assist,
                    ROUND((b.kill + b.dead) / b.assist, 1) AS ratio,
                    b.money,
                    b.point,
                    b.mvp,
                    b.damage,
                    b.damage_,
                    b.take_damage,
                    b.take_damage_,
                    b.teamfight,
                    b.teamfight_
                FROM tb_player AS a
                INNER JOIN tb_match AS b
                ON a.player_id = b.player_id
               """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=[ "name_player", "kill","dead","assist","ratio",
                                     "money","point","mvp","damage","damage_","take_damage","take_damage_",
                                     "teamfight","teamfight_"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["name_player", "kill","dead","assist","ratio","money","point","mvp","damage","damage_",
                        "take_damage","take_damage_","teamfight","teamfight_"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "school_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "result_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"result_id_sequence": "ลำดับ", "name_player": "ชื่อผู้เล่น", "kill": "kill", "dead": "dead", 
                       "assist": "assist", "ratio": "KDA", "money": "money", "point": "point","mvp": "mvp",
                       "damage": "damage", "damage_": "damage%", "take_damage": "take_damage",
                       "take_damage_": "take_damage%", "teamfight": "teamfight", "teamfight_": "teamfight%"}, inplace=True)


    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "result_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)
#---------- Display download-result
@app.route('/download_result_details')
def download_result_details():
    with conn.cursor() as cur:
        cur.execute("""SELECT
                            p.name_player,
                            (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name, 
                            (
                                SELECT h.hero_name
                                FROM tb_match
                                INNER JOIN tb_hero AS h ON tb_match.hero_id = h.hero_id 
                                WHERE player_id = p.player_id
                                GROUP BY h.hero_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_hero_name,                   
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2,
                            ROUND(AVG(b.kill), 1) AS avg_kill,
                            ROUND(AVG(b.dead), 1) AS avg_dead,
                            ROUND(AVG(b.assist), 1) AS avg_assist,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio,
                            ROUND(AVG(b.money), 1) AS avg_money,
                            ROUND(AVG(b.point), 1) AS avg_point,
                            ROUND(AVG(b.mvp), 0) AS avg_mvp,
                            ROUND(AVG(b.damage), 1) AS avg_damage,
                            ROUND(AVG(b.damage_), 1) AS avg_damage_,
                            ROUND(AVG(b.take_damage), 1) AS avg_take_damage,
                            ROUND(AVG(b.take_damage_), 1) AS avg_take_damage_,
                            ROUND(AVG(b.teamfight), 1) AS avg_teamfight,
                            ROUND(AVG(b.teamfight_), 1) AS avg_teamfight_
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        GROUP BY p.name_player
                    """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=[ "name_player","most_common_position_name","most_common_hero_name",
                                     "count_win_2", "avg_kill","avg_dead","avg_assist","avg_ratio",
                                     "avg_money","avg_point","avg_mvp","avg_damage","avg_damage_",
                                     "avg_take_damage","avg_take_damage_","avg_teamfight","avg_teamfight_"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["name_player","most_common_position_name","most_common_hero_name",
                                     "count_win_2", "avg_kill","avg_dead","avg_assist","avg_ratio",
                                     "avg_money","avg_point","avg_mvp","avg_damage","avg_damage_",
                                     "avg_take_damage","avg_take_damage_","avg_teamfight","avg_teamfight_"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "school_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "result_detailsid_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"result_details_id_sequence": "ลำดับ", "name_player": "ชื่อผู้เล่น","most_common_position_name": "ตำแหน่ง","most_common_hero_name": "Hero ที่ใช้บ่อย","count_win_2": "ชนะ", "avg_kill": "kill", "avg_dead": "dead", 
                       "avg_assist": "assist", "avg_ratio": "KDA", "avg_money": "money", "avg_point": "point","avg_mvp": "mvp",
                       "damage": "damage", "damage_": "damage%", "take_damage": "take_damage",
                       "avg_take_damage_": "take_damage%", "avg_teamfight": "teamfight", "avg_teamfight_": "teamfight%"}, inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "result_details_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)

#---------- Display download-position
@app.route('/download_position')
def download_position():
    with conn.cursor() as cur:
        cur.execute("""SELECT
                            p.name_player,
                            (
                                SELECT pos.position_name 
                                FROM tb_match
                                INNER JOIN tb_position AS pos ON tb_match.position_id = pos.position_id 
                                WHERE player_id = p.player_id
                                GROUP BY pos.position_name 
                                ORDER BY COUNT(*) DESC
                                LIMIT 1
                            ) AS most_common_position_name,
                            COUNT(*) AS total_matches,              
                            COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) AS count_win_2,
                            ROUND((COUNT(CASE WHEN b.win = 2 THEN 1 ELSE NULL END) / COUNT(*)) * 100, 1) 
                            AS win_2_percentage,
                            ROUND(AVG((b.kill + b.dead) / b.assist), 1) AS avg_ratio
                        FROM tb_player AS p
                        INNER JOIN tb_match AS b ON p.player_id = b.player_id
                        INNER JOIN tb_team AS t ON p.team_id = t.team_id
                        GROUP BY p.name_player
                    """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=[ "name_player", "most_common_position_name","total_matches",
                                     "count_win_2","win_2_percentage","avg_ratio"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["name_player", "most_common_position_name","total_matches",
                                     "count_win_2","win_2_percentage","avg_ratio"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "school_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "position_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"position_id_sequence": "ลำดับ", "name_player": "ชื่อผู้เล่น", 
                       "most_common_position_name": "ตำแหน่ง", "total_matches": "จำนวนการต่อสู้", 
                       "count_win_2": "อัตราชนะ", "win_2_percentage": "จำนวนครั้งที่ชนะ",
                       "avg_ratio": "KDA"}, inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "position_data.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)

#---------- Display download-win_rate_hero
@app.route('/download_win_rate_hero')
def download_win_rate_hero():
    with conn.cursor() as cur:
        cur.execute("""SELECT
                    h.hero_name,
                    COUNT(*) AS total_matches,
                    SUM(CASE WHEN m.win = 2 THEN 1 ELSE 0 END) AS count_win_2,
                    ROUND((SUM(CASE WHEN m.win = 2 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 1) 
                    AS win_percentage_2_vs_total,
                    ROUND(AVG((m.kill + m.dead) / m.assist), 1) AS kda_ratio
                FROM tb_match AS m
                INNER JOIN tb_hero AS h ON m.hero_id = h.hero_id
                GROUP BY h.hero_name
                ORDER BY total_matches DESC;
                """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=[ "hero_name", "total_matches","count_win_2","win_percentage_2_vs_total",
                                     "kda_ratio"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["hero_name", "total_matches","count_win_2","win_percentage_2_vs_total",
                        "kda_ratio"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "kdahero_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "kdahero_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"kdahero_id_sequence": "ลำดับ", "hero_name": "Hero", "total_matches": "จำนวนการต่อสู้",
                       "count_win_2": "จำนวนครั้งที่ชนะ","win_percentage_2_vs_total": "อัตราการชนะ", "kda_ratio": "KDA"}
                       , inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "win_rate_hero.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)

#---------- Display download-results_RoV
@app.route('/download_results_RoV')
def download_results_RoV():
    with conn.cursor() as cur:
        cur.execute("""SELECT 
                        tb.team_name AS team,
                        SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) AS count_2_in_team,
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END) AS count_3_in_team,
                        (SUM(CASE WHEN trA.results_2 = 2 THEN 1 ELSE 0 END) + 
                        SUM(CASE WHEN trA.results_3 = 3 THEN 1 ELSE 0 END)) AS total_count
                    FROM (
                        SELECT team_a AS team, resultsA AS results_2, resultsA AS results_3 FROM tb_result
                        UNION ALL
                        SELECT team_b AS team, resultsB AS results_2, resultsB AS results_3 FROM tb_result
                    ) AS trA
                    LEFT JOIN tb_team tb ON trA.team = tb.team_id
                    WHERE trA.results_2 = 2 OR trA.results_3 = 3
                    GROUP BY tb.team_name;
                    """)
        rows = cur.fetchall()
    
    # สร้าง DataFrame จากข้อมูลใน rows
    df = pd.DataFrame(rows, columns=["team", "count_2_in_team","count_3_in_team","total_count"])

    # เลือกและเรียงลำดับคอลัมน์ที่ต้องการ
    selected_columns = ["team", "count_2_in_team","count_3_in_team","total_count"]
    df = df[selected_columns]

    # เพิ่มคอลัมน์ "results_RoV_id" แสดงค่าเรียงตามลำดับ 1, 2, 3, ...
    df.insert(0, "results_RoV_id_sequence", range(1, len(df) + 1))

    # เปลี่ยนชื่อคอลัมน์ใน DataFrame
    df.rename(columns={"results_RoV_id_sequence": "ลำดับ", "team": "ทีม", "count_2_in_team": "แพ้",
                       "count_3_in_team": "ชนะ","total_count": "รวม"}
                       , inplace=True)

    # สร้างไฟล์ Excel (.xlsx) และบันทึก
    filename = "results_RoV.xlsx"
    file_path = os.path.join(app.root_path, 'static', filename)

    # บันทึกไฟล์ Excel โดยใช้ to_excel ของ pandas
    df.to_excel(file_path, index=False)

    # ส่งไฟล์ Excel ดาวน์โหลดให้กับผู้ใช้
    return send_file(file_path, as_attachment=True, download_name=filename)


#---------- Display upload 
@app.route('/upload')
def upload():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    return render_template('upload.html')

#---------- upload img 
@app.route('/upload_img',methods = ['GET','POST'])
def upload_img():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get the upload files
        image_statistic = request.files['file_statistic']
        image_details = request.files['file_details']
               
        # แปลงไฟล์ภาพ
        image_statistic_origin = origin(image_statistic)
        image_details_origin = origin(image_details)
        
        # แปลงรูปภาพเป็นรหัสภาพในรูปแบบ Base64
        encoded_statistic = base64.b64encode(cv2.imencode('.jpg', image_statistic_origin)[1]).decode('utf-8')
        encoded_details = base64.b64encode(cv2.imencode('.jpg', image_details_origin)[1]).decode('utf-8')

        # ปรับสีภาพให้เป็นสี RGB
        processed_statistics_o = cv2.cvtColor(image_statistic_origin,cv2.COLOR_BGR2RGB)
        processed_details_o = cv2.cvtColor(image_details_origin, cv2.COLOR_BGR2RGB)
        # processed img
        processed_statistics = dash_statistics(image_statistic_origin)
        processed_details = dash_details(image_details_origin)
        
        # combined img
        combined_img = cv2.vconcat([processed_statistics,processed_details])
        
        # resize img*_*
        scale_percent = 50
        # resize combined img
        width_img_join = int(combined_img.shape[1] * scale_percent / 100)
        height_img_join = int(combined_img.shape[0] * scale_percent / 100)
        dsize_img_join = (width_img_join, height_img_join)
        imgsize_img_join = cv2.resize(combined_img,dsize_img_join)
        # resize statistics img
        width_img_processed_statistics = int(processed_statistics.shape[1] * scale_percent / 100)
        height_img_processed_statistics = int(processed_statistics.shape[0] * scale_percent / 100)
        dsize_img_processed_statistics = (width_img_processed_statistics, height_img_processed_statistics)
        imgsize_img_processed_statistics = cv2.resize(processed_statistics,dsize_img_processed_statistics)
        # resize details img
        width_img_processed_details = int(processed_details.shape[1] * scale_percent / 100)
        height_img_processed_details = int(processed_details.shape[0] * scale_percent / 100)
        dsize_img_processed_details = (width_img_processed_details, height_img_processed_details)
        imgsize_img_processed_details = cv2.resize(processed_details,dsize_img_processed_details)
        
        # แปลงภาพ OpenCV เป็นรหัส base64 string
        retval = Image.fromarray(imgsize_img_join)
        statistics = Image.fromarray(imgsize_img_processed_statistics)
        details = Image.fromarray(imgsize_img_processed_details)
        statistics_origin = Image.fromarray(processed_statistics_o)
        details_origin =Image.fromarray(processed_details_o)

        # result data
        result_data = {}

        # Specify the position of the image to be OCR.
        specify_image = {
        "Player01":{
            "name":{
                "height": 144,
                "heightTo": 178,
                "width": 195,
                "widthTo": 331,
            },
            "kill":{
                "height": 144,
                "heightTo": 178,
                "width": 328,
                "widthTo": 362,
            },
            "dead":{
                "height": 144,
                "heightTo": 178,
                "width": 363,
                "widthTo": 403,
            },
            "assist":{
                "height": 144,
                "heightTo": 178,
                "width": 401,
                "widthTo": 439,
            },
            "money":{
                "height": 144,
                "heightTo": 178,
                "width": 439,
                "widthTo": 500,
            },
            "point":{
                "height": 144,
                "heightTo": 178,
                "width": 499,
                "widthTo": 542,
            },
            "damage":{
                "height": 152,
                "heightTo": 168,
                "width": 325,
                "widthTo": 403,
            },
            "damage_p":{
                "height": 169,
                "heightTo": 186,
                "width": 325,
                "widthTo": 403,
            },
            "take_damage":{
                "height": 152,
                "heightTo": 168,
                "width": 409,
                "widthTo": 494,
            },
            "take_damage_p":{
                "height": 169,
                "heightTo": 186,
                "width": 409,
                "widthTo": 494,
            },
            "team_fight":{
                "height": 152,
                "heightTo": 168,
                "width": 505,
                "widthTo": 594,
            },
            "team_fight_p":{
                "height": 169,
                "heightTo": 186,
                "width": 505,
                "widthTo": 594,
            },
        },
        "Player02":{
            "name":{
                "height": 214,
                "heightTo": 245,
                "width": 195,
                "widthTo": 331,
            },
            "kill":{
                "height": 214,
                "heightTo": 245,
                "width": 328,
                "widthTo": 362,
            },
            "dead":{
                "height": 214,
                "heightTo": 245,
                "width": 363,
                "widthTo": 403,
            },
            "assist":{
                "height": 214,
                "heightTo": 245,
                "width": 401,
                "widthTo": 439,
            },
            "money":{
                "height": 214,
                "heightTo": 245,
                "width": 439,
                "widthTo": 500,
            },
            "point":{
                "height": 214,
                "heightTo": 245,
                "width": 499,
                "widthTo": 542,
            },
            "damage":{
                "height": 220,
                "heightTo": 241,
                "width": 325,
                "widthTo": 403,
            },
            "damage_p":{
                "height": 238,
                "heightTo": 258,
                "width": 325,
                "widthTo": 403,
            },
            "take_damage":{
                "height": 220,
                "heightTo": 241,
                "width": 409,
                "widthTo": 494,
            },
            "take_damage_p":{
                "height": 238,
                "heightTo": 258,
                "width": 409,
                "widthTo": 494,
            },
            "team_fight":{
                "height": 220,
                "heightTo": 241,
                "width": 505,
                "widthTo": 594,
            },
            "team_fight_p":{
                "height": 238,
                "heightTo": 258,
                "width": 505,
                "widthTo": 594,
            },
        },
        "Player03":{
            "name":{
                "height": 285,
                "heightTo": 317,
                "width": 195,
                "widthTo": 331,
            },
            "kill":{
                "height": 285,
                "heightTo": 317,
                "width": 328,
                "widthTo": 362,
            },
            "dead":{
                "height": 285,
                "heightTo": 317,
                "width": 363,
                "widthTo": 403,
            },
            "assist":{
                "height": 285,
                "heightTo": 317,
                "width": 401,
                "widthTo": 439,
            },
            "money":{
                "height": 285,
                "heightTo": 317,
                "width": 439,
                "widthTo": 500,
            },
            "point":{
                "height": 285,
                "heightTo": 317,
                "width": 499,
                "widthTo": 542,
            },
            "damage":{
                "height": 289,
                "heightTo": 312,
                "width": 325,
                "widthTo": 403,
            },
            "damage_p":{
                "height": 311,
                "heightTo": 327,
                "width": 325,
                "widthTo": 403,
            },
            "take_damage":{
                "height": 289,
                "heightTo": 312,
                "width": 409,
                "widthTo": 494,
            },
            "take_damage_p":{
                "height": 311,
                "heightTo": 327,
                "width": 409,
                "widthTo": 494,
            },
            "team_fight":{
                "height": 289,
                "heightTo": 312,
                "width": 505,
                "widthTo": 594,
            },
            "team_fight_p":{
                "height": 311,
                "heightTo": 327,
                "width": 505,
                "widthTo": 594,
            },
        },
        "Player04":{
            "name":{
                "height": 356,
                "heightTo": 385,
                "width": 195,
                "widthTo": 331,
            },
            "kill":{
                "height": 356,
                "heightTo": 385,
                "width": 328,
                "widthTo": 362,
            },
            "dead":{
                "height": 356,
                "heightTo": 385,
                "width": 363,
                "widthTo": 403,
            },
            "assist":{
                "height": 356,
                "heightTo": 385,
                "width": 401,
                "widthTo": 439,
            },
            "money":{
                "height": 356,
                "heightTo": 385,
                "width": 439,
                "widthTo": 500,
            },
            "point":{
                "height": 356,
                "heightTo": 385,
                "width": 499,
                "widthTo": 542,
            },
            "damage":{
                "height": 360,
                "heightTo": 381,
                "width": 325,
                "widthTo": 403,
            },
            "damage_p":{
                "height": 381,
                "heightTo": 395,
                "width": 325,
                "widthTo": 403,
            },
            "take_damage":{
                "height": 360,
                "heightTo": 381,
                "width": 409,
                "widthTo": 494,
            },
            "take_damage_p":{
                "height": 381,
                "heightTo": 395,
                "width": 409,
                "widthTo": 494,
            },
            "team_fight":{
                "height": 360,
                "heightTo": 381,
                "width": 505,
                "widthTo": 594,
            },
            "team_fight_p":{
                "height": 381,
                "heightTo": 395,
                "width": 505,
                "widthTo": 594,
            },
        },
        "Player05":{
            "name":{
                "height": 426,
                "heightTo": 456,
                "width": 195,
                "widthTo": 331,
            },
            "kill":{
                "height": 426,
                "heightTo": 456,
                "width": 328,
                "widthTo": 362,
            },
            "dead":{
                "height": 426,
                "heightTo": 456,
                "width": 363,
                "widthTo": 403,
            },
            "assist":{
                "height": 426,
                "heightTo": 456,
                "width": 401,
                "widthTo": 439,
            },
            "money":{
                "height": 426,
                "heightTo": 456,
                "width": 439,
                "widthTo": 500,
            },
            "point":{
                "height": 426,
                "heightTo": 456,
                "width": 499,
                "widthTo": 542,
            },
            "damage":{
                "height": 431,
                "heightTo": 452,
                "width": 325,
                "widthTo": 403,
            },
            "damage_p":{
                "height": 448,
                "heightTo": 467,
                "width": 325,
                "widthTo": 403,
            },
            "take_damage":{
                "height": 431,
                "heightTo": 452,
                "width": 409,
                "widthTo": 494,
            },
            "take_damage_p":{
                "height": 448,
                "heightTo": 467,
                "width": 409,
                "widthTo": 494,
            },
            "team_fight":{
                "height": 431,
                "heightTo": 452,
                "width": 505,
                "widthTo": 594,
            },
            "team_fight_p":{
                "height": 448,
                "heightTo": 467,
                "width": 505,
                "widthTo": 594,
            },
        },
        "Player06":{
            "name":{
                "height": 144,
                "heightTo": 178,
                "width": 667,
                "widthTo": 798,
            },
            "kill":{
                "height": 144,
                "heightTo": 178,
                "width": 801,
                "widthTo": 836,
            },
            "dead":{
                "height": 144,
                "heightTo": 178,
                "width": 838,
                "widthTo": 872,
            },
            "assist":{
                "height": 144,
                "heightTo": 178,
                "width": 874,
                "widthTo": 907,
            },
            "money":{
                "height": 144,
                "heightTo": 178,
                "width": 905,
                "widthTo": 969,
            },
            "point":{
                "height": 144,
                "heightTo": 178,
                "width": 970,
                "widthTo": 1013,
            },
            "damage":{
                "height": 152,
                "heightTo": 168,
                "width": 794,
                "widthTo": 871,
            },
            "damage_p":{
                "height": 169,
                "heightTo": 186,
                "width": 794,
                "widthTo": 871,
            },
            "take_damage":{
                "height": 152,
                "heightTo": 168,
                "width": 881,
                "widthTo": 963,
            },
            "take_damage_p":{
                "height": 169,
                "heightTo": 186,
                "width": 881,
                "widthTo": 963,
            },
            "team_fight":{
                "height": 152,
                "heightTo": 168,
                "width": 975,
                "widthTo": 1059,
            },
            "team_fight_p":{
                "height": 169,
                "heightTo": 186,
                "width": 975,
                "widthTo": 1059,
            },
        },
        "Player07":{
            "name":{
                "height": 214,
                "heightTo": 245,
                "width": 667,
                "widthTo": 798,
            },
            "kill":{
                "height": 214,
                "heightTo": 245,
                "width": 801,
                "widthTo": 836,
            },
            "dead":{
                "height": 214,
                "heightTo": 245,
                "width": 838,
                "widthTo": 872,
            },
            "assist":{
                "height": 214,
                "heightTo": 245,
                "width": 874,
                "widthTo": 907,
            },
            "money":{
                "height": 214,
                "heightTo": 245,
                "width": 905,
                "widthTo": 969,
            },
            "point":{
                "height": 214,
                "heightTo": 245,
                "width": 970,
                "widthTo": 1013,
            },
            "damage":{
                "height": 220,
                "heightTo": 241,
                "width": 794,
                "widthTo": 871,
            },
            "damage_p":{
                "height": 238,
                "heightTo": 258,
                "width": 794,
                "widthTo": 871,
            },
            "take_damage":{
                "height": 220,
                "heightTo": 241,
                "width": 881,
                "widthTo": 963,
            },
            "take_damage_p":{
                "height": 238,
                "heightTo": 258,
                "width": 881,
                "widthTo": 963,
            },
            "team_fight":{
                "height": 220,
                "heightTo": 241,
                "width": 975,
                "widthTo": 1059,
            },
            "team_fight_p":{
                "height": 238,
                "heightTo": 258,
                "width": 975,
                "widthTo": 1059,
            },
        },
        "Player08":{
            "name":{
                "height": 285,
                "heightTo": 317,
                "width": 667,
                "widthTo": 798,
            },
            "kill":{
                "height": 285,
                "heightTo": 317,
                "width": 801,
                "widthTo": 836,
            },
            "dead":{
                "height": 285,
                "heightTo": 317,
                "width": 838,
                "widthTo": 872,
            },
            "assist":{
                "height": 285,
                "heightTo": 317,
                "width": 874,
                "widthTo": 907,
            },
            "money":{
                "height": 285,
                "heightTo": 317,
                "width": 905,
                "widthTo": 969,
            },
            "point":{
                "height": 285,
                "heightTo": 317,
                "width": 970,
                "widthTo": 1013,
            },
            "damage":{
                "height": 289,
                "heightTo": 312,
                "width": 794,
                "widthTo": 871,
            },
            "damage_p":{
                "height": 311,
                "heightTo": 327,
                "width": 794,
                "widthTo": 871,
            },
            "take_damage":{
                "height": 289,
                "heightTo": 312,
                "width": 881,
                "widthTo": 963,
            },
            "take_damage_p":{
                "height": 311,
                "heightTo": 327,
                "width": 881,
                "widthTo": 963,
            },
            "team_fight":{
                "height": 289,
                "heightTo": 312,
                "width": 975,
                "widthTo": 1059,
            },
            "team_fight_p":{
                "height": 311,
                "heightTo": 327,
                "width": 975,
                "widthTo": 1059,
            },
        },
        "Player09":{
            "name":{
                "height": 356,
                "heightTo": 385,
                "width": 667,
                "widthTo": 798,
            },
            "kill":{
                "height": 356,
                "heightTo": 385,
                "width": 801,
                "widthTo": 836,
            },
            "dead":{
                "height": 356,
                "heightTo": 385,
                "width": 838,
                "widthTo": 872,
            },
            "assist":{
                "height": 356,
                "heightTo": 385,
                "width": 874,
                "widthTo": 907,
            },
            "money":{
                "height": 356,
                "heightTo": 385,
                "width": 905,
                "widthTo": 969,
            },
            "point":{
                "height": 356,
                "heightTo": 385,
                "width": 970,
                "widthTo": 1013,
            },
            "damage":{
                "height": 360,
                "heightTo": 381,
                "width": 794,
                "widthTo": 871,
            },
            "damage_p":{
                "height": 381,
                "heightTo": 395,
                "width": 794,
                "widthTo": 871,
            },
            "take_damage":{
                "height": 360,
                "heightTo": 381,
                "width": 881,
                "widthTo": 963,
            },
            "take_damage_p":{
                "height": 381,
                "heightTo": 395,
                "width": 881,
                "widthTo": 963,
            },
            "team_fight":{
                "height": 360,
                "heightTo": 381,
                "width": 975,
                "widthTo": 1059,
            },
            "team_fight_p":{
                "height": 381,
                "heightTo": 395,
                "width": 975,
                "widthTo": 1059,
            },
        },
        "Player10":{
            "name":{
                "height": 426,
                "heightTo": 456,
                "width": 667,
                "widthTo": 798,
            },
            "kill":{
                "height": 426,
                "heightTo": 456,
                "width": 801,
                "widthTo": 836,
            },
            "dead":{
                "height": 426,
                "heightTo": 456,
                "width": 838,
                "widthTo": 872,
            },
            "assist":{
                "height": 426,
                "heightTo": 456,
                "width": 874,
                "widthTo": 907,
            },
            "money":{
                "height": 426,
                "heightTo": 456,
                "width": 905,
                "widthTo": 969,
            },
            "point":{
                "height": 426,
                "heightTo": 456,
                "width": 970,
                "widthTo": 1013,
            },
            "damage":{
                "height": 431,
                "heightTo": 452,
                "width": 794,
                "widthTo": 871,
            },
            "damage_p":{
                "height": 448,
                "heightTo": 467,
                "width": 794,
                "widthTo": 871,
            },
            "take_damage":{
                "height": 431,
                "heightTo": 452,
                "width": 881,
                "widthTo": 963,
            },
            "take_damage_p":{
                "height": 448,
                "heightTo": 467,
                "width": 881,
                "widthTo": 963,
            },
            "team_fight":{
                "height": 431,
                "heightTo": 452,
                "width": 975,
                "widthTo": 1059,
            },
            "team_fight_p":{
                "height": 448,
                "heightTo": 467,
                "width": 975,
                "widthTo": 1059,
            },
        },
    }
        for data_index in range(2):
            teamA = {
                "name":[],
                "kill":[],
                "dead":[],
                "assist":[],
                "money":[],
                "point":[],
                "damage":[],
                "damage_p":[],
                "take_damage":[],
                "take_damage_p":[],
                "team_fight":[],
                "team_fight_p":[],
            }
            teamB = {
                "name":[],
                "kill":[],
                "dead":[],
                "assist":[],
                "money":[],
                "point":[],
                "damage":[],
                "damage_p":[],
                "take_damage":[],
                "take_damage_p":[],
                "team_fight":[],
                "team_fight_p":[],
            }
            for index_player ,key in enumerate(specify_image):
                if index_player <= 4:
                    # case team blue
                    for index_point ,name in enumerate(specify_image[key]):
                        if index_point <= 5:
                            # img = cv2.imread(imgsize_img_processed_statistics)
                            img_specify_image = imgsize_img_processed_statistics[specify_image[key][name]['height']:specify_image[key][name]['heightTo'], specify_image[key][name]['width']:specify_image[key][name]['widthTo']]
                            result_ocr = tess.image_to_string( img_specify_image, lang='eng+tha+jpn', config='--psm 6 -c preserve_interword_spaces=1' )
                            cleaning_text(result_ocr,index_point, index_player, teamA, teamB)
                        else:
                            # img = cv2.imread(imgsize_img_processed_details)
                            img_specify_image = imgsize_img_processed_details[specify_image[key][name]['height']:specify_image[key][name]['heightTo'], specify_image[key][name]['width']:specify_image[key][name]['widthTo']]
                            result_ocr = tess.image_to_string( img_specify_image, lang='eng+tha+jpn', config='--psm 6 -c preserve_interword_spaces=1' )
                            cleaning_text(result_ocr,index_point, index_player, teamA, teamB)
                else:
                    # case team blue
                    for index_point ,name in enumerate(specify_image[key]):
                        if index_point <= 5:
                            # img = cv2.imread(imgsize_img_processed_statistics)
                            img_specify_image = imgsize_img_processed_statistics[specify_image[key][name]['height']:specify_image[key][name]['heightTo'], specify_image[key][name]['width']:specify_image[key][name]['widthTo']]
                            result_ocr = tess.image_to_string( img_specify_image, lang='eng+tha+jpn', config='--psm 6 -c preserve_interword_spaces=1' )
                            cleaning_text(result_ocr,index_point, index_player, teamA, teamB)
                        else:
                            # img = cv2.imread(imgsize_img_processed_details)
                            img_specify_image = imgsize_img_processed_details[specify_image[key][name]['height']:specify_image[key][name]['heightTo'], specify_image[key][name]['width']:specify_image[key][name]['widthTo']]
                            result_ocr = tess.image_to_string( img_specify_image, lang='eng+tha+jpn', config='--psm 6 -c preserve_interword_spaces=1' )
                            cleaning_text(result_ocr,index_point, index_player, teamA, teamB)

                #ชื่อตัวแปลแสดงข้อมูลเกี่ยวกับฟังก์ชัน
                result_data = [{"teamA": teamA},{"teamB": teamB}]
                dropdown_data_hero = get_dropdown_data_hero()
                dropdown_data_player = get_dropdown_data_player()
                dropdown_data_team = get_dropdown_data_team()
                dropdown_data_position = get_dropdown_data_position()

        # แสดงข้อมูลที่ทำ ocr
        print(result_data)
        return render_template('result.html', result_data = result_data ,statistics_origin=encoded_statistic ,details_origin=encoded_details,dropdown_data_hero=dropdown_data_hero,dropdown_data_player=dropdown_data_player,dropdown_data_team=dropdown_data_team,dropdown_data_position=dropdown_data_position)  
    return render_template('upload.html')  

#---------- Display Check result ocr
@app.route('/check_information', methods=['GET','POST'])
def check_information():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # เชื่อมต่อกับฐานข้อมูล
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        #ข้อมูลที่จะบันทึกลง tb_result
        team_a = request.form['team_a']
        team_b = request.form['team_b']
        round_number = request.form['round']
        date_match = request.form['date_match']
        resultsA = request.form['resultsA']
        resultsB = request.form['resultsB']

        #ข้อมูลที่จะบันทึกลง tb_match
        # case team A
        player_a = request.form.getlist('player_a[]')
        kill_a = request.form.getlist('kill[]')
        dead_a = request.form.getlist('dead[]')
        assist_a = request.form.getlist('assist[]')
        money_a = request.form.getlist('money[]')
        point_a = request.form.getlist('point[]')
        damage_a = request.form.getlist('damage[]')
        damage_p_a = request.form.getlist('damage%[]')
        take_damage_a = request.form.getlist('take_damage[]')
        take_damage_p_a = request.form.getlist('take_damage%[]')
        teamfight_a = request.form.getlist('teamfight[]')
        teamfight_p_a = request.form.getlist('teamfight%[]')
        permission_a = request.form.getlist('permission[]')
        hero_a = request.form.getlist('hero[]')
        mvp_a = request.form.getlist('mvp_a[]')
        win_a = request.form.getlist('win_a[]')

        # case team B
        player_b = request.form.getlist('player_b[]')
        kill_b = request.form.getlist('kill[]')[5:]
        dead_b = request.form.getlist('dead[]')[5:]
        assist_b = request.form.getlist('assist[]')[5:]
        money_b = request.form.getlist('money[]')[5:]
        point_b = request.form.getlist('point[]')[5:]
        damage_b = request.form.getlist('damage[]')[5:]
        damage_p_b = request.form.getlist('damage%[]')[5:]
        take_damage_b = request.form.getlist('take_damage[]')[5:]
        take_damage_p_b = request.form.getlist('take_damage%[]')[5:]
        teamfight_b = request.form.getlist('teamfight[]')[5:]
        teamfight_p_b = request.form.getlist('teamfight%[]')[5:]
        permission_b = request.form.getlist('permission[]')[5:]
        hero_b = request.form.getlist('hero[]')[5:]
        mvp_b = request.form.getlist('mvp_b[]')
        win_b = request.form.getlist('win_b[]')

        # ตรวจสอบชื่อผู้เล่นในทีม A and B
        check_name_player_a = all(check_name_player(player) for player in player_a)
        check_name_player_b = all(check_name_player(player) for player in player_b)

        # ถ้าตรวจสอบชื่อผู้เล่นในทีม A and B ผ่าน
        if check_name_player_a and check_name_player_b:
            # ชื่อผู้เล่นตรงกับฐานข้อมูล
            check_player_teama = all(check_player_team(player, team_a) for player in player_a)
            check_player_teamb = all(check_player_team(player, team_b) for player in player_b)

            if check_player_teama and check_player_teamb:
                # ค้นหา ID ของผู้เล่นทีม A และทีม B และให้ player บันทึกเป็น ID
                player_a_ids = [get_player_id_by_name(cursor, player) for player in player_a]
                player_b_ids = [get_player_id_by_name(cursor, player) for player in player_b]

                # ชื่อผู้เล่นตรงกับฐานข้อมูลและตรงกับชื่อทีม
                team_a_players = []
                for i in range(len(player_a)):
                    # ค้นหา ID ของตำแหน่ง (permission)
                    permission_id = get_position_id_by_name(cursor, permission_a[i])
                    # ค้นหา ID ของฮีโร่ (hero)
                    hero_id = get_hero_id_by_name(cursor, hero_a[i])
                    # ค้นหา ID ของชนะ (win)
                    win_id = get_score_id_by_name(cursor, win_a[i])
                    player = {
                        'name': player_a_ids[i],
                        'kill': kill_a[i],
                        'dead': dead_a[i],
                        'assist': assist_a[i],
                        'money':money_a[i],
                        'point':point_a[i],
                        'damage':damage_a[i],
                        'damage_p':damage_p_a [i],
                        'take_damage':take_damage_a [i],
                        'take_damage_p':take_damage_p_a[i], 
                        'teamfight':teamfight_a [i],
                        'teamfight_p':teamfight_p_a [i],
                        'permission':permission_id,
                        'hero':hero_id,
                        'mvp':mvp_a [i],
                        'win':win_id,
                    }
                    team_a_players.append(player)

                # สร้างรายการของผู้เล่นทีม B
                team_b_players = []
                for i in range(len(player_b)):
                    # ค้นหา ID ของตำแหน่ง (permission)
                    permission_id = get_position_id_by_name(cursor, permission_b[i])
                    # ค้นหา ID ของฮีโร่ (hero)
                    hero_id = get_hero_id_by_name(cursor, hero_b[i])
                    # ค้นหา ID ของชนะ (win)
                    win_id = get_score_id_by_name(cursor, win_b[i])
                    player = {
                        'name': player_b_ids[i],
                        'kill': kill_b[i],
                        'dead': dead_b[i],
                        'assist': assist_b[i],
                        'money':money_b[i],
                        'point':point_b[i],
                        'damage':damage_b[i],
                        'damage_p':damage_p_b [i],
                        'take_damage':take_damage_b [i],
                        'take_damage_p':take_damage_p_b[i], 
                        'teamfight':teamfight_b [i],
                        'teamfight_p':teamfight_p_b [i],
                        'permission':permission_id,
                        'hero':hero_id,
                        'mvp':mvp_b [i],
                        'win':win_id,
                    }
                    team_b_players.append(player)
                return render_template('show_information.html', team_a_players=team_a_players, team_b_players=team_b_players,team_a=team_a,team_b=team_b,round_number=round_number,date_match=date_match,resultsA=resultsA,resultsB=resultsB)
            else:
                # ชื่อผู้เล่นหรือชื่อทีมไม่ตรงกับฐานข้อมูล
                return '<h1 style="color: red; font-weight: bold;">ชื่อผู้เล่นหรือชื่อทีมไม่ตรงกับฐานข้อมูล</h1>'
        else:
            # ชื่อผู้เล่นไม่ตรงกับฐานข้อมูล
            return '<h1 style="color: red; font-weight: bold;">ชื่อผู้เล่นไม่ตรงกับฐานข้อมูล</h1>'        
    return render_template('result.html')

#---------- Display Add result ocr
@app.route('/save_information', methods=['GET','POST'])
def save_information():
    # ตรวจสอบสถานะการเข้าสู่ระบบ ถ้ายังไม่ได้เข้าสู่ระบบให้ redirect ไปยังหน้า login
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # เชื่อมต่อกับฐานข้อมูล
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        #ข้อมูลที่จะบันทึกลง tb_result
        team_a = request.form['team_a']
        team_b = request.form['team_b']
        round_number = request.form['round_number']
        date_match = request.form['date_match']
        resultsA = request.form['resultsA']
        resultsB = request.form['resultsB']

        #ข้อมูลที่จะบันทึกลง tb_match
        #case A
        player_a = request.form.getlist('name_a[]')
        kill_a = request.form.getlist('kill_a[]')
        dead_a = request.form.getlist('dead_a[]')
        assist_a = request.form.getlist('assist_a[]')
        money_a = request.form.getlist('money_a[]')
        point_a = request.form.getlist('point_a[]')
        damage_a = request.form.getlist('damage_a[]')
        damage_p_a = request.form.getlist('damage_p_a[]')
        take_damage_a = request.form.getlist('take_damage_a[]')
        take_damage_p_a = request.form.getlist('take_damage_p_a[]')
        teamfight_a = request.form.getlist('teamfight_a[]')
        teamfight_p_a = request.form.getlist('teamfight_p_a[]')
        permission_a = request.form.getlist('permission_a[]')
        hero_a = request.form.getlist('hero_a[]')
        mvp_a = request.form.getlist('mvp_a[]')
        win_a = request.form.getlist('win_a[]')

        #case B
        player_b = request.form.getlist('name_b[]')
        kill_b = request.form.getlist('kill_b[]')
        dead_b = request.form.getlist('dead_b[]')
        assist_b = request.form.getlist('assist_b[]')
        money_b = request.form.getlist('money_b[]')
        point_b = request.form.getlist('point_b[]')
        damage_b = request.form.getlist('damage_b[]')
        damage_p_b = request.form.getlist('damage_p_b[]')
        take_damage_b = request.form.getlist('take_damage_b[]')
        take_damage_p_b = request.form.getlist('take_damage_p_b[]')
        teamfight_b = request.form.getlist('teamfight_b[]')
        teamfight_p_b = request.form.getlist('teamfight_p_b[]')
        permission_b = request.form.getlist('permission_b[]')
        hero_b = request.form.getlist('hero_b[]')
        mvp_b = request.form.getlist('mvp_b[]')
        win_b = request.form.getlist('win_b[]')

        # ค้นหา id ของ ตัวแปร จากตาราง tb ของฐานข้อมูล
        team_a_id = get_team_id_by_name(cursor, team_a)
        team_b_id = get_team_id_by_name(cursor, team_b)
        result_a_id = get_score_id_by_name(cursor, resultsA)
        result_b_id = get_score_id_by_name(cursor, resultsB)   

        # สร้างคำสั่ง SQL สำหรับแทรกข้อมูลในตาราง tb_result
        sql = "INSERT INTO tb_result (team_a, team_b, round_match, date_match, resultsA, resultsB) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (team_a_id, team_b_id, round_number, date_match, result_a_id, result_b_id)
        print(sql, values)
        try:
            cursor.execute(sql, values)
        except mysql.connector.Error as err:
            print("MySQL Error: ", err)
        
        # สร้างคำสั่ง SQL INSERT สำหรับข้อมูลทีม A
        for i in range(len(player_a)):
            # Save in database
            insert_query = """INSERT INTO tb_match (`player_id`,`kill`, `dead`, `assist`, `money`, `point`, `mvp`, `damage`, `damage_`, `take_damage`, `take_damage_`, `teamfight`, `teamfight_`, `date_match`, `hero_id`, `position_id`, `win`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            values = (player_a[i], kill_a[i], dead_a[i], assist_a[i], money_a[i], point_a[i], mvp_a[i], damage_a[i], damage_p_a[i], take_damage_a[i], take_damage_p_a[i], teamfight_a[i], teamfight_p_a[i], date_match, hero_a[i], permission_a[i], win_a[i])
            print(insert_query, values)
            try:
                cursor.execute(insert_query, values)
            except mysql.connector.Error as err:
                print("MySQL Error: ", err)

        # สร้างคำสั่ง SQL INSERT สำหรับข้อมูลทีม B
        for i in range(len(player_b)):
            # Save in database
            insert_query = """INSERT INTO tb_match (`player_id`,`kill`, `dead`, `assist`, `money`, `point`, `mvp`, `damage`, `damage_`, `take_damage`, `take_damage_`, `teamfight`, `teamfight_`, `date_match`, `hero_id`, `position_id`, `win`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            values = (player_b[i],  kill_b[i], dead_b[i], assist_b[i], money_b[i], point_b[i], mvp_b[i], damage_b[i], damage_p_b[i], take_damage_b[i], take_damage_p_b[i], teamfight_b[i], teamfight_p_b[i], date_match, hero_b[i], permission_b[i], win_b[i])
            print(insert_query, values)
            try:
                cursor.execute(insert_query, values)
            except mysql.connector.Error as err:
                print("MySQL Error: ", err)
        # ยืนยันการเปลี่ยนแปลงและปิดการเชื่อมต่อ
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('upload.html')
    return render_template('show_information.html')

#---------- debug ----------
if __name__ == "__main__":
    app.run(debug=True)