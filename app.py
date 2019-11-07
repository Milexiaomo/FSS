from  flask  import Flask,render_template
from  stock.views import stock
from  sell.views import sell
from  Tool.tool_db  import DB
app=Flask(__name__)
app.debug=True
app.register_blueprint(stock,url_prefix="/stock")
app.register_blueprint(sell,url_prefix="/sell")

#测算总金额和收入额
def  sumDollars(values):
    products=[]
    for  product  in values:
        product = list(product)
        product.insert(6, round(float(product[3]) * float(product[5]),2))
        product.insert(9, round(float(product[7]) * float(product[8]),2))
        products.append(tuple(product))
    return products

@app.route("/")
def  index():
    sql="""SELECT ROWID,productName,productCategory,productNumber,productStandard,
      productPrice,productSaleNumber,productProfit,inputTime from product_list;"""
    products=DB.query_sql(sql)
    products=sumDollars(products)
    return  render_template("product_list.html",products=products)



if  __name__=="__main__":
    app.run()