import os
from sqlite3 import dbapi2

"""
    Genera la base de datos y le introduce unos datos iniciales.
"""
try:
    #Creacion de la base de datos.
    baseDatos = dbapi2.connect("BaseDeDatos.dat")
    cursor = baseDatos.cursor()


    cursor.execute("create table proveedores(id text, Nombre text, CIF text, Direccion text, Telefono text, Email text)")
    cursor.execute("create table productos(id text, NombreProducto text, Stock number, precioUnidad number)")
    cursor.execute("create table clientes(dni text, nombreCliente text, telefono text, direccion text, email text)")
    cursor.execute("create table facturas(idFactura, dni text, NombreProducto text, Cantidad text)")

    #Realizamos Inserts en las tablas

    cursor.execute("insert into proveedores values('0001,'Pepe','682-186-786','Sanjurjo Badia 102','986267455','pepe@gmail.com')")
    cursor.execute("insert into proveedores values('0002','Pedro','415-843-654','Rua da corunha 52','986452175','pedro@gmail.com')")
    cursor.execute("insert into proveedores values('0003','Maria','851-942-961','Travesia de vigo 41','986567441','maria@gmail.com')")

    cursor.execute("insert into productos values ('0001', 'Sanitol', '30', '5')")
    cursor.execute("insert into productos values ('0003', 'Don limpio', '50', '10')")
    cursor.execute("insert into productos values ('0002','Formil', '5', '15')")

    cursor.execute("insert into clientes values('48167529G','Asuncion','678258159','Sanjurjo badia 180','asuncionvigo@gmai.com')")
    cursor.execute("insert into clientes values('71824672P','Gonzalo','667785040','Julian Estevez 23','garciagonzalovigo@gmail.com')")

    cursor.execute("insert into facturas values('1','48167529G', 'Sanitol','2')")
    cursor.execute("insert into facturas values('2','71824672P', 'Don limpio','3')")


    #Realizamos commit en la BD
    baseDatos.commit()


#Creamos una excepcion para los errores y finalmente cerramos la conexion con la base de datos
except (dbapi2.DatabaseError):
    print("Error en la base de datos")
finally:
    print("Cerramos conexion de la base de datos")
    cursor.close()
    baseDatos.close()