import psycopg2
import random
import string
import datetime


class AddData:
    def __init__(self, host, user, password, database):
        self.mydb = psycopg2.connect(host=host, user=user, password=password, database=database)

    @staticmethod
    def g_r_s(logic, size=10):                         # Generate Random String
        ret_str = ''
        for i in range(size):
            character = random.choice(logic)
            ret_str += character
        return ret_str

    @staticmethod
    def query_data(table):
        query = ""
        data = ""
        deside = ['true', 'false']
        provider = ['facebook', 'google', 'manual']
        if table == 'user':
            query = f"insert into public.{table}(first_name,last_name,username,password,email," \
                f"gender,invite_code,is_email_verified,is_mobile_verified,is_accepted_terms_and_condi," \
                f"is_superuser,is_staff,is_active,provider,city_id,date_joined,created_at) " \
                f"values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
            data = (AddData.g_r_s(string.ascii_lowercase, size=6), AddData.g_r_s(string.ascii_lowercase, size=6),
                    AddData.g_r_s(string.ascii_lowercase, size=8), AddData.g_r_s(string.ascii_lowercase, size=8),
                    AddData.g_r_s(string.ascii_lowercase, size=10) + '@' + AddData.g_r_s(string.ascii_lowercase, size=5),
                    random.randint(1, 2), AddData.g_r_s(string.ascii_uppercase, size=6), random.choice(deside),
                    random.choice(deside), random.choice(deside), random.choice(deside), 'false', 'false',
                    random.choice(provider), 4, datetime.datetime.now(), datetime.datetime.now())
        if table == 'invite':
            query = f"insert into public.{table}(invites_mobile,inviter_id,created_at) values(%s, %s, %s) " \
                f"RETURNING id;"
            data = (AddData.g_r_s(string.digits, size=10), 8, datetime.datetime.now())

        if table == 'state':
            query = f"insert into public.{table}(state,banner,is_active,created_at) values(%s, %s, %s, %s) " \
                f"RETURNING id;"
            data = (AddData.g_r_s(string.ascii_lowercase, size=8), AddData.g_r_s(string.ascii_lowercase, size=10),
                    random.choice(deside), datetime.datetime.now())

        if table == 'city':
            query = f"insert into public.{table}(city,banner,is_active,state_id,created_at) values(%s, %s, %s, %s) " \
                f"RETURNING id;"
            data = (AddData.g_r_s(string.ascii_lowercase, size=8), AddData.g_r_s(string.ascii_lowercase, size=10),
                    random.choice(deside), 10, datetime.datetime.now())

        return query, data

    def run_query(self, table):
        mycursor = self.mydb.cursor()
        obj = ""
        try:
            query, data = self.query_data(table)
            mycursor.execute(query, data)
            result = mycursor.fetchone()[0]
            self.mydb.commit()
            print(mycursor.rowcount, "Record stores successfully")
            fetch_query = f"select * from public.{table} where id={result} order by id DESC"
            mycursor.execute(fetch_query)
            obj = mycursor.fetchone()
        except (Exception, psycopg2.Error) as e:
            print(e)
        finally:
            if self.mydb:
                mycursor.close()
                self.mydb.close()

        return obj


if __name__ == '__main__':
    data = AddData(host="your-host", user="your-usename", password="your-password", database="your-database-name")
    table = input("Enter table name ['user','invite','state','city'] : ")
    print(data.run_query(table))
