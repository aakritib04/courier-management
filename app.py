from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import engine
from sqlalchemy import text
import json
import datetime
from cryptography.fernet import Fernet

app = Flask(__name__)


@app.route("/")
def landing():
  # return "<p>Hello, Aakriti!</p>"
  return render_template('home.html')


@app.route("/test")
def hello_TEST():
  # return "<p>Hello, Aakriti!</p>"
  return render_template('signup.html', uid=10, signupType='aakriti')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
  data = request.json
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')
  signupType = data.get('signupType')

  print(f"username: {username}, password:{password}, signupType: {signupType}")
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
      print("IN IF ...GOT SAME MATCH")
      return jsonify(
          {'message': 'Signup failed. Username or Email already exists.'}), 401
    else:

      conn.execute(
          text(
              f"INSERT INTO `sql6638399`.`User`(`UID`,`uname`,`user_type`,`email`,`password`) VALUES ({uid},'{username}','{signupType}','{email}','{encpass}');"
          ))
      conn.commit()
      return jsonify({
          'message': 'Signup Succesful.',
          "uid": uid,
          "signupType": signupType
      }), 200


@app.route('/register/<signupType>/<uid>')
def register(signupType, uid):
  print("in register")
  return render_template('signup.html', signupType=signupType, uid=uid)


@app.route('/signup_user/<signupType>/<uid>', methods=['GET', 'POST'])
def sign_up_user(signupType, uid):
  data = request.json
  print(data)
  if signupType == 'staff':
    staffName = data.get('staffName')
    role = data.get('role')
    query = f"INSERT INTO `sql6638399`.`Staff`(`UID`,`sname`, `role`) VALUES  ({uid},   '{staffName}',  '{role}');"
  elif signupType == 'customer':
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    phoneNum = data.get('phoneNum')
    query = f"INSERT INTO `sql6638399`.`Customer`(`UID`,`firstname`,`lastname`,`phone_num`) VALUES({uid},'{firstName}','{lastName}',{phoneNum});"
  elif signupType == 'manager':
    mname = data.get('managerName')
    query = f"INSERT INTO `sql6638399`.`Manager`(`UID`,`mname`) VALUES({uid},'{mname}');"
  with engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()

    return jsonify({
        'message': 'Details Signup Succesful.',
        "uid": uid,
        "signupType": signupType
    }), 200


@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')
  login_type = data.get('loginType')

  print(f"username: {username}, password:{password}, login_type: {login_type}")
  key = 'dpnNtPQldosc53zrQZeT4zN10NVkMysyrfXao_REllo='
  fernet = Fernet(key)
  with engine.connect() as conn:
    query = f"SELECT * FROM sql6638399.User where uname='{username}';"
    print(f"query: {query}")
    result = conn.execute(text(query))
    res = result.all()
    print(f"res: {res}")
  if len(res) == 1 and password == fernet.decrypt(
      res[0][4]).decode("utf-8") and login_type == res[0][2]:
    return jsonify({
        'message': 'Login Succesful.',
        "uid": res[0][0],
        "loginType": res[0][2]
    }), 200
  else:
    return jsonify({'message': 'Login failed. Invalid credentials.'}), 401


@app.route('/login/<loginType>/<uid>')
def login_dashboard(loginType, uid):
  print("in login dashboard")
  if loginType == 'customer':
    page = 'customer_dashboard.html'
  elif loginType == 'staff':
    page = 'staff_dashboard.html'
  elif loginType == 'manager':
    page = 'manager_dashboard.html'
  else:
    return jsonify({'message': 'Invalid user'}), 401
  return render_template(page, uid=uid, loginType=loginType)


def get_all_orders():
  with engine.connect() as conn:
    results = conn.execute(text("select * from sql6638399.Order"))
    orders = [r._asdict() for r in results]
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

    order = [r._asdict() for r in result]
    return order


@app.route('/api/getAllUserOrders/<uid>', methods=['GET'])
def get_all_user_orders(uid):

  orders = get_all_customer_orders(uid)
  print(f'orders: {orders}')
  return json.dumps(orders, default=str)


def get_order_detail(oid):
  with engine.connect() as conn:

    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.Order as O left join sql6638399.Assigned_order_to as AO on AO.OID=O.OID left join sql6638399.Staff as S on AO.SID=S.UID where O.OID={oid};"
        ))

    order = [r._asdict() for r in result]
    return order


