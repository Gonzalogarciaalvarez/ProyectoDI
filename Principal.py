import webbrowser as wb
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import _sqlite3 as base
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import doctest

"""
Aqui nos conectamos con la base de datos en la cual se va a guardar la informacion de nuestra empresa
"""
conectar = base.connect('BaseDeDatos.dat')
cursor = conectar.cursor()

class Principal (Gtk.Window):
    """
    Esta clase forma la ventana principal donde gira todo el proyecto
    Contiene una caja con 5 botones, uno te saca del programa y el resto te llevan a otras ventanas donde sea que necesites gestionar tu empresa
    """
    def __init__(self):
        Gtk.Window.__init__(self, title='Inicio',border_width=20)
        self.set_default_size(800, 500)
        self.grid = Gtk.Grid(row_homogeneous=True, column_homogeneous=True, row_spacing=10, column_spacing=10,border_width=5)
        header = Gtk.HeaderBar(title="Gonzalo Co.", name="cabecera")
        self.set_titlebar(header)

        """
        Aqui esta la caja de la ventana principal
        """
        self.caja= Gtk.Box(spacing=10)
        self.add(self.caja)

        """
        Este es el boton que nos llevara al apartado de gestion de los clientes
        """
        self.clientes = Gtk.Button(label="Clientes")
        self.clientes.connect("clicked", self.Clientes)
        self.add(self.clientes)
        self.caja.pack_start(self.clientes, True, True, 0)

        """
        Este es el boton que nos llevara al apartado de gestion de los proveedores
        """
        self.proveedores= Gtk.Button(label="Proveedores")
        self.proveedores.connect("clicked", self.Proveedores)
        self.add(self.proveedores)
        self.caja.pack_start(self.proveedores, True, True, 0)
        self.hide()

        """
        Este es el boton que nos llevara al apartado de gestion de los productos
        """
        self.productos = Gtk.Button(label="Productos")
        self.productos.connect("clicked", self.Productos)
        self.add(self.productos)
        self.caja.pack_start(self.productos, True, True, 0)

        """
        Este es el boton que nos llevara al apartado de gestion de las compras
        """
        self.comprar = Gtk.Button(label="Comprar")
        self.comprar.connect("clicked", self.Comprar)
        self.add(self.comprar)
        self.caja.pack_start(self.comprar, True, True, 0)

        """
        Este es el boton de salida del programa
        """
        self.salir = Gtk.Button(label="Salir")
        self.salir.connect("clicked", self.Salir)
        self.add(self.salir)
        self.caja.pack_start(self.salir, True, True, 0)

    """
    Aqui le atribuimos al boton de salida la capacidad de sacarnos del programa
    """
    def Salir(self, Widget):
        Gtk.main_quit()


    """
    Aqui comienza la ventana de los productos
    """
    class Productos(Gtk.Window):
        def __init__(self, widget):
            Gtk.Window.__init__(self, title='Gestion de los productos')
            self.set_default_size(800, 500)
            """En esta caja iran dentro un treeview y dos botones"""
            self.caja = Gtk.Box(spacing=10)
            self.add(self.caja)

            """
            En este treeview nos aparecera que productos tenemos disponibles y en que cantidad
            Los datos vienen dados desde la base de datos, de donde sacamos la id, el nombre del producto, la cantidad y el precio por unidad
            """
            Store= Gtk.ListStore(str,str,str,str)
            palo = cursor.execute("select * from productos")
            for a in palo:
                Store.append(a)
                palote = a
            palito= len(palote)

            self.producto= Gtk.TreeView(Store)

            lista=("Id","Nombre Producto", "Stock", "Precio Unidad")
            for a in range(palito):
                celda = Gtk.CellRendererText()
                columna = Gtk.TreeViewColumn(lista[a], celda, text=a)
                self.producto.append_column(columna)
            self.caja.pack_start(self.producto, True, True, 0)

            """
            Este boton nos llevara a un formulario para introducir un nuevo producto al stock
            """
            self.nuevoproducto = Gtk.Button(label="Nuevo")
            self.nuevoproducto.connect("clicked", self.NuevoProducto)
            self.add(self.nuevoproducto)
            self.caja.pack_start(self.nuevoproducto, True, True, 0)
            """
            Este boton es el encargado de preguntarnos que producto queremos eliminar de la base de datos
            """
            self.eliminarproducto = Gtk.Button(label="Eliminar")
            self.eliminarproducto.connect("clicked", self.EliminarProducto)
            self.add(self.eliminarproducto)
            self.caja.pack_start(self.eliminarproducto, True, True, 0)

            self.show_all()
        """
        Esta es la ventana con el formulario pidiendonos la informacion necesaria para introducir un nuevo producto a nuestra base de datos
        """
        class NuevoProducto(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self, title='Nuevo Producto')
                self.set_default_size(300, 150)
                """"
                Estas son las lineas de codigo necesarias para realizar la insercion de datos dados por el usuario
                """
                def entrada(widget):
                    a = cursor.execute("insert into productos values('" + entrada1.get_text() + "','" + entrada2.get_text() +"','"+ entrada3.get_text()+"','"+ entrada4.get_text()+ "')")
                    tupla= (entrada1.get_text(),entrada2.get_text(),entrada3.get_text(),entrada4.get_text())
                    """
                    Esta tupla fue un intento de pasar los datos a la clase productos y insertarlos en el treeview, pero de momento no me sale la forma de hacerlo
                    """
                    conectar.commit()
                grid=Gtk.Grid()
                label1=Gtk.Label("Id")
                label2=Gtk.Label("Nombre")
                label3=Gtk.Label("Stock")
                label4=Gtk.Label("Precio")
                entrada1=Gtk.Entry()
                entrada2=Gtk.Entry()
                entrada3=Gtk.Entry()
                entrada4=Gtk.Entry()

                aceptar=Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 0, 2, 2, 1)
                grid.attach(label3, 0, 4, 2, 1)
                grid.attach(label4, 0, 6, 2, 1)
                grid.attach(entrada1, 2, 0, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(entrada3, 2, 4, 2, 1)
                grid.attach(entrada4, 2, 6, 2, 1)
                grid.attach(aceptar, 2, 10, 2, 1)

                self.add(grid)

                self.show_all()

        """
        Esta es la ventana donde se eliminan los productos, proximamente sera un boton simplemente y esto desaparecera
        """
        class EliminarProducto(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self,title='Eliminar Producto')
                self.set_default_size(200,100)
                """
                Esto es el codigo necesario para realizar el borrado de la base de datos, preguntando al usuario cual es la id o el nombre del producto, no necesitamos que sean ambos
                """
                def entrada(widget):
                    a = cursor.execute("delete from productos where id='"+ entrada1.get_text()+"' or NombreProducto='"+ entrada2.get_text()+"'")
                    conectar.commit()
                grid=Gtk.Grid()
                label1=Gtk.Label("ID")
                label2=Gtk.Label("Nombre producto")
                entrada1=Gtk.Entry()
                entrada2=Gtk.Entry()

                aceptar=Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 2, 0, 2, 1)
                grid.attach(entrada1, 0, 2, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(aceptar, 1, 4, 2, 1)

                self.add(grid)
                self.show_all()

    """
    Esta es la ventana responsable de gestionar a los clientes
    """
    class Clientes(Gtk.Window):
        def __init__(self, widget):
            Gtk.Window.__init__(self, title="Gestion de los clientes")

            self.set_default_size(800,500)
            """
            Esta es la caja que tendra el treeview mostrando la informacion de los clientes y los botones para gestionarla
            """
            self.caja = Gtk.Box(spacing=10)
            self.add(self.caja)

            """
            Este es el treeview donde se mostrara la informacion de los clientes
            """
            Store= Gtk.ListStore(str, str, str, str, str)

            palo = cursor.execute("select * from clientes")
            for a in palo:
                Store.append(a)
                palote = a
            palito=len(palote)

            self.cliente = Gtk.TreeView(Store)

            lista=("Dni", "Nombre", "Telefono", "Direccion", "Email")
            for a in range(palito):
                celda = Gtk.CellRendererText()
                columna = Gtk.TreeViewColumn(lista[a], celda, text=a)
                self.cliente.append_column(columna)
            self.caja.pack_start(self.cliente, True, True, 0)

            """
            Este es el boton que nos llevara al formulario pidiendo los datos del nuevo cliente
            """
            self.nuevo = Gtk.Button(label="Nuevo")
            self.nuevo.connect("clicked", self.NuevoCliente)
            self.add(self.nuevo)
            self.caja.pack_start(self.nuevo, True, True, 0)
            """
            Este es el boton encargado del borrado de la informacion de algun antiguo cliente el cual ya no desee que tengamos mas informacion de el
            """
            self.eliminar = Gtk.Button(label="Eliminar")
            self.eliminar.connect("clicked", self.EliminarCliente)
            self.add(self.eliminar)
            self.caja.pack_start(self.eliminar, True, True, 0)
            self.show_all()

        """
        Ventana con el formulario de introduccion de datos para el nuevo cliente
        """
        class NuevoCliente(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self, title='Nuevo CLiente')
                self.set_default_size(300,100)
                """
                Esta es la insercion de datos del formulario a la base de datos
                """
                def entrada(widget):
                    a = cursor.execute("insert into clientes values('"+ entrada1.get_text() + "','"+ entrada2.get_text() +"','"+ entrada3.get_text()+"','"+ entrada4.get_text()+"','"+ entrada5.get_text() + "')")
                    conectar.commit()
                grid=Gtk.Grid()
                label1=Gtk.Label("Dni")
                label2=Gtk.Label("Nombre")
                label3=Gtk.Label("Telefono")
                label4=Gtk.Label("Direccion")
                label5=Gtk.Label("Email")
                entrada1=Gtk.Entry()
                entrada2 = Gtk.Entry()
                entrada3 = Gtk.Entry()
                entrada4 = Gtk.Entry()
                entrada5 = Gtk.Entry()

                aceptar=Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 0, 2, 2, 1)
                grid.attach(label3, 0, 4, 2, 1)
                grid.attach(label4, 0, 6, 2, 1)
                grid.attach(label5, 0, 8, 2, 1)
                grid.attach(entrada1, 2, 0, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(entrada3, 2, 4, 2, 1)
                grid.attach(entrada4, 2, 6, 2, 1)
                grid.attach(entrada5, 2, 8, 2, 1)
                grid.attach(aceptar, 2, 10, 2, 1)

                self.add(grid)

                self.show_all()

        """
        Aqui preguntamos que cliente quiere ser borrado, preguntando su nombre o su dni
        """
        class EliminarCliente(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self,title='Eliminar Cliente')
                self.set_default_size(300,100)
                def entrada(widget):
                    a = cursor.execute("delete from clientes where dni='"+ entrada1.get_text()+"' or nombreCliente='"+entrada2.get_text()+"'")
                    conectar.commit()
                grid=Gtk.Grid()
                label1=Gtk.Label("Dni")
                label2=Gtk.Label("Nombre del cliente")
                entrada1=Gtk.Entry()
                entrada2=Gtk.Entry()

                aceptar=Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 2, 0, 2, 1)
                grid.attach(entrada1, 0, 2, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(aceptar, 1, 4, 2, 1)

                self.add(grid)
                self.show_all()

    """
    Esta es la ventana responsable de gestionar los proveedores
    """
    class Proveedores(Gtk.Window):
        def __init__(self, widget):
            Gtk.Window.__init__(self, title="Gestion de proveedores")

            self.set_default_size(800,500)
            """
            Esta caja contiene un treeview y dos botones que gestionaran la informacion de nuestros proveedores
            """
            self.caja = Gtk.Box(spacing=10)
            self.add(self.caja)
            """
            En este treeview se mostrara la informacion de nuestros proveedores
            """
            Store= Gtk.ListStore(str,str,str,str,str,str)
            palo = cursor.execute("select * from proveedores")
            for a in palo:
                Store.append(a)
                palote = a
            palito= len(palote)

            self.proveedores= Gtk.TreeView(Store)

            lista=("id","Nombre", "CIF", "Direccion", "Telefono", "Email")
            for a in range(palito):
                celda = Gtk.CellRendererText()
                columna = Gtk.TreeViewColumn(lista[a], celda, text=a)
                self.proveedores.append_column(columna)
            self.caja.pack_start(self.proveedores, True, True, 0)


            """
            Este boton nos llevara a un formulario donde preguntaremos la informacio necesaria del nuevo proveedor
            """
            self.nuevo = Gtk.Button(label="Nuevo")
            self.nuevo.connect("clicked", self.NuevoProveedor)
            self.add(self.nuevo)
            self.caja.pack_start(self.nuevo, True, True, 0)
            """
            Este boton nos permitira eliminar la informacion de un proveedor
            """
            self.eliminar = Gtk.Button(label="Eliminar")
            self.eliminar.connect("clicked", self.EliminarProveedor)
            self.add(self.eliminar)
            self.caja.pack_start(self.eliminar, True, True, 0)
            self.show_all()
        """
        Esta es la ventana responsable de que introduzcamos la informacion del nuevo proveedor en la base de datos
        """
        class NuevoProveedor(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self, title='Nuevo Proveedor')
                self.set_default_size(300,200)
                """
                Este es el formulario de entrada de datos para introducir los datos en la base de datos
                """
                def entrada(widget):
                    a = cursor.execute("insert into proveedores values('"+ entrada1.get_text() + "','"+ entrada2.get_text() +"','"+ entrada3.get_text()+"','"+ entrada4.get_text()+"','"+ entrada5.get_text() +"','"+ entrada6.get_text()+ "')")
                    conectar.commit()
                grid=Gtk.Grid()
                label1=Gtk.Label("Id")
                label2=Gtk.Label("Nombre")
                label3=Gtk.Label("CIF")
                label4=Gtk.Label("Direccion")
                label5=Gtk.Label("Telefono")
                label6=Gtk.Label("Email")
                entrada1=Gtk.Entry()
                entrada2=Gtk.Entry()
                entrada3=Gtk.Entry()
                entrada4=Gtk.Entry()
                entrada5=Gtk.Entry()
                entrada6=Gtk.Entry()

                aceptar=Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 0, 2, 2, 1)
                grid.attach(label3, 0, 4, 2, 1)
                grid.attach(label4, 0, 6, 2, 1)
                grid.attach(label5, 0, 8, 2, 1)
                grid.attach(label6, 0, 10, 2, 1)
                grid.attach(entrada1, 2, 0, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(entrada3, 2, 4, 2, 1)
                grid.attach(entrada4, 2, 6, 2, 1)
                grid.attach(entrada5, 2, 8, 2, 1)
                grid.attach(entrada6, 2, 10, 2, 1)
                grid.attach(aceptar, 2, 12, 2, 1)

                self.add(grid)

                self.show_all()

        """
        En esta ventana se borran los proveedores
        """
        class EliminarProveedor(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self,title='Eliminar Proveedor')
                self.set_default_size(300,100)
                """
                Aqui preguntando cual es el id del proveedor o su nombre podremos borrar sus datos de la base de datos
                """
                def entrada(widget):
                    a = cursor.execute("delete from proveedores where id='"+ entrada1.get_text()+"' or Nombre='"+ entrada2.get_text()+"'")
                    conectar.commit()

                grid = Gtk.Grid()
                label1 = Gtk.Label("ID")
                label2 = Gtk.Label("Nombre")
                entrada1 = Gtk.Entry()
                entrada2 = Gtk.Entry()

                aceptar = Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 2, 0, 2, 1)
                grid.attach(entrada1, 0, 2, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(aceptar, 1, 4, 2, 1)

                self.add(grid)
                self.show_all()

    """
    Esta es la ventana responsable de gestionar las compras y de generar las facturas
    """
    class Comprar (Gtk.Window):
        def __init__(self,Widget):
            Gtk.Window.__init__(self, title="Haga aqui sus compras")

            self.set_default_size(800,500)
            """
            Esta caja contiene un treeview y dos botones relacionados con las compras y la generacion de facturas
            """
            self.caja = Gtk.Box(spacing=10)
            self.add(self.caja)
            """
            Este treeview te permite ver las compras que hemos realizado, el dni del cliente, que producto compro y que cantidad
            """
            Store= Gtk.ListStore(str, str, str, str)
            palo = cursor.execute("select * from facturas")
            for a in palo:
                Store.append(a)
                palote = a
            palito= len(palote)

            self.compra= Gtk.TreeView(Store)

            lista =("Id", "DNI", "Nombre Producto", "Cantidad")
            for a in range(palito):
                celda = Gtk.CellRendererText()
                columna = Gtk.TreeViewColumn(lista[a], celda, text=a)
                self.compra.append_column(columna)
            self.caja.pack_start(self.compra, True, True, 0)

            """
            Este boton nos permitira registrar una nueva compra
            """
            self.nueva = Gtk.Button(label="Nueva compra")
            self.nueva.connect("clicked", self.NuevaCompra)
            self.add(self.nueva)
            self.caja.pack_start(self.nueva, True, True, 0)
            """
            Este boton nos permitira imprimir la informacion requerida de alguna compra en forma de pdf
            """
            self.imprimir = Gtk.Button(label="Imprimir")
            self.imprimir.connect("clicked", self.ImprimirCompra)
            self.add(self.imprimir)
            self.caja.pack_start(self.imprimir, True, True, 0)
            self.show_all()

        """
        Esta ventana es la responsable de gestionar una nueva compra
        """
        class NuevaCompra(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self, title='Nueva Compra')
                self.set_default_size(350,150)
                """
                Aqui introducimos la nueva compra dentro de la base de datos en la seccion de facturas
                Pero ademas de eso tambien actualizamos el stock dependiendo de cuanta cantidad se haya comprado en esta ocasion
                :type b : int
                :param b : La cantidad de stock que habia
                :type c : int
                :param c : La cantidad de producto que acaban de comprar
                :type d : int
                :param d : La cantidad de stock que queda
                
                Y actualizamos la base de datos en el apartado de productos con un update con el valor d
                
                """
                def entrada(widget):
                    a = cursor.execute("insert into facturas values('" + entrada1.get_text() + "','" + entrada2.get_text() +"','"+ entrada3.get_text()+"','"+ entrada4.get_text()+ "')")
                    cursor.execute("SELECT Stock FROM productos WHERE NombreProducto ='"+ entrada3.get_text()+"'" )
                    for row in cursor.fetchall():
                        b = int (row[0])
                    cursor.execute("SELECT Cantidad FROM facturas WHERE idFactura ='"+ entrada1.get_text()+"'")
                    for row in cursor.fetchall():
                        c = int (row[0])
                    d = str (b-c)
                    cursor.execute("UPDATE productos SET Stock='"+d+"' WHERE NombreProducto ='"+ entrada3.get_text()+"'" )
                    conectar.commit()
                grid=Gtk.Grid()
                label1 = Gtk.Label("Id de la factura")
                label2 = Gtk.Label("Dni del cliente")
                label3 = Gtk.Label("Nombre del producto")
                label4 = Gtk.Label("Cantidad")
                entrada1 = Gtk.Entry()
                entrada2 = Gtk.Entry()
                entrada3 = Gtk.Entry()
                entrada4 = Gtk.Entry()

                aceptar = Gtk.Button("Aceptar")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(label2, 0, 2, 2, 1)
                grid.attach(label3, 0, 4, 2, 1)
                grid.attach(label4, 0, 6, 2, 1)
                grid.attach(entrada1, 2, 0, 2, 1)
                grid.attach(entrada2, 2, 2, 2, 1)
                grid.attach(entrada3, 2, 4, 2, 1)
                grid.attach(entrada4, 2, 6, 2, 1)
                grid.attach(aceptar, 2, 10, 2, 1)

                self.add(grid)

                self.show_all()

        """
        Esto es una ventana en la cual nos preguntan la id de la factura que queremos imprimir y seguidamente realiza un pdf con la informacion que se pide
        """
        class ImprimirCompra(Gtk.Window):
            def __init__(self, widget):
                Gtk.Window.__init__(self, title="Imprimir")
                self.set_default_size(350,150)
                def entrada(widget):
                    doc = SimpleDocTemplate("Facturacion.pdf", pagesize=A4)
                    presentacion = ["Aqui aparece una tabla con lo referente a la compra que ha realizado. Cualquier duda o sugerencia comunicarselo a Gonzalo Garcia Alvarez"]
                    elements = []
                    cursor.execute("select * from facturas where idFactura='"+ entrada1.get_text()+"'")
                    titulo = ('Id Factura','Dni del cliente','Producto','Cantidad')
                    data = []
                    data.append(titulo)
                    for valor in cursor.fetchall():
                        data.append(valor)

                    try:
                        x = len(valor)
                    except UnboundLocalError:
                        x=1

                    i = len(data)

                    t = Table(data, x * [3 * cm], i * [2 * cm]) #Modificar esto para cambiar el tamaño de las celdas
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (4, 0), colors.aqua),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ]))
                    estiloHoja = getSampleStyleSheet()
                    estiloN =estiloHoja['Normal']
                    elements.append(Paragraph("Factura Gonzalo Co..",estiloN))
                    elements.append(Spacer(0,20))
                    elements.append(t)
                    elements.append(Spacer(0,20))
                    elements.append(Paragraph("Esperamos que todo este de su agrado y que tenga un buen dia.",estiloN))
                    elements.append(Spacer(0,20))
                    elements.append(Paragraph("¡Hasta la proxima!",estiloN))
                    doc.build(elements)
                    wb.open_new("Facturacion.pdf")
                    return x
                grid = Gtk.Grid()
                label1 = Gtk.Label("Introduce la id de la factura que deseas imprimir")
                entrada1 = Gtk.Entry()

                aceptar = Gtk.Button("Imprimir")
                aceptar.connect("clicked", entrada)
                grid.attach(label1, 0, 0, 2, 1)
                grid.attach(entrada1, 0, 2, 2 ,1)
                grid.attach(aceptar, 0, 4, 2, 1)

                self.add(grid)

                self.show_all()

principal=Principal()
principal.connect('destroy', Gtk.main_quit)
principal.show_all()
Gtk.main()


