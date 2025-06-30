from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pangitiara_db'

mysql = MySQL(app)

@app.route('/')
def root():
    return 'Hai Semuanyaaa!'

@app.route('/biodata')
def person():
    return jsonify({'nama': 'pangi tiara', 
                    'email': 'tiarapng@gmail.com'})

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    cursor = mysql.connection.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM MAHASISWA")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)
    else:
        data = request.get_json()
        sql = "INSERT INTO MAHASISWA (nama, fakultas, jurusan) VALUES (%s, %s, %s)"
        val = (data['nama'], data['fakultas'], data['jurusan'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})

@app.route('/detailmahasiswa')
def detailmahasiswa():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM MAHASISWA WHERE mahasiswa_id = %s"
        cursor.execute(sql, (request.args['id'],))
        column_names = [i[0] for i in cursor.description]
        row = cursor.fetchone()
        cursor.close()
        return jsonify(dict(zip(column_names, row)) if row else {})

@app.route('/deletemahasiswa', methods=['GET', 'DELETE'])
def deletemahasiswa():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM MAHASISWA WHERE mahasiswa_id = %s"
        cursor.execute(sql, (request.args['id'],))
        mysql.connection.commit()
        cursor.close()

        # Tangani sesuai metode
        if request.method == 'DELETE' or request.headers.get('Accept') == 'application/json':
            return jsonify({'message': 'Data delete successfully'}), 200
        else:
            return redirect(url_for('view_mahasiswa'))
    else:
        return jsonify({'error': 'Parameter id tidak ditemukan'}), 400

@app.route('/editmahasiswa', methods=['PUT'])
def editmahasiswa():
    if 'id' in request.args:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE MAHASISWA SET nama=%s, fakultas=%s, jurusan=%s WHERE mahasiswa_id=%s"
        val = (data['nama'], data['fakultas'], data['jurusan'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully'})

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama']
    fakultas = request.form['fakultas']
    jurusan = request.form['jurusan']
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO MAHASISWA (nama, fakultas, jurusan) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nama, fakultas, jurusan))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_mahasiswa'))

@app.route('/viewmahasiswa')
def view_mahasiswa():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM MAHASISWA")
    column_names = [i[0] for i in cursor.description]
    rows = cursor.fetchall()
    data = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    return render_template('mahasiswa.html', mahasiswa=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=70, debug=True)
