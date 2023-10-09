from flask import Flask, render_template, request, jsonify
from database import engine
from sqlalchemy import text
import json
import datetime
from cryptography.fernet import Fernet

app = Flask(__name__)


@app.route("/")
def hello_world():
  # return "<p>Hello, Aakriti!</p>"
  return render_template('home.html')


@app.route('/signup', methods=['POST'])
def signup():
  data = request.json
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')
  login_type = data.get('loginType')

  print(f"username: {username}, password:{password}, login_type: {login_type}")
  # key = Fernet.generate_key()
  key = 'dpnNtPQldosc53zrQZeT4zN10NVkMysyrfXao_REllo='
  fernet = Fernet(key)
  encpass = fernet.encrypt(password.encode()).decode("utf-8")
  print("original string: ", password)
  print("encrypted string: ", encpass)
  with engine.connect() as conn:

    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.User where uname='{username}' or email = '{email}';"
        ))
    if result.all():
      return jsonify(
          {'message': 'Signup failed. Username or Email already exists.'}), 401
    else:
      result = conn.execute(text(f"SELECT MAX(UID) FROM sql6638399.User;"))
      UID = result.all()[0][0]
      uid = UID + 1
      conn.execute(
          text(
              f"INSERT INTO `sql6638399`.`User`(`UID`,`uname`,`user_type`,`email`,`password`) VALUES ({uid},'{username}','{login_type}','{email}','{encpass}');"
          ))
      conn.commit()

      return render_template('signup.html', login_type=login_type, uid=uid)


@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')
  login_type = data.get('loginType')

  print(f"username: {username}, password:{password}, login_type: {login_type}")
  # key = Fernet.generate_key()
  key = 'dpnNtPQldosc53zrQZeT4zN10NVkMysyrfXao_REllo='
  # print(f"key: {key}")
  fernet = Fernet(key)
  # encpass = fernet.encrypt(password.encode()).decode("utf-8")
  # print("original string: ", password)
  # print("encrypted string: ", encpass)
  with engine.connect() as conn:
    query = f"SELECT * FROM sql6638399.User where uname='{username}';"
    print(f"query: {query}")
    result = conn.execute(text(query))
    res = result.all()
    print(f"res: {res}")
  if len(res) == 1 and password == fernet.decrypt(res[0][4]).decode("utf-8"):
    return render_template('login.html', login_type=login_type, uid=res[0][0])
  else:
    return jsonify({'message': 'Login failed. Invalid credentials.'}), 401


def get_all_orders():
  with engine.connect() as conn:
    result = conn.execute(text("select * from sql6638399.Order"))
    orders = []
    results = result.all()
    for row in results:
      orders.append(row._mapping)
    return orders


@app.route('/api/getAllOrders', methods=['GET'])
def get_all_courier_orders():

  orders = get_all_orders()
  print(f'orders: {orders}')
  return json.dumps(orders, default=str)


def get_all_customer_orders(customer):
  with engine.connect() as conn:
    result = conn.execute(
        text(f"select * from sql6638399.Order where UID={customer}"))

    orders = []
    results = result.all()
    for row in results:
      orders.append(row._mapping)
    return orders


# def get_customer_orders(customer):
#   with engine.connect() as conn:

#     result = conn.execute(
#         text(
#             f"SELECT * FROM sql6638399.Order as O join sql6638399.Order_location_details as OD on O.OID=OD.OID where UID={customer};"
#         ))

#     orders = []
#     results = result.all()
#     for row in results:
#       orders.append(row._mapping)
#     return orders


@app.route('/api/getAllUserOrders/<uid>', methods=['GET'])
def get_all_user_orders(uid):

  orders = get_all_customer_orders(uid)
  print(f'orders: {orders}')
  return json.dumps(orders, default=str)


def get_order_detail(oid):
  with engine.connect() as conn:

    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.Order as O join sql6638399.Order_location_details as OD on O.OID=OD.OID where O.OID={oid};"
        ))

    orders = []
    results = result.all()
    for row in results:
      orders.append(row._mapping)
    return orders


