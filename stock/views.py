from  flask  import Blueprint,render_template,request,redirect,url_for
from Tool.tool_db import DB
from datetime import datetime
stock=Blueprint("stock",__name__)

@stock.route("/new_stock/")
def  newStock():
    return render_template("entry.html")

@stock.route("/post_product/",methods=['POST'])
def post_product():
    if  request.method=="POST":
            productName=request.form.get('product_name')
            productCategory=request.form.get('product_category')
            productNumber=request.form.get("product_number")
            productStandard=request.form.get('product_standard')
            productPrice=request.form.get('product_price')
            productProfit=request.form.get('product_profit')
            productSaleNumber=0
            inputTime=datetime.today().strftime("%Y-%m-%d")
            sql="insert into product_list(productName,productCategory,productNumber,productStandard,productPrice,productSaleNumber,productProfit,inputTime) values(?,?,?,?,?,?,?,?);"
            DB.execute_sql(sql,(productName,productCategory,productNumber,productStandard,productPrice,productSaleNumber,productProfit,inputTime))
            return  redirect(url_for("index"))