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
        frame.grid(row = 0, column =0, columnspan=4, pady =20)

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

        #Personalizarcion de la tabla
        styles = ttk.Style()
        styles.configure("myestilo.Treeview", highlightthickness= 0, bd=0, font=('Calibri', 11))
        styles.configure("myestilo.Treeview.Heading", font=('Calibri', 13, 'bold'))
        styles.layout("myestilo.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        #estructura de la tabla

        columnas = (1, 2, 3,4)
        self.tabla = ttk.Treeview(height= 20, columns = columnas, style = "myestilo.Treeview", show='headings')
        self.tabla.grid(row = 4, column = 0, columnspan = 4)
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
        return con, cur
    con, cur = creacionDb()

    def consultaDb(self, consulta, parametro = ()):

        resultado = self.cur.execute(consulta, parametro)
        return resultado


    def get_producto(self):

        query = 'SELECT * FROM productos ORDER BY Name DESC'
        registros = self.consultaDb(query)

        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text=fila[0], values=fila[1:])

    def validacionNombre(self):

        comprobasion = str(self.nombre_input.get())
        return len(comprobasion) != 0 and str == type(comprobasion)

    def validacionPrecio(self):

        comprobasion = float(self.precio_input.get())
        return len(comprobasion) != 0 and float == type(comprobasion)

    def validacionCatalogo(self):

        comprobasion = str(self.catalogo_input.get())
        return len(comprobasion) != 0 and str == type(comprobasion)

    def validacionStock(self):

        comprobasion = self.stock_input.get()
        return len(comprobasion) != 0 and int == type(comprobasion)

    def get_nuevoProducto(self):

        if self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            print("Hecho")
        elif self.validacionNombre() == False and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock():
            print("necesitas poner el nombre y no puede contener numeros")
        elif self.validacionNombre() and self.validacionPrecio() == False and self.validacionCatalogo() and self.validacionStock():
            print("necesitas poner el precio y no puede contener letras")
        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() == False and self.validacionStock():
            print("necesitas poner el catalogo y no puede contener numeros")
        elif self.validacionNombre() and self.validacionPrecio() and self.validacionCatalogo() and self.validacionStock() == False:
            print("necesitas poner el stock y no puedo contener letras")
        else:
            print("El nombre, el precio, el catalogo y el stock son obligatorios.")

if __name__ == '__main__':

    root = Tk()
    app = Producto(root)
    root.mainloop()