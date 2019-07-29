# =====================================================================
# Summary:
# =====================================================================
"""    
    El modulo 'mt_sqlite.py' contiene clases para acceder \
    a la base de datos sqlite, para realizar operaciones (CRUD).
    
    Sobre la BD:
        Soporta (DML) -> select, insert, delete, update. \
        Soporta (DDL) -> create, alter, drop. \
        Soporta ejecutar script. \
    Ademas contiene funciones para conversion a CSV, JSON, DICT.
    
    Utiliza las librerias:
        'pymysql'
        'json'

        

"""
# =====================================================================
# STANDARD FIELDS
# =====================================================================
__author__     = "Mariano Trigila"
__copyright__  = "Copyright 2019, The MT Project"
__credits__    = ["Mariano Trigila",""]
__license__    = "GPL"
__version__    = "1"
__maintainer__ = "Mariano Trigila"
__email__      = "marianotrigila@gmail.com"
__status__     = "Production"

# =====================================================================
# CUSTOM FIELDS
# =====================================================================
__date__ = '2019/07/26'
__description__ = 'Clases y funciones para administrar base de datos sqlite.'

# =====================================================================
# RESOURCES AND BIBLIOGRAPHY
# =====================================================================

    # RESOURCES
    
    
    # BIBLIOGRAPHY

# =====================================================================
# LIBRARIES
# =====================================================================
import sqlite3
from json import loads
from json import dumps

# =====================================================================
# GLOBALS - CONSTANTS
# =====================================================================


# =====================================================================
# CODE
# =====================================================================

