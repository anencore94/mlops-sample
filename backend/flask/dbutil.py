import pymysql


# db 연결
def getConnection():
  return pymysql.connect(host='192.168.99.100', port=31111,
                         user='testuser', password='testpassword',
                         db='testdb', charset='utf8')


# select model info
def select_model_info():
  # Connection 연결
  conn = getConnection()

  # select 한 데이터를 Dictionary 형태로 가져오기 위함
  dictCursor = conn.cursor(pymysql.cursors.DictCursor)

  # SQL select query 날리기
  sql = "SELECT * FROM MODEL_INFO"
  dictCursor.execute(sql)

  # query 의 output 가져오기
  rows = dictCursor.fetchall()

  # commit
  conn.commit()

  # Connection 닫기
  conn.close()

  return rows
