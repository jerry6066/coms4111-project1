from flask import Flask
import os
from flask import Flask, request, render_template, g, redirect, Response
from markupsafe import escape
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import psycopg2
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://bz2378:7434@35.227.37.35/proj1part2"

engine = psycopg2.connect(DATABASEURI)


@app.route('/', methods=['GET'])
def index():
    return redirect('/prod')


@app.route('/helperuser', methods=['GET'])
def helperuser():
    # TODO get all user info
    def getUsers():
        cur = engine.cursor()
        datas = []
        try:
            cur.execute("SELECT uid, screen_name, address FROM Users")
            for result in cur:
                data = {
                    'uid': '',
                    'username': '',
                    'address': ''
                }
                data['uid'] = ''.join(list(result[0])).rstrip()
                data['username'] = ''.join(list(result[1])).rstrip()
                data['address'] = ''.join(list(result[2])).rstrip()
                datas.append(data)
        except Exception as e:
            return str(e)
        finally:
            cur.close()
        return datas
    data = getUsers()
    return render_template('helperuser.html', data=data)


@app.route('/helperprod', methods=['GET'])
def helperprod():
    # data = [{
    #     'cid': '0001',
    #     'name': 'apple',
    #     'stock': '10',
    #     'cost': '$20'
    #     },
    #     {
    #     'cid': '0002',
    #     'name': 'banana',
    #     'stock': '20',
    #     'cost': '$21'
    #     }]
    # TODO get all product info
    def getCommodities():
        cur = engine.cursor()
        cur.execute("SELECT c.cid, c.name, c.cost, c.stock FROM Commodities c")
        datas = []
        for result in cur:
            data = {
                'cid': '0002',
                'name': 'banana',
                'stock': '20',
                'cost': '$21'
            }
            cid = ''.join(list(result[0])).rstrip()
            name = ''.join(list(result[1])).rstrip()
            cost = result[2]
            stock = result[3]
            data['cid'] = cid
            data['name'] = name
            data['stock'] = stock
            data['cost'] = cost
            datas.append(data)
        cur.close()
        return datas
    data = getCommodities()
    return render_template('helperprod.html', data=data)


