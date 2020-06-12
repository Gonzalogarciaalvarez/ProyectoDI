import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import _sqlite3 as base
conectar = base.connect('BaseDeDatos')
cursor = conectar.cursor()
cursor.execute('CREATE TABLE mitabla( id INT AUTO_INCREMENT PRIMARY KEY, faccion VARCHAR(255), nombre VARCHAR(255), valor INT(10))')
insercion_de_valores = "INSERT INTO mitabla(id,faccion,nombre,valor) VALUES(01,'Alith Anar','Maestros sombrios', 1600)"
cursor.execute(insercion_de_valores)
conectar.commit()

#CREATE TABLE mitabla ( id INT PRIMARY KEY, nombre VARCHAR(20) );
#INSERT INTO mitabla VALUES ( 1, 'Will' );
#INSERT INTO mitabla VALUES ( 2, 'Marry' );
#INSERT INTO mitabla VALUES ( 3, 'Dean' );
#SELECT id, nombre FROM mitabla WHERE id = 1;
#UPDATE mitabla SET nombre = 'Willy' WHERE id = 1;
#SELECT id, nombre FROM mitabla;
#DELETE FROM mitabla WHERE id = 1;

#SELECT se utiliza cuando quieres leer (o seleccionar) tus datos.
#INSERT se utiliza cuando quieres añadir (o insertar) nuevos datos.
#UPDATE se utiliza cuando quieres cambiar (o actualizar) datos existentes.
#DELETE se utiliza cuando quieres eliminar (o borrar) datos existentes.
#REPLACE se utiliza cuando quieres añadir o cambiar (o reemplazar) datos nuevos o ya existentes.
#TRUNCATE se utiliza cuando quieres vaciar (o borrar) todos los datos de la plantilla.

class Pepe (Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Ventana')
        self.set_resizable(False) #Esto es para evitar que se modifique el tamaño de la ventana#
        boton=Gtk.Button('Soy un boton')
        self.add(boton)
algo=Pepe()
algo.connect('destroy',Gtk.main_quit)
algo.show_all()
Gtk.main()