@app.route('/api/getOrder/<oid>', methods=['GET'])
def get_order(oid):

  orders = get_order_detail(oid)
  print(f'orders: {orders}')
  return json.dumps(orders, default=str)


def get_all_staff_details():
  with engine.connect() as conn:
    result = conn.execute(
        text(
            "SELECT U.UID, U.uname, S.sname, S.role ,U.email FROM sql6638399.User as U join sql6638399.Staff as S on U.UID=S.UID ;"
        ))
    staff = []
    results = result.all()
    for row in results:
      staff.append(row._mapping)
    return staff


@app.route('/api/getAllStaff', methods=['GET'])
def get_all_satff():

  staff = get_all_staff_details()
  print(f'staff: {staff}')
  return json.dumps(staff, default=str)


def get_all_customer_details():
  with engine.connect() as conn:
    result = conn.execute(
        text(
            "SELECT U.UID, U.uname, concat(C.firstname, ' '  ,C.lastname) as fullname, U.email FROM sql6638399.User as U join sql6638399.Customer as C on U.UID=C.UID ;"
        ))
    customer = []
    results = result.all()
    for row in results:
      customer.append(row._mapping)
    return customer


@app.route('/api/getAllCustomer', methods=['GET'])
def get_all_customer():

  customer = get_all_customer_details()
  print(f'customer: {customer}')
  return json.dumps(customer, default=str)


def get_order_of_staff(sid):
  with engine.connect() as conn:
    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.Assigned_order_to as AO join sql6638399.Order as O  on O.OID=AO.OID join sql6638399.Staff as S on AO.SID=S.UID where AO.SID={sid};"
        ))
    orders = []
    results = result.all()
    for row in results:
      orders.append(row._mapping)
    return orders


@app.route('/api/getStaffOrders/<sid>', methods=['GET'])
def get_staff_order(sid):

  orders = get_order_of_staff(sid)
  print(f'orders: {orders}')
  return json.dumps(orders, default=str)


@app.route('/assign', methods=['POST'])
def assign_order():
  #by manager
  data = request.json
  order = data.get('order')
  staff = data.get('staff')
  manager = data.get('manager')

  print(f"order: {order}, staff:{staff}, manager: {manager}")
  curr = datetime.datetime.now()
  curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")

  # add try catch
  with engine.connect() as conn:
    query = f"INSERT INTO sql6638399.Assigned_order_to values ({order}, {staff},{manager}, '{curr_date_time}');"
    print(f"query: {query}")
    conn.execute(text(query))
    conn.commit()

  return jsonify({
      'message': 'successfully assigned order',
      'role': manager
  }), 200


@app.route('/createOrder', methods=['POST'])
def create_order():
  # by customer or staff
  data = request.json
  cid = data.get('uid')
  sender = data.get('sender')
  receiver = data.get('receiver')
  pickup_address_num = data.get('pickup_address_num')
  p_city = data.get('p_city')
  p_state = data.get('p_state')
  p_pin = data.get('p_pin')
  d_address_num = data.get('d_address_num')
  d_city = data.get('d_city')
  d_state = data.get('d_state')
  d_pin = data.get('d_pin')
  order_place_date = data.get('order_place_date')
  order_status = data.get('order_status')
  payment_status = data.get('payment_status')
  pickup_date = data.get('pickup_date')

  # curr = datetime.datetime.now()
  # curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")

  # add try catch
  with engine.connect() as conn:
    query = f"INSERT INTO `sql6638399`.`Order`(`UID`,`sender`,`receiver`,`pickup_address_num`,`p_city`,`p_state`,`p_pin`,`d_address_num`,`d_city`,`d_state`,`d_pin`,`order_place_date`,`order_status`,`payment_status`,`pickup_date`) VALUES({cid},'{sender}','{receiver}','{pickup_address_num}','{p_city}','{p_state}',{p_pin},'{d_address_num}','{d_city}','{d_state}',{d_pin},'{order_place_date}','{order_status}','{payment_status}','{pickup_date}');"
    print(f"query: {query}")
    conn.execute(text(query))

    if order_status == 'confirmed' and payment_status == 'confirmed':
      query2 = f"INSERT INTO `sql6638399`.`Order_location_details` (`OID`,`date_time`,`location`) VALUES({oid},'{order_place_date}','{p_city}');"
      print(f"query2: {query2}")
      conn.execute(text(query2))

    conn.commit()

  return jsonify({
      'message': 'successfully created order',
  }), 200


