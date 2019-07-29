#https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
#from mt_sqlite import *     # import la librería

## INSTANCIA ------------------------------------------------------
#from mt_sqlite import *     # import la librería
#DBName  = "example.db"      # Nombre de la base de datos
#db = DBSqlite(DBName)       # Instancia de la clase
##  ---------------------------------------------------------------


### EJECUTAR SCRIPT ------------------------------------------------
#from mt_sqlite import *           # import la librería
#DBName  = "example.db"            # Nombre de la base de datos
#db = DBSqlite(DBName)             # Instancia de la clase
#db.execScriptFromFile("example_script.sql")  # Ejecutar script
#print(db.error)                   # Imprimir error
###  -----------------------------------------------------------------

### OBTENER SCHEMA ---------------------------------------------------
#from mt_sqlite import *           # import la librería
#DBName  = "example.db"            # Nombre de la base de datos
#db = DBSqlite(DBName)             # Instancia de la clase
#print(db.schema(),"\n", db.error) # Obtener el schema de la base de datos
#                                  # Imprime schema e imprime error
### ------------------------------------------------------------------

### INSERT from CSV -------------------------------------------------
#from mt_sqlite import *           # import la librería
#DBName  = "example.db"            # Nombre de la base de datos
#db = DBSqlite(DBName)             # Instancia de la clase
#db.insertFromCSV("person","tabla.csv", cab = True) # Ejecutar INSERT a una tabla desde csv
#print(db.error)                   # Imprime error
### -----------------------------------------------------------------

### EJECUTAR UN SCRIPT-----------------------------------------------
#script="""INSERT INTO person (id,name) VALUES("2",'juan');
#          INSERT INTO person (id,name) VALUES('5',null);
#          INSERT INTO person (id,name) VALUES(7,claudia);
#       """
#db.execScript(script)
### -----------------------------------------------------------------

####  SELECT --------------------------------------------------------
#from mt_sqlite import *            # import la librería
#DBName  = "example.db"             # Nombre de la base de datos
#db = DBSqlite(DBName)              # Instancia de la clase
#sql = 'SELECT * FROM address'      # String con la consulta
#res = db.execQuery(sql, cab=True)  # Ejecutar la consulta
#print(db.schema(),"\n", db.error)  # Imprime el resultado de la consulta y el error
#
#### ----------------------------------------------------------------

####  CONVERTIR A CSV------------------------------------------------
## Convierte a CSV una lista de tuplas que
## contiene el contenido de la tabla
#from mt_sqlite import *              # import la librería
#DBName  = "example.db"               # Nombre de la base de datos
#db = DBSqlite(DBName)                # Instancia de la clase
#sql = 'SELECT * FROM address'        # String con la consulta
#res = db.execQuery(sql, cab=True)    # Ejecutar la consulta
#print(res,"\n", "Error: ",db.error)
#print(toCSVstr(res))                 # Convierte el resultado de la consulta a un sgring CSV
##### ----------------------------------------------------------------

######  CONVERTIR A CSV-----------------------------------------------
### CSV, DICT, JSON
##
#from mt_sqlite import *                    # import la librería
#DBName  = "example.db"                     # Nombre de la base de datos
#db = DBSqlite(DBName)                      # Instancia de la clase
##
#miTabla = "person"                         # string con el nombre de la tabla
#sql = 'SELECT * FROM {}'.format(miTabla)   # string con la consulta
##
##print("--LISTA DE TUPLAS, resultado de una consulta --")
#res = db.execQuery(sql, cab=True)          # Ejecutar consulta
##print(res,"\n", "Error: ",db.error,"\n")
##
##print("--Convertir a CSV desde una lista de tuplas --")
##strCSV = toCSVstr(res)
##print(type(strCSV),"\n",strCSV,"\n")
##
#dicData = toDictPy(res,miTabla)            # Convertir Lista de tuplas de consulta, a dict python
##print("--Convertir a DICCIONARIO desde una lista de tuplas --")
##print(type(dicData),"\n",dicData,"\n")     # Imprimir tipo, y diccionario
##
##print("--Convertir a JSON desde un Diccionario 'Codificacion'--")
#strJsonData = toJsonEncode(dicData)
##print(type(strJsonData),"\n",strJsonData,"\n")
##
##print("-- Convertir a DICCIONARIO desde un json 'Decodificacion'--")
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

#### DELETE -----------------------------
#from mt_sqlite import *                  # import la librería
#DBName  = "example.db"                   # Nombre de la base de datos
#db = DBSqlite(DBName)                    # Instancia de la clase
#sql = "DELETE from address where id =22" # String con la consulta
#res = db.transQuery(sql)                 # Ejecutar consulta (Transaccion)
#print(res,"\n", "Error: ",db.error)      # imprimir resultado y error
#
### -------------------------------------

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



