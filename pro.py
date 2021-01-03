from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate


app2=Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI']="postgresql://user1:test123@localhost/employee"
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app2)
#migrate=Migrate(app2,db)
class Info(db.Model):
    __tablename__='info2'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String())
    timestamp=db.Column(db.String())

    def __init__(self,name,timestamp):
        self.name=name
        self.timestamp=timestamp

    def __repr__(self):
        return f"<Emp {self.name}>"

@app2.route('/info2',methods=['POST','GET'])
def handle_info2():
    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
            new_info=Info(name=data['name'],timestamp=data['timestamp'])
            db.session.add(new_info)
            db.session.commit()
            return "successfully created"
        else:
            return {"error:" "The request payload is not in JSON format"}
    elif request.method=='GET':
        info2=Info.query.all()
        results=[
            {
                "name":info.name,
                "timestamp":info.timestamp,
            }for info in info2]
        return {"count": len(results), "info2":results}
db.create_all()
#app2.run()

@app2.route('/info2/<info_id>',methods=['GET','PUT','DELETE'])
def handles_info2(info_id):
    info=Info.query.get_or_404(info_id)
    if request.method=='GET':
        response={
            "name":info.name,
            "timestamp":info.timestamp,
        }
        return {"message":"success","info":response}
    elif request.method=='PUT':
        data=request.get_json()
        info.name=data['name']
        info.timestamp=data['timestamp']
        db.session.add(info)
        db.session.commit()
        return "successfully updated"
    elif request.method=='DELETE':
        db.session.delete(info)
        db.session.commit()
        return "successfully deleted"
app2.run()