@app.route('/updateOrder', methods=['POST'])
def update_order():
  # by customer
  data = request.json
  oid = data.get('oid')
  sender = data.get('sender')
  receiver = data.get('receiver')
  pickup_address_num = data.get('pickup_address_num')
  p_city = data.get('p_city')
  p_state = data.get('p_state')
  p_pin = data.get('p_pin')
  d_address_num = data.get('d_address_num')
  d_city = data.get('d_city')
  d_state = data.get('d_state')
  d_pin = data.get('d_pin')
  order_status = data.get('order_status')
  payment_status = data.get('payment_status')
  pickup_date = data.get('pickup_date')

  curr = datetime.datetime.now()
  curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  # add try catch
  with engine.connect() as conn:
    query = f"UPDATE `sql6638399`.`Order` SET `sender` = '{sender}',`receiver` = '{receiver}',`pickup_address_num` = '{pickup_address_num}',`p_city` = '{p_city}',`p_state` = '{p_state}',`p_pin` = {p_pin},`d_address_num` = '{d_address_num}',`d_city` = '{d_city}',`d_state` = '{d_state}',`d_pin` = {d_pin},`order_status` = '{order_status}',`payment_status` = '{payment_status}',`pickup_date` = '{pickup_date}' WHERE `OID` = {oid};"
    print(f"query: {query}")
    conn.execute(text(query))

    if order_status == 'confirmed' and payment_status == 'confirmed':
      query2 = f"INSERT INTO `sql6638399`.`Order_location_details` (`OID`,`date_time`,`location`) VALUES({oid},'{curr_date_time}','{p_city}');"
      print(f"query2: {query2}")
      conn.execute(text(query2))

    conn.commit()

  return jsonify({
      'message': 'successfully updated order',
  }), 200


@app.route('/updateDeliveryDetails', methods=['POST'])
def update_delivery_details():
  #by staff
  data = request.json
  oid = data.get('oid')
  pickup_date = data.get('pickup_date')
  pickup_by = data.get('pickup_by')
  delivery_date = data.get('delivery_date')
  delivery_by = data.get('delivery_by')
  location = data.get('location')

  curr = datetime.datetime.now()
  date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  # add try catch
  with engine.connect() as conn:
    query = f"UPDATE `sql6638399`.`Order` SET `pickup_date` = '{pickup_date}',`pickup_by` = '{pickup_by}',`delivery_date` = '{delivery_date}',`delivery_by` = '{delivery_by}'  WHERE `OID` = {oid};"
    print(f"query: {query}")
    conn.execute(text(query))

    if location is not None:
      query2 = f"INSERT INTO `sql6638399`.`Order_location_details` (`OID`,`date_time`,`location`) VALUES({oid},'{date_time}','{location}');"
      print(f"query2: {query2}")
      conn.execute(text(query2))
    conn.commit()

  return jsonify({
      'message': 'successfully updated order',
  }), 200


@app.route('/cancelOrder/<oid>', methods=['DELETE'])
def cancel_order(oid):
  #by staff/customer

  curr = datetime.datetime.now()
  date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  # add try catch
  with engine.connect() as conn:
    query = f"UPDATE `sql6638399`.`Order` SET `order_status` = 'cancel',`payment_status` = 'cancel' WHERE `OID` = {oid};"
    print(f"query: {query}")
    conn.execute(text(query))

    query2 = f"DELETE FROM `sql6638399`.`Order_location_details` WHERE OID = {oid};"
    print(f"query: {query2}")
    conn.execute(text(query2))

    query3 = f"DELETE FROM `sql6638399`.`Assigned_order_to` WHERE OID = {oid};"
    print(f"query: {query3}")
    conn.execute(text(query3))

    conn.commit()

  return jsonify({
      'message': 'successfully canceled order',
  }), 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