@app.route('/prod', methods=['GET'])
def product():
    args = request.args
    cate = None
    page = None
    key = None
    if 'cate' in args:
        cate = args['cate']
    else:
        cate = 'All'
    if 'page' in args:
        page = args['page']
    else:
        page = 1
    if 'key' in args:
        key = args['key']
    else:
        key = ""

    # TODO search
    def search(cate, key, page):
        page = int(page)
        if cate == 'All' and key == "":
            # TODO normal search by page
            # one page 5 items
            def getBYpage():
                cur = engine.cursor()
                cur.execute("SELECT c.cid, c.name, c.cost, c.stock, ca.category_name "
                            "FROM Commodities c, Categories ca, Type_is T WHERE T.cid = c.cid AND T.caid = ca.caid")
                datas = []
                p = 5 * page
                for result in cur:
                    if 0 < p <= 5:
                        pt = {
                            'cid': '',
                            'name': '',
                            'stock': '',
                            'cost': '',
                            'category': ''
                        }
                        cid = ''.join(list(result[0])).rstrip()
                        name = ''.join(list(result[1])).rstrip()
                        cost = result[2]
                        stock = result[3]
                        # category = ''.join(list(result[4])).rstrip()
                        category = result[4]
                        pt['cid'] = cid
                        pt['name'] = name
                        pt['stock'] = stock
                        pt['cost'] = cost
                        pt['category'] = category
                        datas.append(pt)
                    p = p - 1
                cur.close()
                return datas
            return getBYpage()

            pass
        elif cate != 'All' and key == "":
            # TODO search by category and page
            def getBYpageANDcategory():
                cur = engine.cursor()
                c = "%" + cate + "%"
                cur.execute("SELECT c.cid, c.name, c.cost, c.stock "
                            "FROM Commodities c, Categories ca, Type_is T WHERE T.cid = c.cid "
                            "AND T.caid = ca.caid AND ca.category_name LIKE %s", (c, ))
                datas = []
                p = 5 * page
                for result in cur:
                    if 0 < p <= 5:
                        pt = {
                            'cid': '',
                            'name': '',
                            'stock': '',
                            'cost': '',
                            'category': ''
                        }
                        cid = ''.join(list(result[0])).rstrip()
                        name = ''.join(list(result[1])).rstrip()
                        cost = result[2]
                        stock = result[3]
                        pt['cid'] = cid
                        pt['name'] = name
                        pt['stock'] = stock
                        pt['cost'] = cost
                        pt['category'] = cate
                        datas.append(pt)
                    p = p - 1
                cur.close()
                return datas
            return getBYpageANDcategory()
            pass

        elif key != "" and cate == 'All':
            # TODO search by keywords and page
            def getBYpageANDkey():
                cur = engine.cursor()
                k = '%' + key + '%'
                cur.execute("SELECT c.cid, c.name, c.cost, c.stock, ca.category_name "
                            "FROM Commodities c, Categories ca, Type_is T WHERE T.cid = c.cid "
                            "AND T.caid = ca.caid AND c.name LIKE %s ", (k, ))
                datas = []
                p = 5 * page
                for result in cur:
                    if 0 < p <= 5:
                        pt = {
                            'cid': '',
                            'name': '',
                            'stock': '',
                            'cost': '',
                            'category': ''
                        }
                        pt['cid'] = ''.join(list(result[0])).rstrip()
                        pt['name'] = ''.join(list(result[1])).rstrip()
                        pt['stock'] = result[3]
                        pt['cost'] = result[2]
                        pt['category'] = result[4]
                        datas.append(pt)
                    p = p - 1
                cur.close()
                return datas
            return getBYpageANDkey()
            pass
        else:
            # TODO search by keywords and category and page
            def getBYpageANDkeyANDcategory():
                cur = engine.cursor()
                k = '%' + key + '%'
                c = "%" + cate + "%"
                cur.execute("SELECT c.cid, c.name, c.cost, c.stock, ca.category_name "
                            "FROM Commodities c, Categories ca, Type_is T WHERE T.cid = c.cid "
                            "AND T.caid = ca.caid AND c.name LIKE %s AND ca.category_name LIKE %s", (k, c))
                datas = []
                p = 5 * page
                for result in cur:
                    if 0 < p <= 5:
                        pt = {
                            'cid': '',
                            'name': '',
                            'stock': '',
                            'cost': '',
                            'category': ''
                        }
                        # cid = ''.join(list(result[0])).rstrip()
                        # name = ''.join(list(result[1])).rstrip()
                        # cost = result[2]
                        # stock = result[3]
                        # category = ''.join(list(result[4])).rstrip()

                        pt['cid'] = ''.join(list(result[0])).rstrip()
                        pt['name'] = ''.join(list(result[1])).rstrip()
                        pt['stock'] = result[3]
                        pt['cost'] = result[2]
                        pt['category'] = result[4]
                        datas.append(pt)
                    p = p - 1
                cur.close()
                return datas
            return getBYpageANDkeyANDcategory()
            pass
        # return products in array

    # TODO get categories
    def get_cate():
        # TODO return categories
        categories = ['All']
        cur = engine.cursor()
        cur.execute("SELECT c.category_name FROM Categories c")
        for result in cur:
            # ca = ''.join(list(result[0])).rstrip()
            categories.append(result[0].strip())
        cur.close()
        return categories
        pass

    data = {}
    data['title'] = 'Products Page'
    data['page'] = page
    data['cate'] = cate
    data['key'] = key
    data['categories'] = get_cate()
    data['products'] = search(cate, key, page)
    return render_template('index.html', data=data)


