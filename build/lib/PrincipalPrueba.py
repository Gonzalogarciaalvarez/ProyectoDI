import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import _sqlite3 as base
conectar = base.connect('BaseDeDatos.dat')
cursor = conectar.cursor()

class Principal (Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Inicio',border_width=20)

        Store= Gtk.ListStore(str, str, str, str, str, str)

        palo = cursor.execute("select * from proveedores")
        for a in palo:
            Store.append(a)
            palote = a
            print(a)
        palito=len(palote)

        proveedor = Gtk.TreeView(Store)

        lista = ("id", "nombre", "dni", "direccion", "telefono", "awsdfafsgf")
        for a in range(palito):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(lista[a], celda, text=a)
            proveedor.append_column(columna)

        self.add(proveedor)




principal=Principal()
principal.connect('destroy', Gtk.main_quit)
principal.show_all()
Gtk.main()