# def get_order_detail(oid):
#   with engine.connect() as conn:

#     result = conn.execute(
#         text(
#             f"SELECT * FROM sql6638399.Order as O join sql6638399.Assigned_order_to as AO on AO.OID=O.OID join sql6638399.Staff as S on AO.SID=S.UID where O.OID={oid};"
#         ))

#     order = [r._asdict() for r in result]
#     return order

# def get_order_with_location_detail(oid):
#   with engine.connect() as conn:

#     result = conn.execute(
#         text(
#             f"SELECT * FROM sql6638399.Order as O left join sql6638399.Order_location_details as OD on O.OID=OD.OID left join sql6638399.Assigned_order_to as AO on AO.OID=O.OID where O.OID={oid};"
#         ))

#     order = [r._asdict() for r in result]
#     return order


def get_order_with_location_detail(oid):
  with engine.connect() as conn:

    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.Order_location_details where OID={oid};"
        ))

    order = [r._asdict() for r in result]
    return order


@app.route('/order/<oid>/<uid>/<loginType>', methods=['GET'])
def get_order_page(oid, uid, loginType):

  order = get_order_detail(oid)
  print(f'orders: {order}')
  # return json.dumps(order, default=str)
  if loginType == 'customer':
    page = 'customer_view_order_details.html'
  elif loginType == 'staff':
    page = 'customer_view_order_details.html'
  elif loginType == 'manager':
    page = 'manager_view_order_details.html'
  else:
    return jsonify({'message': 'Invalid user'}), 401
  print(f"page: {page}")
  return render_template(page, oid=oid, uid=uid, loginType=loginType)


@app.route('/create_order_page/<loginType>/<uid>', methods=['GET'])
def create_order_page(loginType, uid):
  if loginType == 'customer':
    page = 'create_order.html'
  elif loginType == 'staff':
    page = 'create_order_by_staff.html'
  else:
    return jsonify({'message': 'Invalid user'}), 401
  print(f"page: {page}")
  return render_template(page, uid=uid, loginType=loginType)


@app.route('/update_order_page/<loginType>/<oid>/<uid>', methods=['GET'])
def update_order_page(loginType, oid, uid):
  if loginType == 'customer':
    page = 'update_order.html'
  elif loginType == 'staff':
    page = 'update_order_by_staff.html'
  else:
    return jsonify({'message': 'Invalid user'}), 401
  print(f"page: {page}")
  return render_template(page, oid=oid, loginType=loginType, uid=uid)


@app.route('/api/getOrder/<oid>', methods=['GET'])
def get_order(oid):

  order = get_order_detail(oid)
  print(f'orders: {order}')
  return json.dumps(order, default=str)


@app.route('/api/getOrderWithLocation/<oid>', methods=['GET'])
def get_order_with_location(oid):

  order = get_order_with_location_detail(oid)
  print(f'orders with location: {order}')
  return json.dumps(order, default=str)


def get_all_staff_details():
  print("in get all staff details")
  with engine.connect() as conn:
    result = conn.execute(
        text(
            "SELECT U.UID, U.uname, S.sname, S.role ,U.email FROM sql6638399.User as U join sql6638399.Staff as S on U.UID=S.UID ;"
        ))
    staff_list = []
    results = result.all()
    for row in results:
      # Create a dictionary for each row
      staff_dict = {
          'UID': row.UID,
          'Staffname': row.sname,
          'email': row.email,
          'role': row.role
      }
      staff_list.append(staff_dict)
    return staff_list


# def get_all_staff_details():
#   with engine.connect() as conn:
#     result = conn.execute(
#         text(
#             "SELECT U.UID, U.uname, S.sname, S.role ,U.email FROM sql6638399.User as U join sql6638399.Staff as S on U.UID=S.UID ;"
#         ))
#     staff = []
#     results = result.all()
#     for row in results:
#       staff.append(row._mapping)
#     return staff


@app.route('/api/getAllStaff', methods=['GET'])
def get_all_satff():

  staff = get_all_staff_details()
  print(f'staff: {staff}')
  return json.dumps(staff, default=str)


