from datetime import datetime
from create_data import user_data

from project_setting import User


def create_data():
    if not User.exists():
        User.create_table()
    for data in user_data:
        # {'birthday' 'email''first_name''last_name''no': 'phone''state''zipcode'}
        date_value = data.get("birthday")
        data["birthday"] = datetime(date_value.year, date_value.month, date_value.day)
        user = User(**data)
        user.save()

    print("数据总数", User.count())


# create_data()

def index_query():
    for u1 in User.phone_index.query("0"):
        print(u1.no, u1.first_name, u1.last_name)
    print(list(User.phone_index.query("1", limit=1)))


if __name__ == '__main__':
    index_query()
