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
        frame = LabelFrame(self.ventana,text = "Registra un nuevo producto", padx=20, pady=10)
        frame.grid(row = 0, column =0, columnspan=4, pady =8)

        #label nombre
        self.nombre = Label(frame, text="Nombre: ").grid(row = 1, column = 0)

        #input para almacenar el nombre
        self.nombre_input = Entry(frame)
        self.nombre_input.grid(row = 1, column = 1)
        self.nombre_input.focus()

        #label precio
        self.precio = Label(frame, text="Precio: ").grid(row = 2, column = 0)

        #input para almacenar el precio

        self.precio_input = Entry(frame)
        self.precio_input.grid(row = 2, column = 1, pady= 5)

        # label catalogo
        self.catalogo = Label(frame, text="Categoria: ").grid(row=3, column=0)

        # input para almacenar el catalogo
        self.catalogo_input = Entry(frame)
        self.catalogo_input.grid(row=3, column=1)

        # label stock
        self.stock = Label(frame, text="Stock: ").grid(row=4, column=0)

        # input para almacenar el stock
        self.stock_input = Entry(frame).grid(row=4, column=1, pady=5)

        self.stock_input = Entry(frame)
        self.stock_input.grid(row=4, column=1, pady=5)

        #boton dentro del frame.
        self.boton = ttk.Button(frame, text="Guardar Producto", command=self.get_nuevoProducto)
        self.boton.grid(row = 5, columnspan = 2, sticky= W + E, pady= 5)

        #texto para confirmar al usuario.
        self.confirmacion = Label(text="", fg = 'red', font=('Calibri',13, 'bold'))
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
        self.tabla.heading('1', text = 'Nombre', anchor = tkinter.CENTER)
        self.tabla.heading('2', text='Precio', anchor = CENTER)
        self.tabla.heading('3',text='Catalogo', anchor=CENTER)
        self.tabla.heading('4', text='Stock', anchor=CENTER)


        self.get_producto()




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
    con = creacionDb()
    cur = con.cursor()

    def consultaDb(self, consulta, parametro = ()):

        resultado = self.cur.execute(consulta, parametro)
        self.con.commit()
        return resultado


    def get_producto(self):

        registros_tabla = self.tabla.get_children()

        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM productos ORDER BY Name DESC'
        registros = self.consultaDb(query)

        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text=fila[0], values=fila[1:])

    def pruebaNumerico(self,prueba):

        return prueba.isdigit()

    def pruebaAlpha(self,prueba):
        return prueba.isalpha()

    def validacionNombre(self):

        comprobasion = self.nombre_input.get()
        print(comprobasion)
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

    def get_nuevoProducto(self):

        if self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            query = "INSERT INTO productos (Name, Price, Catalogue, Stock) VALUES (?,?,?,?)"
            parametros = (self.nombre_input.get(),self.precio_input.get(),self.catalogo_input.get(), self.stock_input.get())
            self.consultaDb(query,parametros)
            self.get_producto()
            self.confirmacion['text'] = 'El producto {} se añadido correctamente'.format(self.nombre_input.get())
            print("Hecho")
        elif self.validacionNombre() == False and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el nombre y no puede contener numeros'
            print("necesitas poner el nombre y no puede contener numeros")
        elif self.validacionNombre() and self.validacionPrecio() == False and self.validacionCatalogo() and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el precio y no puede contener letras'
            print("necesitas poner el precio y no puede contener letras")
        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() == False and self.validacionStock():
            self.confirmacion['text'] = 'necesitas poner el catalogo y no puede contener numeros'
            print("necesitas poner el catalogo y no puede contener numeros")
        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock() == False:
            self.confirmacion['text'] = 'necesitas poner el stock y no puedo contener letras'
            print("necesitas poner el stock y no puedo contener letras")
        else:
            self.confirmacion['text'] = 'El nombre, el precio, el catalogo y el stock son obligatorios.'
            print("El nombre, el precio, el catalogo y el stock son obligatorios.")

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

    def editar_producto(self):

        self.confirmacion['text']= ""
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.confirmacion['text'] = "Seleccione algún articulo."
            return

        self.confirmacion['text'] = ""

        antiguo_nombre = self.tabla.item(self.tabla.selection())['values'][0]
        antiguo_precio = self.tabla.item(self.tabla.selection())['values'][1]
        antiguo_categoria = self.tabla.item(self.tabla.selection())['values'][2]
        antiguo_stock = self.tabla.item(self.tabla.selection())['values'][3]

        #Edicion de la nueva ventana creada para la edicion de los productos.

        self.ventana_editar = Toplevel()
        self.ventana_editar.title = 'Editar productos'
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')
        self.ventana_editar.geometry("540x500")  # Para tener una ventana con un tamaño predeterminado

        self.titulo = Label(self.ventana_editar, text='Edita tus productos', font=('Calibri', 50))
        self.titulo.grid(row = 0,column = 0, columnspan=4, pady=8)

        # creacion de un fram donde irá cosas principales.
        frameEditar = LabelFrame(self.ventana_editar, text="Edita el producto", padx=20, pady=10, font=('Calibri', 12, 'bold'))
        frameEditar.grid(row=1, column=0, columnspan=4, pady=50)

        # label nombre antiguo
        """self.tituloN_antiguo = Label(frameEditar, text="Nombre antiguo".title())
        self.tituloN_antiguo.grid(row=0, column=0)
        nombreAntiguo = self.tabla.item(self.tabla.selection())['values'][0]
        self.direcionUno = Label(frameEditar, text="---------->")
        self.direcionUno.grid(row=0, column=1)
        self.nombre_antiguo = Label(frameEditar,text ="{}".format(nombreAntiguo).upper())
        self.nombre_antiguo.grid(row=0, column=2)"""
        self.nombre_antiguo = self.tabla.item(self.tabla.selection())['values'][0]
        self.tituloN_antiguo = Label(frameEditar, text="Nombre antiguo  ------>   {}".format(self.nombre_antiguo).title(), pady = 5)
        self.tituloN_antiguo.grid(row=0, column=0,columnspan=3, sticky = W + E)
        # label nombre nuevo
        self.nombre_nuevo = Label(frameEditar, text="Nombre nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.nombre_nuevo.grid(row=1, column=0, pady=5)
        # input para almacenar el nombre nuevo
        self.nombre_inputUno = Entry(frameEditar)
        self.nombre_inputUno.grid(row=1, column=1, columnspan=3, sticky = W + E)
        self.nombre_inputUno.focus()

        # label precio antiguo
        """self.tituloP_antiguo = Label(frameEditar, text="precio antiguo".title())
        self.tituloP_antiguo.grid(row=2, column=0)
        precioAntiguo = self.tabla.item(self.tabla.selection())['values'][1]
        self.direcionDos = Label(frameEditar, text="---------->")
        self.direcionDos.grid(row=2, column=1)
        self.precio_antiguo = Label(frameEditar, text="{}".format(precioAntiguo).upper())
        self.precio_antiguo.grid(row=2, column=2)"""
        self.precio_antiguo = self.tabla.item(self.tabla.selection())['values'][1]
        self.tituloN_antiguo = Label(frameEditar, text="precio antiguo   ------>   {}".format(self.precio_antiguo).title(), pady = 5)
        self.tituloN_antiguo.grid(row=2, column=0, columnspan=3, sticky=W + E)
        # label precio
        self.precio_nuevo = Label(frameEditar, text="Precio nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.precio_nuevo.grid(row=3, column=0)
        # input para almacenar el precio
        self.precio_inputDos = Entry(frameEditar)
        self.precio_inputDos.grid(row=3, column=1, columnspan=3, sticky = W + E)

        # label categoria antiguo
        """self.tituloC_antiguo = Label(frameEditar, text="categoria antigua".title())
        self.tituloC_antiguo.grid(row=4, column=0)
        categoriaAntiguo = self.tabla.item(self.tabla.selection())['values'][2]
        self.direcionTres = Label(frameEditar, text="---------->")
        self.direcionTres.grid(row=4, column=1)
        self.categoria_antiguo = Label(frameEditar, text="{}".format(categoriaAntiguo).upper())
        self.categoria_antiguo.grid(row=4, column=2)"""
        self.categoria_antiguo = self.tabla.item(self.tabla.selection())['values'][2]
        self.tituloN_antiguo = Label(frameEditar, text="categoria antiguo  ------>   {}".format(self.categoria_antiguo).title(), pady = 5)
        self.tituloN_antiguo.grid(row=4, column=0, columnspan=3, sticky=W + E)
        # label categoria nueva
        self.categoria_nuevo = Label(frameEditar, text="Categoria nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.categoria_nuevo.grid(row=5, column=0)
        # input para almacenar la categoria nueva
        self.categoria_inputTres = Entry(frameEditar)
        self.categoria_inputTres.grid(row=5, column=1, columnspan=3, sticky=W + E)

        # label stock antiguo
        """self.tituloS_antiguo = Label(frameEditar, text="stock antigua".title())
        self.tituloS_antiguo.grid(row=6, column=0)
        stockAntiguo = self.tabla.item(self.tabla.selection())['values'][3]
        self.direcionCuatro = Label(frameEditar, text="---------->")
        self.direcionCuatro.grid(row=6, column=1)
        self.stock_antiguo = Label(frameEditar, text="{}".format(stockAntiguo).upper())
        self.stock_antiguo.grid(row=6, column=2)"""
        self.stock_antiguo = self.tabla.item(self.tabla.selection())['values'][3]
        self.tituloN_antiguo = Label(frameEditar, text="stock antiguo  ------>   {}".format(self.stock_antiguo).title(), pady = 5)
        self.tituloN_antiguo.grid(row=6, column=0, columnspan=3, sticky=W + E)
        # label stock nueva
        self.stock_nuevo = Label(frameEditar, text="stock nuevo: ".title(), font=('Calibri', 10, 'bold'))
        self.stock_nuevo.grid(row=7, column=0)
        # input para almacenar la categoria nueva
        self.stock_inputCuatro = Entry(frameEditar)
        self.stock_inputCuatro.grid(row=7, column=1, columnspan=3, sticky=W + E)

        # boton dentro del frame.
        self.boton_actualizar = ttk.Button(frameEditar, text="Actualizar producto", command=lambda : self.actualizar_producto(self.nombre_antiguo,
                                                                                                                              self.nombre_inputUno.get(),
                                                                                                                              self.precio_antiguo,
                                                                                                                              self.precio_inputDos.get(),
                                                                                                                              self.categoria_antiguo,
                                                                                                                              self.categoria_inputTres.get(),
                                                                                                                              self.stock_antiguo,
                                                                                                                              self.stock_inputCuatro.get()))
        self.boton_actualizar.grid(row=8, columnspan=4, sticky=W + E, pady=10)

    def actualizar_producto(self, antiguo_nombre, nuevo_nombre, antiguo_precio, nuevo_precio, antigua_categoria, nueva_categoria, antiguo_stock, nuevo_stock):

        modificado = False
        query = "UPDATE productos SET Name = ?, Preci = ?, Catalogue = ?, Stock = ? WHERE Name = ?, Preci = ?, Catalogue = ? AND Stock = ?"

        if nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria != "" and nuevo_stock != "":
            modificado = True
            parametros = (nuevo_nombre,nuevo_precio,nueva_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria == "" and nuevo_stock == "":
            modificado = True
            parametros = (nuevo_nombre,antiguo_precio,antigua_categoria,antiguo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria == "" and nuevo_stock == "":
            modificado = True
            parametros = (antiguo_nombre,nuevo_precio,antigua_categoria,antiguo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio == "" and nueva_categoria != "" and nuevo_stock == "":
            modificado = True
            parametros = (antiguo_nombre,antiguo_precio,nueva_categoria,antiguo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio == "" and nueva_categoria == "" and nuevo_stock != "":
            modificado = True
            parametros = (antiguo_nombre,antiguo_precio,antigua_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria != "" and nuevo_stock != "":
            modificado = True
            parametros = (antiguo_nombre,nuevo_precio,nueva_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria != "" and nuevo_stock != "":
            modificado = True
            parametros = (nuevo_nombre,antiguo_precio,nueva_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria == "" and nuevo_stock != "":
            modificado = True
            parametros = (nuevo_nombre,nuevo_precio,antigua_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria != "" and nuevo_stock == "":
            modificado = True
            parametros = (nuevo_nombre,nuevo_precio,nueva_categoria,antiguo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio == "" and nueva_categoria != "" and nuevo_stock != "":
            modificado = True
            parametros = (antiguo_nombre,antiguo_precio,nueva_categoria,nuevo_stock,antiguo_nombre,antiguo_precio,antigua_categoria,antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio != "" and nueva_categoria == "" and nuevo_stock == "":
            modificado = True
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria != "" and nuevo_stock == "":
            modificado = True
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)

        elif nuevo_nombre != "" and nuevo_precio == "" and nueva_categoria == "" and nuevo_stock != "":
            modificado = True
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria != "" and nuevo_stock == "":
            modificado = True
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)

        elif nuevo_nombre == "" and nuevo_precio != "" and nueva_categoria == "" and nuevo_stock != "":
            modificado = True
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,antigua_categoria, antiguo_stock)

        if (modificado):

            self.consultaDb(query, parametros)
            self.ventana_editar.destroy()
            self.confirmacion['text'] = "El producto {} ha sido actualizado con éxito.".format(antiguo_nombre)
            self.get_producto()

        else:

            self.ventana_editar.destroy()
            self.confirmacion['text'] = "El producto {} no ha sido actualizado con éxito.".format(antiguo_nombre)




if __name__ == '__main__':

    root = Tk()
    app = Producto(root)
    root.mainloop()