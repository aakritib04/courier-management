from sqlalchemy import create_engine
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(db_connection_string)

# with engine.connect() as conn:
#   result = conn.execute(text("select * from sql6638399.Order"))
#   # ps = result.all()
#   # print(ps)
#   # print(type(ps))

#   # print(ps[0])
#   # print(type(ps[0]))
#   # ps_dict = ps[0]
#   # print(ps_dict._mapping)

#   results = result.all()
#   for row in results:
#     print(row._mapping)
