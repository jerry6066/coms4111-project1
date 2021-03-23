from flask import Flask
import os
from flask import Flask, request, render_template, g, redirect, Response
from markupsafe import escape

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)




@app.route('/', methods=['GET'])
def index():
    return redirect('/prod')


@app.route('/helperuser',methods=['GET'])
def helperuser():
    data = [{
        'uid':'user001',
        'username':'username001',
        'address':'My address'
    },
    {
        'uid':'user002',
        'username':'username002',
        'address':'My address02'
    }]
    # TODO get all user info
    return render_template('helperuser.html',data=data)

@app.route('/helperprod',methods=['GET'])
def helperprod():
    data = [{
        'cid':'0001',
        'name':'apple',
        'stock':'10',
        'cost':'$20'
        },
        {
        'cid':'0002',
        'name':'banana',
        'stock':'20',
        'cost':'$21'
        }]
    # TODO get all product info
    return render_template('helperprod.html',data=data)

@app.route('/prod',methods=['GET'])
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
        page=1
    if 'key' in args:
        key = args['key']
    else:
        key = ""

    # TODO search
    def search(cate, key, page):
        if cate == 'All' and key == "":
            # TODO normal search by page
            pass
        elif cate != 'All' and key == "":
            # TODO search by category and page
            pass
        elif key != "" and cate == 'All':
            # TODO search by keywords and page
            pass
        else:
            # TODO search by keywords and category and page
            pass
        # return products in array

    # TODO get categories
    def get_cate():
        # TODO return categories
        # E.g. return ['All','option1','option2','option3']
        pass

    data = {}
    data['title'] = 'Products Page'
    data['page'] = page
    data['cate'] = cate
    data['key'] = key

    data['categories'] = ['All','option1','option2','option3']
    data['products'] = [
        {
        'cid':'0001',
        'name':'apple',
        'stock':'10',
        'cost':'$20',
        'category':'fruit'
        },
        {
        'cid':'0002',
        'name':'banana',
        'stock':'20',
        'cost':'$21',
        'category':'fruit'
        }]
    
    return render_template('index.html',data=data)


@app.route('/cid',methods=['GET'])
def cid():
    args = request.args
    if 'cid' not in args:
        return redirect('/error')
    cid = args['cid']
    def getItemInfo(cid):
        # TODO given cid, return info
        info = {}
        basicInfo = {
        'cid':'0001',
        'name':'apple',
        'stock':'10',
        'cost':'$20',
        'category':'fruit',
        'avg_score':'4.8'
        }
        messages = [
            {
            'time':'today',
            'content':'good',
            'username':'User1'
            },
            {
            'time':'yesterday',
            'content':'bad',
            'username':'User2'
            }
        ]
        rates = [
            {
                'content':'Good',
                'score':'5',
                'username':'User1'
            }
        ]
        info={
            'basicInfo':basicInfo,
            'messages':messages,
            'rates':rates
        }
        return info
    info = getItemInfo(cid)
    return render_template('cid.html',data=info)

@app.route('/send',methods=['GET'])
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
        return args
    if method == 'cart':
        cid = args['cid']
        uid = args['uid']
        num = args['num']
        # TODO given cid, uid, num, add product to cart in database
        return args
    if method == 'username':
        uid = args['uid']
        username = args['username']
        # TODO given uid, username, change username
        return args
    if method == 'address':
        uid = args['uid']
        address = args['address']
        # TODO given uid, address, change address
        return args
    if method == 'checkout':
        uid = args['uid']
        # TODO given uid, checkout
        return args
    if method == 'rate':
        uid = args['uid']
        oid = args['oid']
        cid = args['cid']
        rate = args['rate']
        content = args['content']
        # TODO given uid,oid,cid,rate,content, add rating to database
        return args
    return 'None'

@app.route('/user',methods=['GET'])
def user():
    args = request.args
    if 'uid' not in args:
        return redirect('/error')
    uid = args['uid']
    def getUserInfo(uid):
        # TODO given uid, return user info
        pass
    data = {}
    basicInfo = {
        'uid':'user001',
        'username':'username001',
        'address':'My address'
    }
    cart = [{
        'name':'apple',
        'number':'2',
        'cid':'001',
        'cost':'$20'
    },{
        'name':'apple',
        'number':'2',
        'cid':'001',
        'cost':'$20'
    }]
    purchased = [
        {
            'order_id':'00001',
            'total_cost':'120',
            'expComp':'USP',
            'expFee':'10',
            'items':[
                {
                'name':'apple',
                'number':'2',
                'cid':'001',
                'cost':'$20'
                },
                {
                'name':'apple',
                'number':'2',
                'cid':'001',
                'cost':'$20'
                }
            ]
        },
        {
            'order_id':'00001',
            'total_cost':'120',
            'expComp':'USP',
            'expFee':'10',
            'items':[
                {
                'name':'apple',
                'number':'2',
                'cid':'001',
                'cost':'$20'
                },
                {
                'name':'apple',
                'number':'2',
                'cid':'001',
                'cost':'$20'
                }
            ]
        }
    ]
    data = {
        'basicInfo':basicInfo,
        'cart':cart,
        'purchased':purchased
    }
    return render_template('user.html',data=data)



@app.route('/error',methods=['GET'])
def error():
    return 'ERROR'

app.run()


