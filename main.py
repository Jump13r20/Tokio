import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    def __init__(self, root):
        self.ventana = root #ventana de la aplicacion que le llamaremos ventana.
        self.ventana.title("App de gestor de productos")#este es el titulo de la app
        self.ventana.resizable(1,1)#activamos la redimension de la ventana.
        self.ventana.wm_iconbitmap('recursos/M6_P2_icon.ico')
        #self.ventana.geometry("500x500")#Para tener una ventana con un tamaño predeterminado

        #self.ventana.config(bg="black")#Color de fondo de la ventana.

        #creacion de un fram donde irá cosas principales.
        frame = LabelFrame(self.ventana,text = "Registra un nuevo producto", padx=30, pady=20, font=('Calibri', 11, 'bold'))
        frame.grid(row = 0, column =0, columnspan=4, pady =8)

        #label nombre
        self.nombre = Label(frame, text="Nombre: ", font=('Calibri', 10, 'bold'))
        self.nombre.grid(row = 1, column = 0, )

        #input para almacenar el nombre
        self.nombre_input = Entry(frame)
        self.nombre_input.grid(row = 1, column = 1)
        self.nombre_input.focus()

        #label precio
        self.precio = Label(frame, text="Precio: ", font=('Calibri', 10, 'bold'))
        self.precio.grid(row = 2, column = 0)

        #input para almacenar el precio

        self.precio_input = Entry(frame)
        self.precio_input.grid(row = 2, column = 1, pady= 8)

        # label catalogo
        self.catalogo = Label(frame, text="Categoria: ", font=('Calibri', 10, 'bold'))
        self.catalogo.grid(row=3, column=0)

        # input para almacenar el catalogo
        self.catalogo_input = Entry(frame)
        self.catalogo_input.grid(row=3, column=1)

        # label stock
        self.stock = Label(frame, text="Stock: ", font=('Calibri', 10, 'bold'))
        self.stock.grid(row=4, column=0)

        # input para almacenar el stock
        self.stock_input = Entry(frame)
        self.stock_input.grid(row=4, column=1, pady=8)

        #boton dentro del frame.
        self.boton = ttk.Button(frame, text="Guardar Producto", command=self.get_nuevoProducto)
        self.boton.grid(row = 5, columnspan = 2, sticky= W + E, pady= 5)

        #texto para confirmar al usuario.
        self.confirmacion = Label(text="", fg = 'red', font=('Calibri',10, 'bold'))
        self.confirmacion.grid(row = 1, column = 0, columnspan = 4, sticky= W + E, pady= 10)

        #boton eliminar
        self.boton_eliminar = ttk.Button(text = 'ELIMINAR', command=self.eliminar_producto)
        self.boton_eliminar.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        #boton editar
        self.boton_editar = ttk.Button(text = 'EDITAR', command= self.editar_producto)
        self.boton_editar.grid(row=3, column= 2, columnspan = 2, sticky= W + E)

        #Personalizarcion de la tabla
        styles = ttk.Style()
        styles.configure("myestilo.Treeview", highlightthickness= 0, bd=0, font=('Calibri', 11))
        styles.configure("myestilo.Treeview.Heading", font=('Calibri', 13, 'bold'))
        styles.layout("myestilo.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        #estructura de la tabla

        columnas = (1, 2, 3,4)
        self.tabla = ttk.Treeview(height= 20, columns = columnas, style = "myestilo.Treeview", show='headings')
        self.tabla.grid(row = 2, column = 0, columnspan = 4)
        self.tabla.heading('1', text = 'Nombre', anchor = CENTER)
        self.tabla.heading('2', text='Precio', anchor = CENTER)
        self.tabla.heading('3',text='Catalogo', anchor=CENTER)
        self.tabla.heading('4', text='Stock', anchor=CENTER)


        self.get_producto()




    #Esta funcion es en donde se creara la base de datos de SQLite teniendo unos datos predefinidos.
    def creacionDb():
        with sqlite3.connect('database/productos.db') as con:

            cur = con.cursor()
            cur.execute("DROP TABLE productos")
            print("Se eliminado la tabla")
            cur.execute("CREATE TABLE productos (id_producto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Name VARCHAR NOT NULL, Price FLOAT NOT NULL, Catalogue TEXT NOT NULL, Stock INTEGER NOT NULL)")
            print("Tabla creada")
            cur.execute("INSERT INTO productos (Name, Price, Catalogue, Stock) VALUES ('portatil',255,'informatica',25)")
            con.commit()
        return con
    #lo saque de la funcion para poder utilizarlo en elgun momento en otras funciones
    con = creacionDb()
    cur = con.cursor()

    # en esta funciones es en donde se harán las consultas a la base de datos o si tenemos que editar los datos.
    def consultaDb(self, consulta, parametro = ()):

        resultado = self.cur.execute(consulta, parametro)
        self.con.commit()
        return resultado

    #En esta funcion es la que utilizaremos para poder ver todo lo que hay dentro de la base de datos.
    def get_producto(self):

        registros_tabla = self.tabla.get_children()

        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM productos ORDER BY Name DESC'
        registros = self.consultaDb(query)

        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text=fila[0], values=fila[1:])

    #Aquí hice algunas funciones de prueba numerica y alfabetica.
    def pruebaNumerico(self,prueba):

        return prueba.isdigit()

    def pruebaAlpha(self,prueba):
        return prueba.isalpha()

    #en esta funcion implemento tambien las pruebas anteriores.
    def validacionNombre(self):

        comprobasion = self.nombre_input.get()
        return len(comprobasion) != 0 and self.pruebaAlpha(comprobasion)

    def validacionPrecio(self):

        comprobasion = self.precio_input.get()
        return len(comprobasion) != 0 and self.pruebaNumerico(comprobasion)

    def validacionCatalogo(self):

        comprobasion = self.catalogo_input.get()
        return len(comprobasion) != 0 and self.pruebaAlpha(comprobasion)

    def validacionStock(self):

        comprobasion = self.stock_input.get()
        return len(comprobasion) != 0 and self.pruebaNumerico(comprobasion)

    #en esta funcion añadiremos nuevos datos a la base datos y tambien para que salga en la tabla que haremos en el programa para visualizar los datos de la Data Base
    def get_nuevoProducto(self):

        if self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            query = "INSERT INTO productos (Name, Price, Catalogue, Stock) VALUES (?,?,?,?)"
            parametros = (self.nombre_input.get(),self.precio_input.get(),self.catalogo_input.get(), self.stock_input.get())
            self.consultaDb(query,parametros)
            self.get_producto()
            self.confirmacion['text'] = 'El producto {} se añadido correctamente'.format(self.nombre_input.get())
            self.nombre_input.delete(0, END)
            self.precio_input.delete(0, END)
            self.catalogo_input.delete(0, END)
            self.stock_input.delete(0, END)
            self.nombre_input.focus()

        elif self.validacionNombre() == False and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el nombre y no puede contener numeros'

        elif self.validacionNombre() and self.validacionPrecio() == False and self.validacionCatalogo() and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el precio y no puede contener letras'

        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() == False and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el catalogo y no puede contener numeros'

        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock() == False:
            self.confirmacion['text'] = 'necesitas poner el stock y no puedo contener letras'

        else:
            self.confirmacion['text'] = 'El nombre, el precio, el catalogo y el stock son obligatorios.'

    #En esta funcion eliminaremos los productos puestos en la tabla y tambien directamente de la base de datos.
    def eliminar_producto(self):

        self.confirmacion["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.confirmacion['text'] = "Seleccione algún articulo."
            return

        self.confirmacion['text'] = ""
        nombre = self.tabla.item(self.tabla.selection())['values'][0]
        query = "DELETE FROM productos WHERE Name = ?"
        self.consultaDb(query, (nombre,))
        self.confirmacion["text"]= "Se ha eliminado {} de la lista de productos.".format(nombre)
        self.get_producto()

    #En esta funcion editaremos los productos que estan en la tabla y al mismo tiempo tambien en la base de datos. Abriendo una nueva ventana.
    def editar_producto(self):

        #esta es una prueba de si no selecciones algun articulo te saldra un aviso de para poder editar tienes que seleccionar algun articulo.
        self.confirmacion['text']= ""
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.confirmacion['text'] = "Seleccione algún articulo."
            return

        self.confirmacion['text'] = ""

        antiguo_nombreUno = self.tabla.item(self.tabla.selection())['values'][0]
        antiguo_precioUno = self.tabla.item(self.tabla.selection())['values'][1]
        antiguo_categoriaUno = self.tabla.item(self.tabla.selection())['values'][2]
        antiguo_stockUno = self.tabla.item(self.tabla.selection())['values'][3]

        #Edicion de la nueva ventana creada para la edicion de los productos.

        self.ventana_editar = Toplevel()
        self.ventana_editar.title = 'Editar productos'
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')
        self.ventana_editar.geometry("500x490")  # Para tener una ventana con un tamaño predeterminado

        self.titulo = Label(self.ventana_editar, text='Edita tu producto', font=('roman', 50, 'bold'))
        self.titulo.grid(row = 0,column = 0, columnspan=4, pady=8)

        # creacion de un fram donde irá cosas principales.
        frameEditar = LabelFrame(self.ventana_editar, text="Edita el producto", padx=20, pady=10, font=('Calibri', 12, 'bold'))
        frameEditar.grid(row=1, column=0, columnspan=4, pady=20)

        # label nombre antiguo
        self.tituloN_antiguo = Label(frameEditar, text="Nombre antiguo  ------>   ".title(), pady = 5)
        self.input_antiguo_nombre = Entry(frameEditar, textvariable=StringVar(self.ventana_editar, value=antiguo_nombreUno), state='readonly')
        self.tituloN_antiguo.grid(row=0, column=0, sticky = W + E)
        self.input_antiguo_nombre.grid(row=0, column=1)
        # label nombre nuevo
        self.nombre_nuevo = Label(frameEditar, text="Nombre nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.nombre_nuevo.grid(row=1, column=0, pady=5)
        # input para almacenar el nombre nuevo
        self.nombre_inputUno = Entry(frameEditar)
        self.nombre_inputUno.grid(row=1, column=1, columnspan=3, sticky = W + E)
        self.nombre_inputUno.focus()

        # label precio antiguo
        self.input_antiguo_precio = Entry(frameEditar,textvariable=StringVar(self.ventana_editar, value=antiguo_precioUno),state='readonly')
        self.input_antiguo_precio.grid(row=2, column=1)
        self.tituloN_antiguo = Label(frameEditar, text="precio antiguo   ------>   ".title(), pady = 5)
        self.tituloN_antiguo.grid(row=2, column=0, sticky=W + E)
        # label precio
        self.precio_nuevo = Label(frameEditar, text="Precio nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.precio_nuevo.grid(row=3, column=0)
        # input para almacenar el precio
        self.precio_inputDos = Entry(frameEditar)
        self.precio_inputDos.grid(row=3, column=1, columnspan=3, sticky = W + E)

        # label categoria antiguo
        self.input_antiguo_categoria = Entry(frameEditar,textvariable=StringVar(self.ventana_editar, value=antiguo_categoriaUno),state='readonly')
        self.input_antiguo_categoria.grid(row=4, column=1)
        self.tituloN_antiguo = Label(frameEditar, text="categoria antiguo  ------>   ".title(), pady = 5)
        self.tituloN_antiguo.grid(row=4, column=0, sticky=W + E)
        # label categoria nueva
        self.categoria_nuevo = Label(frameEditar, text="Categoria nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.categoria_nuevo.grid(row=5, column=0)
        # input para almacenar la categoria nueva
        self.categoria_inputTres = Entry(frameEditar)
        self.categoria_inputTres.grid(row=5, column=1, columnspan=3, sticky=W + E)

        # label stock antiguo
        self.input_antiguo_stock = Entry(frameEditar,textvariable=StringVar(self.ventana_editar, value=antiguo_stockUno),state='readonly')
        self.input_antiguo_stock.grid(row=6, column=1)
        self.tituloN_antiguo = Label(frameEditar, text="stock antiguo  ------>   ".title(), pady = 5)
        self.tituloN_antiguo.grid(row=6, column=0, sticky=W + E)
        # label stock nueva
        self.stock_nuevo = Label(frameEditar, text="stock nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.stock_nuevo.grid(row=7, column=0)
        # input para almacenar la categoria nueva
        self.stock_inputCuatro = Entry(frameEditar)
        self.stock_inputCuatro.grid(row=7, column=1, columnspan=3, sticky=W + E)

        # boton dentro del frame.
        self.boton_actualizar = ttk.Button(frameEditar, text="Actualizar producto", command=lambda:self.actualizar_producto(self.input_antiguo_nombre.get(), self.nombre_inputUno.get(), self.input_antiguo_precio.get(), self.precio_inputDos.get(), self.input_antiguo_categoria.get(), self.categoria_inputTres.get(), self.input_antiguo_stock.get(), self.stock_inputCuatro.get()))
        self.boton_actualizar.grid(row=8, columnspan=4, sticky=W + E, pady=10)

        #un mensaje de confirmacion dentro de la ventana de editar.
        self.confirmacionDos = Label (self.ventana_editar, text="", fg = 'red', font=('Calibri',10, 'bold'))
        self.confirmacionDos.grid(row = 2, column = 0, columnspan = 4)

    """
    Esto es una funcion que me llevo muchas horas para que quede mas o menos personalizado y con sus diferentes errores que puede haber al editar algun producto de la tabla
    Aquí tampoco te deja introducir letras y numeros juntos.
    se podra salir de dos formas normalmente de la ventana de editar.
    1. saliendo editando lo que quieras y sin que tenga ningun error.
    2. si no quieres editar nada le daras al boton de actualizar producto pero claramente si no se ha actualizado nada entonces se cerrara la ventana mandando al usuario un error de que no se ha podido actualizar un su producto.
    """
    def actualizar_producto(self, antiguo_nombre, nuevo_nombre, antiguo_precio, nuevo_precio, antigua_categoria, nueva_categoria, antiguo_stock, nuevo_stock):

        modificado = False
        query = 'UPDATE productos SET Name = ?, Price = ?, Catalogue = ?, Stock = ? WHERE Name = ? AND Price = ? AND Catalogue = ? AND Stock = ?'

        if (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros,\n precio y el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros,\n precio y el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros,\n el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros,\n precio y el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros,\n precio no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros,\n precio no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros,\n el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros,\n el stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio y en stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letras'


        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros y\n el precio no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros y\n el precio no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros y\n el precio no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letras'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio y en stock no puede contener letras y\n en categoria no puede contener numeros'

        elif (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En stock no puede contener letras y\n en categoria no puede contener numeros'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En precio y en stock no puede contener letras'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En precio no puede contener letras y\n en categoria no puede contener numeros'

        elif (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En stock no puede contener letras'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En precio no puede contener letras'

        elif (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isalpha() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio y stock no puede contener letras y\n el nombre no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isalpha() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio y stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nuevo_stock.isalpha() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros y\n en stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isalpha() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'En nombre no puede contener numeros y\n el precio no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nuevo_stock.isalpha() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != '') and (nuevo_stock.isalpha() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener letras'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isalpha() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letras'

        elif (nuevo_nombre.isdigit() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y en categoria no puede contener numeros y\n el stock no puede contener letras'

        elif (nuevo_nombre.isdigit() and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letras y\n la categoria no puede contener numeros'

        elif (nuevo_nombre.isdigit() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros y\n el stock no puede contener letras'

        elif (nuevo_nombre.isdigit() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener letras'

        elif (nuevo_nombre.isdigit() and nuevo_nombre != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letras'

        elif (nuevo_nombre.isdigit() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros'

        elif (nuevo_nombre.isdigit() and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros y\n el precio no puede contener letras'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nuevo_precio.isdigit() and nuevo_precio != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nuevo_precio.isdigit() == False and nuevo_precio != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener numeros'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letra y\n la categoria no puede contener numeros'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nueva_categoria.isalpha() and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letra'

        elif (nuevo_precio.isdigit() and nuevo_precio != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener letra'

        elif (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros y\n el stock no puede contener letras'

        elif (nueva_categoria.isalpha() == False and nueva_categoria != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nueva_categoria.isalpha() and nueva_categoria != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener numeros'

        elif (nuevo_stock.isdigit() == False and nuevo_stock != '') and (nuevo_nombre.isalpha() == False and nuevo_nombre != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letra y\n el nombre no puede contener numeros'

        elif (nuevo_stock.isdigit() == False and nuevo_stock != '') and (nuevo_nombre.isalpha() and nuevo_nombre != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letra'

        elif (nuevo_stock.isdigit() and nuevo_stock != '') and (nuevo_nombre.isalpha() == False and nuevo_nombre != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener letra'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre y categoria no puede contener numeros'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != '') and (nueva_categoria.isalpha() and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros'

        elif (nuevo_nombre.isalpha() and nuevo_nombre != '') and (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio y stock no puede contener letra'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != '') and (nuevo_stock.isdigit() and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letra'

        elif (nuevo_precio.isdigit() and nuevo_precio != '') and (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letra'

        elif (nuevo_nombre.isalpha() == False and nuevo_nombre != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El nombre no puede contener numeros'

        elif (nuevo_precio.isdigit() == False and nuevo_precio != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El precio no puede contener letra'

        elif (nueva_categoria.isalpha() == False and nueva_categoria != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'La categoria no puede contener numeros'

        elif (nuevo_stock.isdigit() == False and nuevo_stock != ''):

            self.confirmacionDos['text'] = ''
            self.confirmacionDos['text'] = 'El stock no puede contener letra'

        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock == '':

            self.ventana_editar.destroy()
            self.confirmacion['text'] = "El producto {} no ha sido actualizado con éxito.".format(antiguo_nombre)

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = ( antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != ''and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio != ''and nueva_categoria != '' and nuevo_stock == '':
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            modificado = True

        if (modificado):

            self.consultaDb(query, parametros)
            self.ventana_editar.destroy()
            self.confirmacion['text'] = "El producto {} ha sido actualizado con éxito.".format(antiguo_nombre)
            self.get_producto()

# este es el main del programa
if __name__ == '__main__':

    root = Tk()
    app = Producto(root)
    root.mainloop()