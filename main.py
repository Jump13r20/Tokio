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
        frame.grid(row = 0, column =0, columnspan=4, pady =15)

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
        self.catalogo = Label(frame, text="Catalogo: ").grid(row=3, column=0)

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
        self.confirmacion = Label(text="", fg = 'red')
        self.confirmacion.grid(row = 1, column = 0, columnspan = 4, sticky= W + E)

        #boton eliminar
        self.boton_eliminar = ttk.Button(text = 'ELIMINAR', command=self.eliminar_producto())
        self.boton_eliminar.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        #boton editar
        self.boton_editar = ttk.Button(text = 'EDITAR', command= self.editar_producto())
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
        #self.tabla['padding'] = 5,10
        self.tabla.heading('1', text = 'Nombre', anchor = CENTER)
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

        self.

    def editar_producto(self):

        pass



if __name__ == '__main__':

    root = Tk()
    app = Producto(root)
    root.mainloop()