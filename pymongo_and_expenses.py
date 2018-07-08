from pymongo import mongo_client
import pprint, time, datetime, openpyxl as px

def create_posts(choice, sheet_data, sheet_max):
    data = []
    if choice == 'month':
        for i in range(2, sheet_max+1):
            data.append({
            "Expense": sheet_data['A{}'.format(i)].value,
            "Category": sheet_data['B{}'.format(i)].value,
            "Notes": sheet_data['C{}'.format(i)].value,
            "Cost": sheet_data['D{}'.format(i)].value,
            })

    if choice == 'category':
        for i in range(2, sheet_max+1):
            data.append({
                "Keyword": sheet_data['A{}'.format(i)].value,
                "Category": sheet_data['B{}'.format(i)].value,
            })
    #print(data)
    return data

def update_expenses():
    expenses = create_posts('month', month_data, month_max)

    #Find a way to update this in mongo
    post = {
    "month"+month:
    {
    "Month": month,
    "Expenses": expenses
    }
    }

    posts = db["yr{}".format(year)]

    posts.insert_one(post)

    pprint.pprint(posts.find())
    print('Success!')

def category_upload():
    categorical_data = wb.get_sheet_by_name("Category Words")
    categorical_max = categorical_data.max_row

    categories = create_posts('category', categorical_data, categorical_max)

    post = {
        "Keywords": categories
        }
    
    posts = db["category_words"]
    posts.insert_one(post)
    pprint.pprint(posts.find())
    print('Success!')



print('(Make sure mongod is running...)')
time.sleep(1)

labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
year = '2018'
# year = datetime.datetime.today().strftime('%Y')
# month = datetime.datetime.today().strftime('%m')
wb = px.load_workbook('{} Monthly Expenses.xlsx'.format(year))
month = input('what month?\n')
month_data = wb.get_sheet_by_name(labels[int(month)-1])
month_max = month_data.max_row


client = mongo_client.MongoClient('localhost', 27017)

db = client.month_expenses

# update_expenses()
category_upload()
