import database_manipulate
dbm=database_manipulate.DBOperation("/home/x/installed/pyserver/AQzLike.db")
dbm.drop(table0="Plan_P1")
dbm.create(col1=[
                ("id",["Integer","Primary Key","Autoincrement"]),
		("title",["Text","Not Null"]),
		("description",["Text"]),
		("universal",["Text"]),
		("plans",["Text"]),#先将plans序列化成多个px,[p1,p2,p3,...]
		("extrasid",["Integer"])],
                table0="Plan_P1"
)
dbm.commit()
dbm.close()