@app.route('/cid', methods=['GET'])
def cid():
    args = request.args
    if 'cid' not in args:
        return redirect('/error')
    cid = args['cid']

    def getItemInfo(cid):
        # TODO given cid, return info
        basicInfo = {
        'cid': cid,
        'name': '',
        'stock': '',
        'cost': '',
        'category': '',
        'avg_score': ''
        }
        try:
            cur = engine.cursor()
            cur.execute("SELECT Com.name, Com.stock, Com.cost, Cate.category_name, "
                        "(SELECT AVG(r.score) FROM Commodities c, Rated_by r "
                        "WHERE c.cid = r.cid AND c.cid = %s) AS average_score "
                        "FROM Commodities Com, Type_is T, Categories Cate "
                        "WHERE Com.cid = T.cid AND T.caid = Cate.caid AND Com.cid = %s", (cid, cid))
            result = cur.fetchone()
            # basicInfo['name'] = ''.join(list(result[0])).rstrip()

            if result[0] != None:
                basicInfo['name'] = result[0]
                basicInfo['stock'] = result[1]
                basicInfo['cost'] = result[2]
                # basicInfo['category'] = ''.join(list(result[3])).rstrip()
                basicInfo['category'] = result[3]
                basicInfo['avg_score'] = result[4]
        except Exception as e:
            return str(e)
        finally:
            cur.close()
        #####################
        # messages = [
        #     {
        #     'time':'today',
        #     'content':'good',
        #     'username':'User1'
        #     },
        #     {
        #     'time':'yesterday',
        #     'content':'bad',
        #     'username':'User2'
        #     }
        # ]
        messages = []
        cur = engine.cursor()
        try:
            cur.execute("SELECT L.time, L.content, U.screen_name "
                        "FROM Users U, leave_message L "
                        "WHERE L.uid = U.uid AND L.cid = %s", (cid, ))
            for result in cur:
                message = {
                    'time': '',
                    'content': '',
                    'username': ''
                }
                message['time'] = result[0]
                message['content'] = ''.join(list(result[1])).rstrip()
                message['username'] = ''.join(list(result[2])).rstrip()
                messages.append(message)
        except Exception as e:
            return str(e)
        finally:
            cur.close()
        ########################
        rates = []
        cur = engine.cursor()
        try:
            cur.execute("SELECT R.content, R.score, U.screen_name "
                        "FROM Users U, Rated_by R "
                        "WHERE R.uid = U.uid AND R.cid = %s", (cid, ))
            for result in cur:
                rate = {
                    'content': '',
                    'score': '',
                    'username': ''
                }
                # rate['content'] = ''.join(list(result[0])).rstrip()
                rate['content'] = result[0]
                rate['score'] = result[1]
                # rate['username'] = ''.join(list(result[2])).rstrip()
                rate['username'] = result[2]
                rates.append(rate)
        except Exception as e:
            return str(e)
        finally:
            cur.close()
        info = {
            'basicInfo': basicInfo,
            'messages': messages,
            'rates': rates
        }
        return info

    info = getItemInfo(cid)
    return render_template('cid.html', data=info)