# def get_all_customer_details():
#   with engine.connect() as conn:
#     result = conn.execute(
#         text(
#             "SELECT U.UID, U.uname, concat(C.firstname, ' '  ,C.lastname) as fullname, U.email , C.phone_num FROM sql6638399.User as U join sql6638399.Customer as C on U.UID=C.UID ;"
#         ))
#     customer = []
#     results = result.all()
#     for row in results:
#       customer.append(row._mapping)
#     return customer


def get_all_customer_details():
  with engine.connect() as conn:
    result = conn.execute(
        text(
            "SELECT U.UID, U.uname, concat(C.firstname, ' '  ,C.lastname) as fullname, U.email , C.phone_num FROM sql6638399.User as U join sql6638399.Customer as C on U.UID=C.UID ;"
        ))
    customer_list = []
    results = result.all()
    for row in results:
      # Create a dictionary for each row
      customer_dict = {
          'fullname': row.fullname,
          'email': row.email,
          'phone_num': row.phone_num
      }
      customer_list.append(customer_dict)
    return customer_list


@app.route('/api/getAllCustomer', methods=['GET'])
def get_all_customer():

  customer = get_all_customer_details()
  print(f'customer: {customer}')
  return json.dumps(customer)


def get_order_of_staff(sid):
  with engine.connect() as conn:
    result = conn.execute(
        text(
            f"SELECT * FROM sql6638399.Assigned_order_to as AO join sql6638399.Order as O  on O.OID=AO.OID join sql6638399.Staff as S on AO.SID=S.UID where AO.SID={sid};"
        ))
    orders = []
    results = result.all()
    orders = [r._asdict() for r in results]
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
    query1 = f"SELECT * FROM sql6638399.Assigned_order_to where OID = {order};"
    result = conn.execute(text(query1))
    results = result.all()
    if results:
      query = f"UPDATE `sql6638399`.`Assigned_order_to` SET `SID` = {staff},`MID` = {manager},`assigned_date` = '{curr_date_time}' WHERE `OID` = {order};"
    else:
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
  pickup_address_num = data.get('pickupAddress')
  p_city = data.get('pickupCity')
  p_state = data.get('pickupState')
  p_pin = data.get('pickupPin')
  d_address_num = data.get('deliveryAddress')
  d_city = data.get('deliveryCity')
  d_state = data.get('deliveryState')
  d_pin = data.get('deliveryPin')
  pickup_date = data.get('pickupDate')
  curr = datetime.datetime.now()
  curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  order_place_date = curr_date_time
  payment_status = 'Confirmed'
  order_status = 'To be confirmed'

  # curr = datetime.datetime.now()
  # curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")

  # add try catch
  with engine.connect() as conn:
    result = conn.execute(text(f"SELECT MAX(OID) FROM sql6638399.Order;"))
    OID = result.all()[0][0]
    if OID:
      oid = OID + 1
    else:
      oid = 1
    query = f"INSERT INTO `sql6638399`.`Order`(`OID`, `UID`,`sender`,`receiver`,`pickup_address_num`,`p_city`,`p_state`,`p_pin`,`d_address_num`,`d_city`,`d_state`,`d_pin`,`order_place_date`,`pickup_date`, `payment_status`, `order_status`) VALUES({oid}, {cid},'{sender}','{receiver}','{pickup_address_num}','{p_city}','{p_state}',{p_pin},'{d_address_num}','{d_city}','{d_state}',{d_pin},'{order_place_date}','{pickup_date}', '{payment_status}', '{order_status}');"
    print(f"query: {query}")
    conn.execute(text(query))

    query2 = f"INSERT INTO `sql6638399`.`Order_location_details` (`OID`,`date_time`,`location`) VALUES({oid},'{order_place_date}','{p_city}');"
    print(f"query2: {query2}")
    conn.execute(text(query2))

    query3 = f"INSERT INTO `sql6638399`.`Assigned_order_to`(`OID`) VALUES({oid});"
    print(f"query3: {query3}")
    conn.execute(text(query3))

    conn.commit()

  return jsonify({
      'message': 'successfully created order',
  }), 200


# @app.route('/createOrder', methods=['POST'])
# def create_order():
#   # by customer or staff
#   data = request.json
#   cid = data.get('uid')
#   sender = data.get('sender')
#   receiver = data.get('receiver')
#   pickup_address_num = data.get('pickup_address_num')
#   p_city = data.get('p_city')
#   p_state = data.get('p_state')
#   p_pin = data.get('p_pin')
#   d_address_num = data.get('d_address_num')
#   d_city = data.get('d_city')
#   d_state = data.get('d_state')
#   d_pin = data.get('d_pin')
#   order_place_date = data.get('order_place_date')
#   order_status = data.get('order_status')
#   payment_status = data.get('payment_status')
#   pickup_date = data.get('pickup_date')