class DBSqlite:
  
    """
    Examples:
        Intancia de la clase. Se le pasa por parámetro el nombre de la  \
        base de datos. Si no existe, entonces la crea y conecta; y si existe \
        entonces conecta. Se asigna en db el objeto conección.
        
        >>> from mt_sqlite import *     # import la librería
        >>> DBName  = "example.db"      # Nombre de la base de datos
        >>> db = DBSqlite(DBName)       # Instancia de la clase
        >>> 
        
    """  
    connDB=None
    """
        connDB(obj): contiene el objeto conección a la base de datos. \
                     Su valor por defecto connDB=None.
    """
    error=None
    """
        error(obj): contiene el objeto error. Su valor por defecto error=None.
    """

    def __init__(self, DBName):
        try:                               
            self.DBName = DBName           
            self.connDB = self.openConnDB()     # Conecta a la BD.
            
        except sqlite3.Error as err:
            self.error=err
            #raise
        finally:
            self.closeConnDB()                  # Cerrar conexion a BD. 
       
    def closeConnDB(self):
        """
            Cierra la conección a la base de datos.
        """
        try:
            if self.connDB!=None:
                self.connDB.close()
            
        except sqlite3.Error as err:            
            del (self.connDB)
            self.error = err
            raise
        finally:
            self.connDB=None
            
    def openConnDB(self):
        """
        Conecta a una base de datos y retorna el objeto de conección.
        Si no existe BD => la crea y conecta.
        Si existe       => conecta.
                        
        Returns:
            (obj) : Retorna el objeto coneccion a la base de datos, \
                    si la coneccion es exitosa.
            (None): Retorna None si la coneccion NO es exitosa.
        """
        try:
            conn = sqlite3.connect(self.DBName)
            self.error=None
        except sqlite3.Error as err:
            conn=None
            self.error = err
            raise
        return conn

    def execQuery(self,sql,cab=False):
        
        """
        Ejecuta una consulta SELECT y retorna el contenido de la \
        respuesta a la consulta.
          
        Args:
            sql(str): String que contiene la consulta sql a ejecutar.            
            cab(bool): Si cab=True, indica que la consulta trae la
                        cabecera (es decir los nombres de las columnas).
                
        Return:
            res([(tuple)]): Retorna un lista de tuplas con el contenido \
                            de la respuesta de la consulta. Para cab=True, \
                            incluye el contenido del nombre de las columnas \
                            en la primer tupla.
        Return:
            res(int): Retorna -1 si hay error.
        
        Examples:
            
            >>> from mt_sqlite import *            # import la librería
            >>> DBName  = 'example.db'             # Nombre de la base de datos
            >>> db = DBSqlite(DBName)              # Instancia de la clase
            >>> sql = 'SELECT * FROM address'      # String con la consulta
            >>> res = db.execQuery(sql, cab=True)  # Ejecutar la consulta
            >>> print(res,'\\n', db.error)          # Imprime el resultado de la consulta y el error
            [('id', 'street_name', 'street_number', 'post_code', 'person_id'), 
            (1, 'python road', '1', '00000', 1), (2, 'blblblbl', '1', '2222', 2), 
            (6, 'pythoncentrallllll', '11', '1221', 14), (12, 'blblblbl', '1', '2222', 2), 
            (22, 'blblblbl', '1', '2222', 2)] 
            None
            >>>
        """        
        try:
            results=-1
            self.connDB = self.openConnDB() # Conecta a la BD.
            if self.connDB!=None: 
                cursor = self.connDB.cursor()   # preparar un objeto cursor utilizando el método cursor()
                
                cursor.execute(sql)             # ejecutar consulta
                
                results = cursor.fetchall()     # retorna una lista de tuplas con el contenido de la consulta
                
                # - - - - - Armado de cabecera - - - - - #
                if cab:
                    tupDesc=tuple(cursor.description)    # Tupla con las descripciones de la tabla
                    cabecera=[]
                    for x in tupDesc:
                        cabecera.append(x[0])
                    results.insert(0,tuple(cabecera))
                # - - - - - - - - - -  - - - - - - - - - #
                
        except sqlite3.Error as err:
            results = -1
            self.error = err
            #raise
        finally:            
            self.closeConnDB()                  # Cerrar conexion a BD.
        return results

    def transQuery(self,sql):
        """          
        Ejecuta una consulta INSERT, UPDATE, DELETE, CREATE,DROP.
        Retorna la informacion sobre el estado de la accion, es decir
        sobre la cantidad de registros afectados.
            
        Args:
            sql(str): String con la consulta sql a ejecutar.
                
        Return:        
            res(int): Retorna un entero n > 0 si ha ejecutado efectivamente \
                      sobre n registros el INSERT o el UPDATE o el DELETE.
        
        Return:
            res(int): Retorna *0* si se realizó con exito el CREATE o \
                      el DROP o el etc.
        
        Return:
            res(int): Retorna *-1* si hubo algún error.
            
        Examples:
            Un ejemplo con un DELETE. Retorna la cnatidad de filas afectadas. \
            La ejecución se realiza dentro de una transacción.
        
            >>> from mt_sqlite import *                  # import la librería
            >>> DBName  = "example.db"                   # Nombre de la base de datos
            >>> db = DBSqlite(DBName)                    # Instancia de la clase
            >>> sql = "DELETE from address where id =22" # String con la consulta
            >>> res = db.transQuery(sql)                 # Ejecutar consulta (Transaccion)
            >>> print(res,"\\n", "Error: ",db.error)      # imprimir resultado y error            
            1 
            Error:  None
            >>> 
        """
        
        try:
            res=-1
            self.connDB = self.openConnDB()     # Conecta a la BD.
            if self.connDB!=None: 
                cursor = self.connDB.cursor()
                result = cursor.execute(sql)    # Ejecuta sql, retorna la cantidad de inserciones, actualizaciones o borrados realizados  
                self.connDB.commit()            # Commit para hacer efectivos los cambios en la base de datos
                res=result.rowcount             # Se deja en res la cantidad de filas afectadas, ya que result es un cursor
                if res==-1:                     #create , drop retorna -1 con el rowcount
                    res=0                       # se coloca en 0 indicando que se efectuo correctamente 
                self.error=None
        except sqlite3.Error as err:
            if self.connDB!=None:
                self.connDB.rollback()          # Rollback en caso de algún error
            res=-1
            self.error = err
            #raise
        finally:
            self.closeConnDB()                  # Cerrar conexion a BD.
            
        return res
    
    def schema(self):
        """
         Retorna una secuencia de tuplas, donde por cada tabla se \
         muestra el sql necesario \
         para crear dicha tabla, incluyendo indice, claves.
         
         Examples:
             Se imprime el schema de la base de datos conectada. \
             Imprime None, si no hubo error.
             
            >>> from mt_sqlite import *             # import la librería
            >>> DBName  = 'example.db'              # Nombre de la base de datos
            >>> db = DBSqlite(DBName)               # Instancia de la clase
            >>> print(db.schema(),'\\n', db.error)  # Obtener el schema de la base de datos
                                                    # Imprime schema e imprime error
            [('address', 'CREATE TABLE address (id INTEGER PRIMARY KEY ASC, street_name varchar(250), 
            street_number varchar(250), post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL, 
            FOREIGN KEY(person_id) REFERENCES person(id))'), ('person', 'CREATE TABLE person 
            (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)')] 
            None
            >>>
    
        """
        #            [('address', 'CREATE TABLE address (id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250), post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL, FOREIGN KEY(person_id) REFERENCES person(id))'), ('person', 'CREATE TABLE person (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)')] 
  
        sql = "select tbl_name, sql from sqlite_master ;"
        return self.execQuery(sql);
        
    def execScript(self, strScript):
        """
        Ejecuta un sript en la base de datos.
        
        Args:
            strScript(str): String que contiene el script a ejecutar.
            

        """
        
        try:
           
            self.connDB = self.openConnDB()         # Conecta a la BD.
            
            if self.connDB!=None:
                cursor = self.connDB.cursor()       # preparar un objeto cursor utilizando el método cursor()                               
                cursor.executescript(strScript)     # ejecutar script

                self.error=None
        except sqlite3.Error as err:
            self.error=err
            #raise
        finally:            
            self.closeConnDB()                      # Cerrar conexion a BD.
           
    
    def execScriptFromFile(self,fileName):
        """
        Ejecuta un sript en la base de datos, desde un archivo.
        
        Args:
            fileName(str): String que contiene en nombre del archivo \
                           a ejecutar.
            
        Examples:
            Se ejecuta el script 'example_script.sql' que contiene la secuencia \
            sql para crear las tablas, agregarle las claves, insertar datos.
            La ejecución del script se hace sobre la base de datos conectada.
            execScriptFromFile dejará en error, la información del error ocurrido, \
            que para el caso en None, por no haber error.
            
            >>> from mt_sqlite import *           # import la librería
            >>> DBName  = "example.db"            # Nombre de la base de datos
            >>> db = DBSqlite(DBName)             # Instancia de la clase
            >>> db.execScriptFromFile("example_script.sql")  # Ejecutar script
            >>> print(db.error)                   # Imprimir error
            None
            >>> 

        """
        try:
            fileScript = open(fileName,"r")
            strScript=""
        
            for linea in fileScript:
                strScript += linea
                
            self.execScript(strScript)
            self.error=None
        except sqlite3.Error as err:
            self.error = err
            #raise
        except IOError as err:
            self.error = err
            #raise 
        finally:
            try:
                fileScript.close()
            except:
                pass

    def insertFromCSV(self,tableName,fileName, cab=False):
        """
        Ejecuta un sript en la base de datos, desde un archivo.
        
        Args:
            tableName(str): String que contiene el nombre de la tabla donde \
                            se ejecutaran los instert que se encuentran en fileName.
            fileName(str): String que contiene en nombre del archivo a ejecutar.
            cab(bool): Booleana que indica en True si el csv contiene los nombre \
                       de las columnas. 
        Examples:
            En el archvio csv se encuentra la informacion de los valores de cada registro \
            separado por coma. insertFromCSV toma los valores y los convierte en un secuencia sql. \
            El primer parametro 'person' indica el nombre de la tabla donde se harán los insert. \
            Si hay error, se indicará en la variable error.
            
            >>> from mt_sqlite import *           # import la librería
            >>> DBName  = "example.db"            # Nombre de la base de datos
            >>> db = DBSqlite(DBName)             # Instancia de la clase
            >>> db.insertFromCSV("person","tabla.csv", cab = True) # Ejecutar INSERT desde csv
            >>> print(db.error)                   # Imprime error
            None
            >>> 
        """
        
        def formatLinea(lst):
            """
            Da el formato a la linea
            """
            
            def adaptadorCampo(campo):
                """
                Adapta el campo al proveedor de base de datos
                """
                res=""
                if campo=="" or "null" in campo.lower():       # vacio o nulo (null)
                    res += "NULL"
                elif campo.isnumeric() or isFloat(campo):      # integer, real
                    res += lst[i]
                elif campo[0:2]=="x'" or campo[0:2]=="X'":     # blob               
                    res += lst[i]                   
                else: 
                    res += "'" + campo + "'"                   # cualquier otro... ej: text
                return res
            
            def isFloat(str):
                """
                Retorna True si str representa un Flot, False caso contrario.
                """
                try:
                    float(str)
                    return True
                except ValueError:
                    return False
                
            linea=""
            i=0
            if len(lst)!=0:
                while i<len(lst)-1:                
                    linea += adaptadorCampo(lst[i])
                    linea +=","
                    i+=1
                    
                if linea == "":
                    linea = adaptadorCampo(lst[i])
                else:
                    linea += adaptadorCampo(lst[i])            
            return linea
        
        if cab:            
            tempIns = "INSERT INTO " + tableName +" ({}) VALUES({});\n"
        else:
            tempIns = "INSERT INTO " + tableName +" VALUES({});\n"
            
        try:
            fileCSV = open(fileName,"r")
            strScript=""
            if cab:
                strCab = fileCSV.readline()
                strCab = strCab[:-1]
                
            for linea in fileCSV:
                strValues=""
                lstLineas=[]
                tieneBarraN = linea[-1]=="\n"                    #True si tiene un \n al final de la linea
                lineaVacia  = len(linea)==1 and linea[-1]=="\n"  #True si la linea solo tiene un '\n'
                if not(lineaVacia) and tieneBarraN:              
                    lstLineas = linea[:-1].split(",")            # tiene \n
                elif not(lineaVacia) and not(tieneBarraN):
                    lstLineas = linea.split(",")                 # no tiene \n
                if not(lineaVacia):
                    strValues = formatLinea(lstLineas)
                    if cab:
                        strScript += tempIns.format(strCab,strValues)
                    else:
                        strScript += tempIns.format(strValues)

            self.execScript(strScript)
            #print(strScript)
            self.error=None
        except sqlite3.Error as err:
            self.error = err
            #raise
        except IOError as err:
            self.error = err
            #raise   
        finally:
            try:
                fileCSV.close()
            except:
                pass
    