@app.route('/send', methods=['GET'])
def send():
    args = request.args
    if 'method' not in args:
        return redirect('/error')
    method = args['method']

    if method == 'comment':
        cid = args['cid']
        uid = args['uid']
        content = args['content']
        # TODO given cid, uid, content, leave comment in database
        time = random.randint(0, 23)
        cur = engine.cursor()

        try:
            cur.execute("select uid, cid from Leave_message")
            sign = 0
            for i in cur:
                if uid == ''.join(list(i[0])).rstrip() and cid == ''.join(list(i[1])).rstrip():
                    sign = 1
            if sign == 0:
                cur.execute("INSERT INTO Leave_message VALUES (%s, %s, %s, %s)", (uid, cid, time, content))
            if sign == 1:
                cur.execute("update leave_message set time = %s, content = %s "
                            "where cid = %s and uid = %s ", (time, content, cid, uid))

        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()
        return args

    if method == 'cart':
        cid = str(args['cid'])
        uid = str(args['uid'])
        num = int(args['num'])
        # TODO given cid, uid, num, add product to cart in database

        try:
            cur = engine.cursor()
            sign = 0
            cur.execute("select cid, uid from contains_1")
            for i in cur:
                if cid == ''.join(list(i[0])).rstrip() and uid == ''.join(list(i[1])).rstrip():
                    sign = 1
            if sign == 1:
                cur.execute("update contains_1 set number = number + %s where uid = %s and cid =%s", (num, uid, cid))
            if sign == 0:
                cur.execute("INSERT INTO contains_1 VALUES (%s, %s, %s)", (uid, cid, num))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()
        return args

    if method == 'username':
        uid = args['uid']
        username = args['username']
        # TODO given uid, username, change username
        cur = engine.cursor()
        try:
            cur.execute("UPDATE Users SET screen_name = %s WHERE uid = %s", (username, uid))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()
        return args

    if method == 'address':
        uid = args['uid']
        address = args['address']
        # TODO given uid, address, change address
        cur = engine.cursor()
        try:
            cur.execute("UPDATE Users SET address = %s WHERE uid = %s", (address, uid))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()
        return args

    if method == 'checkout':
        oid = random.randint(2300, 1000000)

        def valid(id):
            cur = engine.cursor()
            cur.execute("SELECT oid FROM Sent_by")
            for result in cur:
                if id == int(''.join(list(result[0])).rstrip()):
                    return False
            cur.close()
            return True
        while not valid(oid):
            oid = random.randint(2020, 3000)

        uid = args['uid']
        # TODO given uid, checkout
        cids = []
        numbers = []
        costs = []

        # allCids = {}
        # # find all cids
        # c = engine.cursor()
        # c.execute("select cid, stock from commodities")
        # for i in c:
        #     allCids[''.join(list(i[0])).rstrip()] = i[1]
        # c.close()
        cur = engine.cursor()
        try:
            cur.execute("SELECT C.cid, C.number, Com.cost FROM contains_1 C, Commodities Com "
                        "WHERE C.uid = %s AND Com.cid = C.cid", (uid, ))

            for result in cur:
                cid = ''.join(list(result[0])).rstrip()
                # if allCids[cid] >= result[1]:
                # newStock = allCids[cid] - result[1]
                cids.append(cid)  # can also be accessed using result[0]
                numbers.append(int(result[1]))
                costs.append(int(result[2]))
            for i in range(len(numbers)):
                cur.execute("update commodities set stock = stock - %s where cid = %s", (numbers[i], cids[i]))
        except Exception as e:
            return str(e)
        finally:
            cur.close()
        #  mailing fee
        fee = random.randint(1, 20)
        totalcost = fee
        for i in range(len(numbers)):
            totalcost = totalcost + numbers[i] * costs[i]
        # insert the info into orders
        import time
        localtime = time.asctime(time.localtime(time.time()))
        cur = engine.cursor()
        try:
            cur.execute("INSERT INTO Orders VALUES (%s, %s, %s, %s) ", (oid, uid, localtime, totalcost))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        # insert into contains_2
        cur = engine.cursor()
        try:
            for i in range(len(numbers)):
                cur.execute("INSERT INTO Contains_2 VALUES (%s, %s, %s)", (oid, cids[i], numbers[i]))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        # insert into Sent_by
        cur = engine.cursor()
        try:
            eid = random.randint(3, 9)
            cur.execute("INSERT INTO Sent_by VALUES (%s, %s, %s)", (oid, eid, fee))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        # delete from contains_1
        cur = engine.cursor()
        try:
            cur.execute("DELETE FROM contains_1 WHERE uid = %s", (uid, ))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        return args

    if method == 'rate':
        uid = args['uid']
        oid = args['oid']
        cid = args['cid']
        rate = int(args['rate'])
        content = args['content']
        # TODO given uid,oid,cid,rate,content, add rating and content to database
        cur = engine.cursor()
        try:
            cur.execute("select uid, cid, oid from Rated_by")
            sign = 0
            for i in cur:
                if uid == ''.join(list(i[0])).rstrip() and cid == ''.join(list(i[1])).rstrip() \
                        and oid == ''.join(list(i[2])).rstrip():
                    sign = 1
            if sign == 0:
                cur.execute("INSERT INTO Rated_by VALUES(%s, %s, %s, %s, %s)", (oid, cid, uid, rate, content))
            if sign == 1:
                cur.execute("update Rated_by set score = %s, content = %s"
                            " where uid = %s and cid = %s and oid = %s", (rate, content, uid, cid, oid))
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        return args
    return 'None'


