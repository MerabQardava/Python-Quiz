import requests
import json
import sqlite3

sus=1

url=f'https://api.nytimes.com/svc/books/v3/reviews.json?title=Becoming.json?api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My'


a=requests.get('https://api.nytimes.com/svc/books/v3//lists/names.json?&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')

print(a.status_code)
print(a.headers)
res=a.json()
# print(res)
# print(json.dumps(res, indent=4))

with open('Books.json', 'w') as f:
    json.dump(res, f, indent=4)


conn = sqlite3.connect('book_category.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS book_category
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_name VARCHAR(20),
            display_name VARCHAR(20),
            list_name_encoded VARCHAR(20),
            oldest_published_date VARCHAR(20),
            newest_published_date VARCHAR(20),
            updated VARCHAR(20)
            )''')
all = []
for i in res['results']:
    list_name = i['list_name']
    display_name = i['display_name']
    list_name_encoded = i['list_name_encoded']
    oldest_published_date = i['oldest_published_date']
    newest_published_date = i['newest_published_date']
    updated = i['updated']
    row = (list_name, display_name, list_name_encoded, oldest_published_date, newest_published_date, updated)
    all.append(row)
c.executemany('INSERT INTO book_category (list_name, display_name, list_name_encoded, oldest_published_date, newest_published_date, updated) VALUES (?, ?, ?, ?, ?, ?)', all)
conn.commit()
conn.close()


while sus==1 :
    num = int(input("\nრისი გაკეთება გსურთ?\nკატეგორიების სია-1\nკატეგორიის გახსნა-2\nწიგნზე ინფორმაციის ნახვა-3\nდახურვა-0\n "))
    if num==1:
        for x in range (0,len(res["results"])):
            print(res["results"][x]["list_name"])

    elif num==2:
        try:
            cat=str(input("ჩაწერეთ კატეგორია \n "))
            cat=cat.replace(" ","-")
            b = requests.get(f'https://api.nytimes.com/svc/books/v3//lists/current/{cat}.json?&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')
            res2=b.json()
            # print(json.dumps(res2,indent=3))
            for y in range(0,len(res2["results"]["books"])):
                print(res2["results"]["books"][y]["title"])
        except:
            print("სამწუხაროდ კატეგორია არ იქნა ნაპოვნი, გადაამოწმეთ დასახელება ან აირჩიეთ სხვა.")

    elif num==3:
        try:
            book_name=str(input("ჩაწერეთ წიგნის დასახელება \n "))
            c=requests.get(f'https://api.nytimes.com/svc/books/v3/reviews.json?title={book_name}&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')
            res3=c.json()
            # print(json.dumps(res3,indent=3))
            print(f"\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                  f"\nწიგნის დასახელება: {res3['results'][0]['book_title']}"
                  f"\nგამოშვების თარიღი: {res3['results'][0]['publication_dt']}"
                  f"\nავტორი: {res3['results'][0]['book_author']}"
                  f"\nმოკლე აღწერა: {res3['results'][0]['summary']}"
                  f"\nსრული Review: {res3['results'][0]['url']}"
                  f"\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        except:
            print("სამწუხაროდ წიგნი არ იქნა ნაპოვნი, გადაამოწმეთ დასახელება ან აირჩიეთ სხვა.")
    elif num==0:
        sus=0


