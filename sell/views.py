from  flask import Blueprint,render_template,request,redirect,url_for
from Tool.tool_db import DB
from datetime import datetime
sell=Blueprint("sell",__name__)

#在库周期
def time_cycle(values):
    pastDate=datetime.strptime(values,"%Y-%m-%d")
    nowDate=datetime.today()
    timeCycle=(nowDate-pastDate).days
    return timeCycle
#计算在库商品数量
def  in_stock_number(values):
    sells=[]
    for  sell in values:
        sell=list(sell)
        sell.insert(5,int(sell[3]-sell[4]))
        sell.insert(7,"{}天".format(time_cycle(sell[6])))
        sells.append(sell)
    return sells

@sell.route("/sell_list/")
def sellList():
    sql="""select rowid,productName,productStandard,productNumber,productSaleNumber,
        inputTime,productCategory from product_list where productNumber-productSaleNumber != 0;"""
    sells=DB.query_sql(sql)
    sells=in_stock_number(sells)
    return  render_template("sell_list.html",sells=sells)

@sell.route("/sell_information/<id>,<number>")
def sellInformation(id,number):
    sql="select productName,productCategory,productStandard,productProfit,rowid from product_list where rowid=?;"
    datas=DB.query_sql(sql,(id,),single_strip=True)
    datas=datas+(number,)
    return  render_template("sell_product_information.html",datas=datas)
    #return "{}".format(datas)

@sell.route("/sell_data/",methods=['POST'])
def sellData():
    """
        修改产品售卖数量信息
    """
    if request.method=='POST':
        rowid=request.form["product_id"]
        productName=request.form["product_name"]
        sellNumber=request.form["sell_number"]
        productCategory=request.form["product_category"]
        productProfit=request.form["product_price"]
        operator="system"
        operatorTime=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        sql3="insert  into product_history(productName, productCategory, productSaleNumber, productProfit, operator, operatorTime) values (?,?,?,?,?,?)"
        DB.execute_sql(sql3,(productName, productCategory, int(sellNumber), productProfit, operator, operatorTime))
        sql="select productSaleNumber from product_list where rowid=?"
        productSaleNumber=DB.query_sql(sql,(rowid,),single_strip=True)
        productSaleNumber=int(productSaleNumber[0])+int(sellNumber)
        sql2="update product_list set productSaleNumber=?  where rowid=?;"
        DB.execute_sql(sql2,(productSaleNumber,rowid))
        return redirect(url_for("sell.sellList"))


@sell.route("/sell_list_history/")
def  sellListHistory():
    sql="select rowid,productName,productCategory,productSaleNumber,productProfit,operator,operatorTime from product_history order by operatorTime desc ;"
    datas=DB.query_sql(sql)
    return render_template("sell_list_history.html",datas=datas)