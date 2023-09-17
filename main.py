import requests
from bs4 import BeautifulSoup
import pymysql

# Initialize the MySQL connection
connection = pymysql.connect(host='localhost', user='your_username', password='your_password', db='your_db_name')
cursor = connection.cursor()

# Fetch the webpage
interPark_res = requests.get("http://ticket.interpark.com/webzine/paper/TPNoticeList_iFrame.asp?bbsno=0&pageno=0&stext=&KindOfGoods=&Genre=&sort=")

if interPark_res.status_code == 200:
    html_content = interPark_res.content.decode('cp949')
    soup = BeautifulSoup(html_content, 'html.parser')

    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    for row in rows:
        ticket_type = row.find('td', {'class': 'type'}).text.strip()
        ticket_title = row.find('td', {'class': 'subject'}).text.strip()
        ticket_url = "http://ticket.interpark.com/webzine/paper/" + row.find('a')['href'].strip()
        ticket_date = row.find('td', {'class': 'date'}).text.strip()
        ticket_views = row.find('td', {'class': 'count'}).text.strip()

        # Inserting data into MySQL
        sql = "INSERT INTO tickets (ticket_type, ticket_title, ticket_url, ticket_date, ticket_views) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (ticket_type, ticket_title, ticket_url, ticket_date, ticket_views))

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()
