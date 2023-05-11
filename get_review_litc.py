import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import calendar


URL = "https://www.trustpilot.com/review/litextension.com?languages=all&page={}&sort=recency"

con = mysql.connector.connect(
    user="canhdv",
    password="1305",
    host="127.0.0.1",
    database="mydb",
    auth_plugin="mysql_native_password",
)

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS Review")
sql = """CREATE TABLE Review(
    Name TEXT,
    Country TEXT,
    Rate INT,
    Title TEXT,
    Content TEXT,
    Dates DATE
    )"""
cur.execute(sql)


for i in range(1, 40):
    response = requests.get(URL.format(i))

    if response.status_code != 200:
        print("Can't get review!!!")
        break

    elif response.status_code == 200:
        tree = BeautifulSoup(markup=response.text, features="html.parser")
        reviews = tree.findAll(
            "div",
            attrs={
                "class": "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"
            },
        )

    for review in reviews:
        countries = review.find(
            "div",
            attrs={
                "class": "typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua"
            },
        )
        country = countries.find("span")

        customer = review.find(
            "span",
            attrs={
                "class": "typography_heading-xxs__QKBS8 typography_appearance-default__AAY17"
            },
        )
        rates = review.find(
            "div",
            attrs={"class": "star-rating_starRating__4rrcf star-rating_medium__iN6Ty"},
        )
        stars = int(rates.img["alt"][5:8])

        reviews_content = review.find(
            "div", attrs={"class": "styles_reviewContent__0Q2Tg"}
        )
        content_title = reviews_content.find(
            "h2",
            attrs={
                "class": "typography_heading-s__f7029 typography_appearance-default__AAY17"
            },
        )
        content = reviews_content.find(
            "p",
            attrs={
                "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
            },
        )
        date_of_exp = reviews_content.find(
            "p",
            attrs={
                "class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn"
            },
        )
        time_str = date_of_exp.text[20:]
        try:
            time_obj = datetime.strptime(time_str, "%B %d, %Y")
        except:
            time_obj = datetime.strptime(time_str, "%b %d, %Y")

        if content is None:
            data = (
                customer.text,
                country.text,
                stars,
                content_title.text,
                "No Content Review",
                time_obj,
            )
            data1 = (
                "customer name",
                country.text,
                stars,
                "Content Title",
                "No Content Review",
                time_obj,
            )
        else:
            data = (
                customer.text,
                country.text,
                stars,
                content_title.text,
                content.text,
                time_obj,
            )
            data1 = (
                "customer name",
                country.text,
                stars,
                "Content Title",
                "No Content Review",
                time_obj,
            )

        try:
            cur.execute(
                "INSERT INTO Review (Name, Country, Rate, Title, Content, Dates) VALUES (%s, %s, %s, %s, %s, %s);",
                data,
            )
            con.commit()
        except:
            cur.execute(
                "INSERT INTO Review (Name, Country, Rate, Title, Content, Dates) VALUES (%s, %s, %s, %s, %s, %s);",
                data1,
            )
            con.commit()


def get_month_23():
    cur.execute(
        "SELECT COUNT(*), MONTH(Dates) FROM Review WHERE YEAR(Dates) = '2023' GROUP BY  MONTH(Dates)"
    )
    cols23 = cur.fetchall()
    for col in cols23:
        print(calendar.month_name[col[1]], col[0])
    most = max(cols23, key=lambda x: x[0])
    print("Most reviews are in:", calendar.month_name[most[1]])
    cur.close()
    con.close()

def get_country_23():
    cur.execute(
        "SELECT COUNT(*), Country FROM Review WHERE YEAR(Dates) = '2023' GROUP BY Country ORDER BY COUNT(*)"
    )

    num_country = cur.fetchall()
    for c in num_country:
        print(c[1], c[0])
    most = max(num_country, key=lambda x: x[0])
    print("Most reviews are from:", most[1])
    cur.close()
    con.close()


def get_22():
    cur.execute("SELECT * FROM Review WHERE YEAR(Dates) = '2022'")
    cur.close()
    con.close()

def compare():
    cur.execute(
        """
            SELECT a.mcount23, a.month23, b.mcount22
            FROM (
                SELECT COUNT(*) mcount23, MONTH(Dates) month23
                FROM Review
                WHERE YEAR(Dates) = '2023'
                GROUP BY  MONTH(Dates)
                )a
            INNER JOIN (
                SELECT COUNT(*) mcount22, MONTH(Dates) month22
                FROM Review
                WHERE YEAR(Dates) = '2022'
                GROUP BY  MONTH(Dates)
                )b
            ON month23 = month22
                """
    )
    month_compare = cur.fetchall()
    print("2023", "month".rjust(8), "2022".rjust(8))
    for month in month_compare:
        print(month[0], str(calendar.month_name[month[1]]).rjust(8), str(month[2]).rjust(8))
    cur.close()
    con.close()
