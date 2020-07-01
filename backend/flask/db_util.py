"""
Flask server 에서 mysql DB server 로 통신하는 부분의 구현체
"""
import pymysql

import const


# db 연결
def get_connection():
  # TODO DB_IP, DB_PORT 는 k8s client 로 db pod 이 떠있는 node 와 service port 를
  #  조회해서 받아오도록 수정 필요
  #  singleton session 보장 필요?
  return pymysql.connect(host=const.DB_IP, port=const.DB_PORT,
                         user=const.DB_USER, password=const.DB_PASSWORD,
                         db=const.DB_DATABASE, charset='utf8')


def select_model_info():
  """
MODEL_INFO table 의 모든 row 를 조회합니다.

:return: 조회결과를 담은 dictionary
:rtype: dict
"""
  # DB session 생성
  conn = get_connection()

  # select 한 데이터를 Dictionary 형태로 가져오기 위한 dict_cursor
  dict_cursor = conn.cursor(pymysql.cursors.DictCursor)

  # SQL select query 날리기
  select_model_info_sql = "SELECT * FROM MODEL_INFO"
  dict_cursor.execute(select_model_info_sql)

  # query 의 output 가져오기
  rows = dict_cursor.fetchall()

  # DB commit
  conn.commit()

  # DB session 종료
  conn.close()

  return rows