def toCSVstr(lst, sep=','):
    """
    Retorna un string con formato CSV, con el contenido la lista lst.
    
    Args:
            lst(list): Lista de tuplas que proviene de una consulta.
            sep(str) : String que contiene el separador a aplicar entre campos.
                       
                       Note: El valor por defecto sep = ',' .
                       
    Examples:
    
        >>> from mt_sqlite import *              # import la librería
        >>> DBName  = "example.db"               # Nombre de la base de datos
        >>> db = DBSqlite(DBName)                # Instancia de la clase
        >>> sql = 'SELECT * FROM address'        # String con la consulta
        >>> res = db.execQuery(sql, cab=True)    # Ejecutar la consulta
        >>> print(toCSVstr(res))                 # Convierte el resultado de la consulta a un sgring CSV
        id,street_name,street_number,post_code,person_id
        1,python road,1,00000,1
        2,blblblbl,1,2222,2
        6,pythoncentrallllll,11,1221,14
        12,blblblbl,1,2222,2
        22,blblblbl,1,2222,2
        >>>
    """
    strData=""
    for linea in lst:
        strLinea=""
        for item in linea:
            strLinea+=(str(item)+sep)
        strLinea = strLinea[:-1] + "\n"
        strData+= strLinea
    return strData 

    
def toDictPy(lst,strNomObjeto = 'NomObj'):

    """
    Retorna un dictionario, con el contenido la lista de tuplas 'lst' .
    La tupla 0 (primero) contiene los nombres de las columnas.
    
    Args:
        lst(list): Lista de tuplas que proviene de una consulta.
        strNomObjeto (str): String que contiene el nombre del objeto json a crear.
                            El valor por defecto strNomObjeto = 'NomObj'.
                            
    Examples:
    
        >>> from mt_sqlite import *                    # import la librería
        >>> DBName  = "example.db"                     # Nombre de la base de datos
        >>> db = DBSqlite(DBName)                      # Instancia de la clase    
        >>> miTabla = "person"                         # string con el nombre de la tabla
        >>> sql = 'SELECT * FROM {}'.format(miTabla)   # string con la consulta
        >>> res = db.execQuery(sql, cab=True)          # Ejecutar consulta
        >>> dicData = toDictPy(res,miTabla)            # Convertir Lista de tuplas de consulta, a dict python
        >>> print(type(dicData),"\\n",dicData,"\\n")     # Imprimir tipo, y diccionario
        <class 'dict'> 
         {'person': [{'id': 1, 'name': 'pythoncentral'}]}
        >>> 
            
    """

    lstCab = []
    lstDatos = []
    dicResult = {}
    lstResult = []
    if len(lst)>0:
        lstCab = lst[0]
        lstDatos = lst[1:]
    
    for linea in lstDatos:
        dicLinea={}
        i=0
        for dato in linea:
            dicLinea[lstCab[i]] = dato
            i+=1
        lstResult.append(dicLinea)
    dicResult[strNomObjeto]=lstResult    
    return dicResult

