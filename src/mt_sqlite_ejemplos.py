#https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
from mt_sqlite_poo import *


# CONFIGURAR NOMBRE DE LA BASE DE DATOS ######
DBName  = "example.db"
##############################################

## INSTANCIA ------------------------------------------------------
db = DBSqlite(DBName)
##  ---------------------------------------------------------------


## EJECUTAR SCRIPT ------------------------------------------------
#db.execScriptFromFile("example_script.sql")
#print(db.error)
##  -----------------------------------------------------------------

## OBTENER SCHEMA ---------------------------------------------------
#print(db.schema(),"\n", db.error)
## ------------------------------------------------------------------

### INSERT from CSV -------------------------------------------------
#db.insertFromCSV("person","tabla.csv", cab = True)
#print(db.error)
### -----------------------------------------------------------------

### EJECUTAR UN SCRIPT-----------------------------------------------
#script="""INSERT INTO person (id,name) VALUES("2",'juan');
#          INSERT INTO person (id,name) VALUES('5',null);
#          INSERT INTO person (id,name) VALUES(7,claudia);
#       """
#db.execScript(script)
### -----------------------------------------------------------------

####  SELECT --------------------------------------------------------
#sql = 'SELECT * FROM address'
#res = db.execQuery(sql, cab=True)
#print(res, db.error)
#### ----------------------------------------------------------------

####  CONVERTIR A CSV------------------------------------------------
## Convierte a CSV una lista de tuplas que
## contiene el contenido de la tabla
#sql = 'SELECT * FROM address'
#res = db.execQuery(sql, cab=True)
#print(res,"\n", "Error: ",db.error)
#print(toCSVstr(res)) 
#### ----------------------------------------------------------------

######  CONVERTIR A CSV-----------------------------------------------
### CSV, DICT, JSON
#
#miTabla = "person"
#sql = 'SELECT * FROM {}'.format(miTabla)
#
#print("--LISTA DE TUPLAS, resultado de una consulta --")
#res = db.execQuery(sql, cab=True)
#print(res,"\n", "Error: ",db.error,"\n")
#
#print("--Convertir a CSV desde una lista de tuplas --")
#strCSV = toCSVstr(res)
#print(type(strCSV),"\n",strCSV,"\n")
#
#dicData = toDictPy(res,miTabla)
#print("--Convertir a DICCIONARIO desde una lista de tuplas --")
#print(type(dicData),"\n",dicData,"\n")
#
#print("--Convertir a JSON desde un Diccionario 'Codificacion'--")
#strJsonData = toJsonEncode(dicData)
#print(type(strJsonData),"\n",strJsonData,"\n")
#
#print("-- Convertir a DICCIONARIO desde un json 'Decodificacion'--")
#dicJsonData= toJsonDecode(strJsonData)
#print(type(dicJsonData),"\n",dicJsonData,"\n")
#
### ------------------------------------------------------------------

## INSERTAR ---------------------------------------------------------
#sql = "INSERT INTO address VALUES(22, 'blblblbl', '1', '2222', 2)"
#res =  db.transQuery(sql)
#print(res, db.error)
## - - - - -

#sql = "INSERT INTO address VALUES(3, 'clacla', '12', '9909', 20)"
#res =  db.transQuery(sql)
#print(res)
## - - - - -

#sql = "INSERT INTO address VALUES(6, 'golll', '11', '1221', 14)"
#res =  db.transQuery(sql)
#print(res)
## -------------------------------------

### DELETE -----------------------------
#sql = "DELETE from address where id =22"
#res = db.transQuery(sql)
#print(res)
## -------------------------------------

#### UPDATE ----------------------------
#sql="UPDATE address SET street_name='pythoncentrallllll' WHERE id='6'"
#res = db.transQuery(sql)
#print(res)
####  ----------------------------------

## DROP --------------------------------
#res = transQuery(db,strDropT1)
#print(res)

#res = transQuery(db,strDropT2)
#print(res)
##  ------------------------------------

## DROP --------------------------------
#strDropT1   = "DROP TABLE person"
##strDropT2   = "DROP TABLE address"
#res = transQuery(db,strDropT1)
#print(res)
##  ------------------------------------

## CREATE-------------------------------
#strCreateT1   = "CREATE TABLE address"
##strCreateT2   = "CREATE TABLE person"
#res = transQuery(db,strCreateT1)
#print(res)
##  ------------------------------------