#   # curr = datetime.datetime.now()
#   # curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")

#   # add try catch
#   with engine.connect() as conn:
#     query = f"INSERT INTO `sql6638399`.`Order`(`UID`,`sender`,`receiver`,`pickup_address_num`,`p_city`,`p_state`,`p_pin`,`d_address_num`,`d_city`,`d_state`,`d_pin`,`order_place_date`,`order_status`,`payment_status`,`pickup_date`) VALUES({cid},'{sender}','{receiver}','{pickup_address_num}','{p_city}','{p_state}',{p_pin},'{d_address_num}','{d_city}','{d_state}',{d_pin},'{order_place_date}','{order_status}','{payment_status}','{pickup_date}');"
#     print(f"query: {query}")
#     conn.execute(text(query))

#     # if order_status == 'confirmed' and payment_status == 'confirmed':
#     #   query2 = f"INSERT INTO `sql6638399`.`Order_location_details` (`OID`,`date_time`,`location`) VALUES({oid},'{order_place_date}','{p_city}');"
#     #   print(f"query2: {query2}")
#     #   conn.execute(text(query2))

#     conn.commit()

#   return jsonify({
#       'message': 'successfully created order',
#   }), 200


@app.route('/updateOrder/<oid>', methods=['POST'])
def update_order(oid):
  # by customer
  data = request.json
  sender = data.get('sender')
  receiver = data.get('receiver')
  pickup_address_num = data.get('pickupAddress')
  p_city = data.get('pickupCity')
  p_state = data.get('pickupState')
  p_pin = data.get('pickupPin')
  d_address_num = data.get('deliveryAddress')
  d_city = data.get('deliveryCity')
  d_state = data.get('deliveryState')
  d_pin = data.get('deliveryPin')
  pickup_date = data.get('pickupDate')

  curr = datetime.datetime.now()
  curr_date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  # add try catch
  with engine.connect() as conn:
    query = f"UPDATE `sql6638399`.`Order` SET `sender` = '{sender}',`receiver` = '{receiver}',`pickup_address_num` = '{pickup_address_num}',`p_city` = '{p_city}',`p_state` = '{p_state}',`p_pin` = {p_pin},`d_address_num` = '{d_address_num}',`d_city` = '{d_city}',`d_state` = '{d_state}',`d_pin` = {d_pin}, `pickup_date` = '{pickup_date}' WHERE `OID` = {oid};"
    print(f"query: {query}")
    conn.execute(text(query))

    query2 = f"UPDATE `sql6638399`.`Order_location_details` SET `date_time` = '{curr_date_time}',`location` = '{p_city}' WHERE `OID` = {oid};"
    print(f"query2: {query2}")
    conn.execute(text(query2))

    conn.commit()

  return jsonify({
      'message': 'successfully updated order',
  }), 200


@app.route('/updateDeliveryDetails/<oid>', methods=['POST'])
def update_delivery_details(oid):
  #by staff
  data = request.json
  order_status = data.get('orderStatus')
  pickup_by = data.get('pickupBy')
  delivery_date = data.get('deliveryDate')
  delivery_by = data.get('deliveryBy')
  location = data.get('location')
  print(f"order_status: {order_status}")
  curr = datetime.datetime.now()
  date_time = curr.strftime("%Y-%m-%d %H:%M:%S")
  # add try catch
  with engine.connect() as conn:
    query = f"UPDATE `sql6638399`.`Order` SET "
    if order_status:
      query += f" `order_status` = '{order_status}', "
    if pickup_by:
      query += f" `pickup_by` = '{pickup_by}', "
    if delivery_date:
      query += f" `delivery_date` = '{delivery_date}', "
    if delivery_by:
      query += f" `delivery_by` = '{delivery_by}', "
    query = query.rstrip(', ')
    print(f"query: {query}")
    query += f" WHERE `OID` = {oid}; "

    print(f"query: {query}")
    conn.execute(text(query))

    if location:
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
  print("in cancel order")
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
