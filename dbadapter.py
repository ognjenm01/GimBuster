import psycopg2
from examterm import ExamTerm
from subscription import Subscription
from util import timestamp
import os

get_term_query = """ SELECT * FROM public."ExamTerms" """

insert_term_query = """ INSERT INTO public."ExamTerms"(
	"DATE", "TIME", "IS_AVAILABLE", "TIMESTAMP")
	VALUES (%s, %s, %s, %s); """

update_term_query = """ UPDATE public."ExamTerms"
	SET "IS_AVAILABLE" = %s, "TIMESTAMP" = %s
	WHERE "DATE" = %s AND "TIME" = %s; """

get_subscriptions_query = """ SELECT * FROM public."Subscriptions" """

get_subscription_query = """ SELECT * FROM public."Subscriptions" WHERE "CHAT_ID" = %s """

insert_subscription_query = """ INSERT INTO public."Subscriptions"(
	"FULL_NAME", "CHAT_ID", "ENABLED", "TIMESTAMP")
	VALUES (%s, %s, %s, %s);
"""

update_subscription_query = """ UPDATE public."Subscriptions"
	SET "ENABLED"=%s, "TIMESTAMP"=%s
	WHERE "CHAT_ID"=%s;
"""

def create_connection():
    return psycopg2.connect(user=os.getenv('SQL_USER'),
                                    password=os.getenv('SQL_PASSWORD'),
                                    host=os.getenv('SQL_HOST'),
                                    port=os.getenv('SQL_PORT'),
                                    database=os.getenv('SQL_DB_NAME'))

def get_all_terms():
    all_terms = []
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(get_term_query)
            for term in cursor.fetchall():
                all_terms.append(ExamTerm(term[1], term[2], term[3], term[4]))
            return all_terms

def insert_term(term):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            insert_data = (term.date, term.time, term.is_available, term.timestamp)
            cursor.execute(insert_term_query, insert_data)            

def update_term(term, value):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            update_data = (value, timestamp(), term.date, term.time)
            cursor.execute(update_term_query, update_data)

def get_all_subscriptions():
    all_subs = []
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(get_subscriptions_query)
            for sub in cursor.fetchall():
                all_subs.append(Subscription(sub[1], sub[2], sub[3], sub[4]))
    return all_subs

def get_subscription(chat_id):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(get_subscription_query, chat_id)
            sub = cursor.fetchone()
            return Subscription([sub[1], sub[2], sub[3], sub[4]])

def insert_subscription(subscription):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            insert_data = (subscription.full_name, subscription.chat_id, subscription.enabled, subscription.timestamp)
            cursor.execute(insert_subscription_query, insert_data)

def update_subscription(subscription):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            update_data = (subscription.enabled, subscription.timestamp, str(subscription.chat_id))
            cursor.execute(update_subscription_query, update_data)