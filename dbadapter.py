import psycopg2
from examterm import ExamTerm
from datetime import datetime
import os

get_query = """ SELECT * FROM public."ExamTerms" """

insert_query = """ INSERT INTO public."ExamTerms"(
	"DATE", "TIME", "IS_AVAILABLE", "TIMESTAMP")
	VALUES (%s, %s, %s, %s); """

update_query = """ UPDATE public."ExamTerms"
	SET "IS_AVAILABLE" = %s, "TIMESTAMP" = %s
	WHERE "DATE" = %s AND "TIME" = %s; """

def get_all():
    all_terms = []
    with psycopg2.connect(user=os.getenv('SQL_USER'),
                                    password=os.getenv('SQL_PASSWORD'),
                                    host=os.getenv('SQL_HOST'),
                                    port=os.getenv('SQL_PORT'),
                                    database=os.getenv('SQL_DB_NAME')) as connection:
        
        with connection.cursor() as cursor:
            cursor.execute(get_query)
            for term in cursor.fetchall():
                all_terms.append(ExamTerm(term[1], term[2], term[3], term[4]))
            return all_terms

def insert(term):
    with psycopg2.connect(user=os.getenv('SQL_USER'),
                                    password=os.getenv('SQL_PASSWORD'),
                                    host=os.getenv('SQL_HOST'),
                                    port=os.getenv('SQL_PORT'),
                                    database=os.getenv('SQL_DB_NAME')) as connection:
        
        with connection.cursor() as cursor:
            insert_data = (term.date, term.time, term.is_available, term.timestamp)
            cursor.execute(insert_query, insert_data)
            

def update(term, value):
    with psycopg2.connect(user=os.getenv('SQL_USER'),
                                    password=os.getenv('SQL_PASSWORD'),
                                    host=os.getenv('SQL_HOST'),
                                    port=os.getenv('SQL_PORT'),
                                    database=os.getenv('SQL_DB_NAME')) as connection:
        
        with connection.cursor() as cursor:
            update_data = (value, timestamp(), term.date, term.time)
            cursor.execute(update_query, update_data)

#TODO: EU verzija i Americka verzija
def timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")