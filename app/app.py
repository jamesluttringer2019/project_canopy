from flask import Flask, request, jsonify
import psycopg2 as pg
from psycopg2.sql import SQL
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    conn = pg.connect(dbname=config('DBNAME'),
                        user=config('USER'),
                        password=config('PASSWORD'),
                        host=config('HOST'))
    
    @app.route('/')
    def hello():
        return 'it works'

    @app.route('/history', methods=['GET'])
    def history():
        curs = conn.cursor()
        years = request.args.get('years').split(',')
        results = {}
        
        for y in years:
            col = 'y' + y
            q = f'''
            SELECT {col}, COUNT({col})
            FROM history
            GROUP BY {col}
            '''
            curs.execute(q)
            out = {} 
            for cat,count in curs.fetchall():
                if cat:
                    out[cat]=count

            results[y] = out
        curs.close()
        return jsonify(results)

    @app.route('/taxonhistory', methods=['GET'])
    def taxonhistory():
        curs = conn.cursor()
        year = request.args.get('year')
        country = request.args.get('country')
        

    return app