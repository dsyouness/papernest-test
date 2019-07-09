from connect import connect_db
from connect import connect_gmail
import pandas as pd


def get_body():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.execute("""
    select
        calls.date,
        count(calls.called_number) as number_calls
    from
        calls
    where
        calls.date>(select max(calls.date)-7 from calls)
    group by
        calls.date
    order by
        1
    """)
    # Getting Field Header names
    column_names = [i[0] for i in cur.description]
    # Getting Content query
    data = [list(i) for i in cur.fetchall()]
    cur.close()
    df = pd.DataFrame(data, columns=column_names)
    return df.to_html()


def generate_csv(file='src/file.csv'):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    select
        cls.id,
        cls."FirstName",
        cls."LastName",
        cls."PhoneNumber",
        cal.incoming_number,
      max(cal.date) as first_call,
        sum(cal.duration_in_sec)/count(cal.duration_in_sec) as average_calls
    from
        clients_crm cls inner join calls cal
            on cls."PhoneNumber" like '%' || cal.incoming_number
    group by
        cls.id,
        cls."FirstName",
        cls."LastName",
        cls."PhoneNumber",
      cal.incoming_number
    order by
      1
    """)
    # Getting Field Header names
    column_names = [i[0] for i in cur.description]
    # Getting Content query
    data = [list(i) for i in cur.fetchall()]
    cur.close()
    df = pd.DataFrame(data, columns=column_names)
    df.to_csv(file, sep=';', index=False, encoding='iso-8859-1')


def send_gmail(subject='Technical test DE BY DRISSI SLIMANI YOUNESS', file='src/file.csv'):
    body = 'This is obviously the body'
    html = get_body()
    connect_gmail(subject, [body, html], file)
