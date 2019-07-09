from functions import generate_csv
from functions import send_gmail

if __name__ == '__main__':
    generate_csv(file='src/file.csv')
    send_gmail(subject='Technical test DE BY DRISSI SLIMANI YOUNESS', file='src/file.csv')