def toJsonDecode(strData):
    """
    Retorna un diccionario (Python) con el contenido json pasado por parametro.
    
    Args:
        strData(str): Recibe un "string" con contenido en formato json.
        
    Examples:
    
        >>> from mt_sqlite import *                    # import la librería
        >>> DBName  = "example.db"                     # Nombre de la base de datos
        >>> db = DBSqlite(DBName)                      # Instancia de la clase    
        >>> miTabla = "person"                         # string con el nombre de la tabla
        >>> sql = 'SELECT * FROM {}'.format(miTabla)   # string con la consulta
        >>> res = db.execQuery(sql, cab=True)          # Ejecutar consulta
        >>> dicData = toDictPy(res,miTabla)            # Convertir Lista de tuplas de consulta, a dict python
        >>> strJsonData = toJsonEncode(dicData)        # Convertir Dict a str con formato json
        >>> print(type(strJsonData),"\\n",strJsonData,"\\n") # Imprimir tipo, y str con formato json
        <class 'str'> 
         {"person": [{"id": 1, "name": "pythoncentral"}]} 
        >>>
                    
    References:
        Comprobar json en: http://json2table.com/
            
    """
    decoded = loads(strData)
    return decoded

def toJsonEncode(dicData):
    # https://docs.python.org/3/library/json.html
    # http://www.convertcsv.com/csv-to-json.htm
    # http://json2table.com
    """
    Retorna un "string" con el contenido de dicData en formato json
    
    Args:
        dicData(Dict): Recibe un diccionario (Python) con un elemento que contiene
                        una lista, donde cada elemento de la lista es un diccionario
                        cuyas claves son las columnas, y sus valores son
                        "los valores" de cada campo.
    
    Examples:
    
        >>> from mt_sqlite import *                    # import la librería
        >>> DBName  = "example.db"                     # Nombre de la base de datos
        >>> db = DBSqlite(DBName)                      # Instancia de la clase    
        >>> miTabla = "person"                         # string con el nombre de la tabla
        >>> sql = 'SELECT * FROM {}'.format(miTabla)   # string con la consulta
        >>> res = db.execQuery(sql, cab=True)          # Ejecutar consulta
        >>> dicData = toDictPy(res,miTabla)            # Convertir Lista de tuplas de consulta, a dict python
        >>> strJsonData = toJsonEncode(dicData)        # Convertir Dict a str con formato json
        >>> dicJsonData= toJsonDecode(strJsonData)     # Convertir str con formato json a Dict
        >>> print(type(dicJsonData),"\\n",dicJsonData,"\\n") # Imprimir tipo, y diccionario
        <class 'dict'> 
         {'person': [{'id': 1, 'name': 'pythoncentral'}]} 
        >>>
        
                
    References:
        Comprobar json en: http://json2table.com/
       
        
    """  
   
    encoded = dumps(dicData)
    return encoded


    