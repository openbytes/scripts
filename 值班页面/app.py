# coding=utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime

year = datetime.datetime.now().year
month = datetime.datetime.now().month

# 创建应用
app = Flask(__name__)

# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@172.10.4.92/dianyou"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    duty_day = db.Column(db.String(30), unique=True)
    duty_week_day = db.Column(db.String(50))
    duty_people = db.Column(db.String(200))
    phone = db.Column(db.String(11))


# data = User.query.filter(User.duty_day.startswith(f"{year}" + "-" + f"0{month - 1}")).all()
# for i in data:
#     print(str(i.duty_day,'utf-8'))
# 生成新表
# db.create_all()
#
@app.route('/')
def show_all():
    # 数据库里面保存的日期数据是01,02,03,04...09,这里需要在个位数上面加一个0
    if (month - 1) < 10:
        data = User.query.filter(User.duty_day.startswith(f"{year}" + "-" + f"0{month - 1}")).all()
    else:
        data = User.query.filter(User.duty_day.startswith(f"{year}" + "-" + f"{month - 1}")).all()
    labels = ["时间", "值班人员", "值班人员", "联系电话"]
    return render_template('index.html', labels=labels, content=data, month=month, year=year)


@app.route('/tj')
def tj():
    # group_by语句不能用flask-sqlalchemy的对象进行操作，必须用sqlalchemy最原始的方式进行操作，并要冲sqlalchemy中导入func这个工具
    # 进行分组查询，query中必须包含分组后必须显示出的字段
    # http://www.zhengdazhi.com/archives/1679
    if (month - 1) < 10:
        data = db.session.query(User.duty_people, func.count(User.duty_people)).filter(
            User.duty_day.like(f"{year}" + "-"f"0{month}" + "-" + "%")).group_by(User.duty_people).all()
        print(data)
    else:
        data = db.session.query(User.duty_people, func.count(User.duty_people)).filter(
            User.duty_day.like(f"{year}" + "-"f"{month}" + "-" + "%")).group_by(User.duty_people).all()
    labels = ["值班人员", "值班天数"]
    return render_template('tj.html', labels=labels, content=data, month=month, year=year)


if __name__ == '__main__':
    app.run()