@app.route('/user', methods=['GET'])
def user():
    args = request.args
    if 'uid' not in args:
        return redirect('/error')
    uid = args['uid']

    def getUserInfo(uid):
        # TODO given uid, return user info
        cur = engine.cursor()
        basicInfo = {
            'uid': '',
            'username': '',
            'address': ''
        }
        try:
            cur.execute("SELECT screen_name, address FROM Users WHERE uid = %s", (uid,))
            result = cur.fetchone()
            username = ''.join(list(result[0])).rstrip()
            address = ''.join(list(result[1])).rstrip()
            basicInfo['uid'] = uid
            basicInfo['username'] = username
            basicInfo['address'] = address
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()

        #######################################################

        cur = engine.cursor()
        carts = []
        try:
            cur.execute("SELECT Com.name, Con.number, Com.cid, Com.cost FROM Users U, Contains_1 Con, Commodities Com  "
                        "WHERE Com.cid = Con.cid AND U.uid = Con.uid AND U.uid = %s", (uid,))
            for result in cur:
                cart = {
                    'name': 'apple',
                    'number': '2',
                    'cid': '001',
                    'cost': '$20'
                }
                cart['name'] = ''.join(list(result[0])).rstrip()
                cart['number'] = result[1]
                cart['cid'] = ''.join(list(result[2])).rstrip()
                cart['cost'] = result[3]
                carts.append(cart)
        except Exception as e:
            return str(e)
        finally:
            engine.commit()
            cur.close()
        ###############################################################

        purchased = []
        cur = engine.cursor()
        try:
            cur.execute("SELECT O.oid, O.total_cost, E.company_name, S.fee"
                        " FROM Users U, Orders O, ExpressCompanies E, Sent_by S  "
                        "WHERE U.uid = O.uid AND S.oid = O.oid AND S.eid = E.eid AND U.uid = %s", (uid,))
            for result in cur:
                order = {
                    'order_id': '',
                    'total_cost': '',
                    'expComp': '',
                    'expFee': '',
                    'items': []
                }
                order['order_id'] = ''.join(list(result[0])).rstrip()
                order['total_cost'] = result[1]
                order['expComp'] = ''.join(list(result[2])).rstrip()
                order['expFee'] = result[3]
                purchased.append(order)
        except Exception as e:
            return str(e)
        finally:
            cur.close()

        for i in range(len(purchased)):
            items = []
            cur = engine.cursor()
            try:
                id = purchased[i]['order_id']
                cur.execute("SELECT Com.name, Con.number, Com.cid, Com.cost"
                            " FROM Users U, Contains_2 Con, Commodities Com, Orders O  "
                            "WHERE Com.cid = Con.cid AND U.uid = O.uid AND O.oid = Con.oid "
                            "AND O.oid = %s AND U.uid = %s", (id, uid))
                for result in cur:
                    item = {
                        'name': '',
                        'number': '',
                        'cid': '',
                        'cost': ''
                    }
                    c_name = ''.join(list(result[0])).rstrip()
                    c_number = result[1]
                    c_cid = ''.join(list(result[2])).rstrip()
                    c_cost = result[3]
                    item['name'] = c_name
                    item['number'] = c_number
                    item['cid'] = c_cid
                    item['cost'] = c_cost
                    items.append(item)
            except Exception as e:
                return str(e)
            finally:
                cur.close()
            purchased[i]['items'] = items

        Data = {
            'basicInfo': basicInfo,
            'cart': carts,
            'purchased': purchased
        }
        return Data
        pass

    data = getUserInfo(uid)
    return render_template('user.html', data=data)


@app.route('/error', methods=['GET'])
def error():
    return 'ERROR'

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=5000, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    #print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

# app.run()


