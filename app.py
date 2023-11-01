from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")  # Titulo de la ventana
        self.ventana.resizable(1, 1)  # Habilita las redimension, para desactivarla poner 0,0
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")  # Icono de la ventana

        # Creacion del contenedor Frame Principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto")
        frame.grid(row=0, column=0, columnspan=4, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ")
        self.etiqueta_categoria.grid(row=3, column=0)

        # Entry Categoría
        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ")
        self.etiqueta_stock.grid(row=4, column=0)

        # Entry Stock
        self.stock = Entry(frame)
        self.stock.grid(row=4, column=1)

        # Botón Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto)
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=5, column=0, columnspan=4, stick=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        self.tabla = ttk.Treeview(height=20, columns=[f"#{n}" for n in range(1, 4)], style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=4)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.column("#0", anchor=CENTER)
        self.tabla.heading('#1', text="Precio", anchor=CENTER)
        self.tabla.column("#1", anchor=CENTER)
        self.tabla.heading('#2', text="Categoria", anchor=CENTER)
        self.tabla.column("#2", anchor=CENTER)
        self.tabla.heading('#3', text="Stock", anchor=CENTER)
        self.tabla.column("#3", anchor=CENTER)

        # Estructura de la tabla
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto)
        boton_eliminar.grid(row=7, column=1, sticky=W + E)
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto)
        boton_editar.grid(row=7, column=2, sticky=W + E)
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla: self.tabla.delete(fila)

        # Consulta SQL
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros = self.db_consulta(query)  # Se hace la llamada al metodo db_consultas
        print(registros)

        # Escribir los datos en pantalla
        for fila in registros:
            print(fila)  # Para verificar por consola los datos
            self.tabla.insert('', "end", text=fila[1], values=(fila[2], fila[3], fila[4]))

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def validacion_categoria(self):
        return len(self.categoria.get()) != 0

    def validacion_stock(self):
        return len(self.stock.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = " Producto {} añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)
        else:
            print("Todos los campos son obligatorios")
            self.mensaje["text"] = "Todos los campos son obligatorios"
        self.get_productos()

    def del_producto(self):
        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "Producto {} eliminado con éxito".format(nombre)
        self.get_productos()

    def edit_producto(self):
        self.mensaje["text"] = ""

        old_nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]
        old_categoria = self.tabla.item(self.tabla.selection())["values"][1]
        old_stock = self.tabla.item(self.tabla.selection())["values"][2]

        self.ventana_editar = Toplevel()  # Crear una nueva ventana
        self.ventana_editar.title("Editar producto")
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Calibri", 50, "bold"))
        titulo.grid(row=0, column=0)

        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente producto")
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=("Calibri", 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)

        # Entry Nombre antiguo
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre),
                                          state="readonly", font=("Calibri", 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Calibri", 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo
        self.input_nombre_nuevo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=""),
                                        font=("Calibri", 13))
        self.input_nombre_nuevo.grid(row=3, column=1)

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=("Calibri", 13))
        self.etiqueta_precio_antiguo.grid(row=4, column=0)

        # Entry Precio antiguo
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Calibri", 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Calibri", 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo
        self.input_precio_nuevo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=""),
                                        font=("Calibri", 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoría antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoría antigua: ", font=("Calibri", 13))
        self.etiqueta_categoria_antigua.grid(row=6, column=0)

        # Entry Categoría antigua
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                             state="readonly", font=("Calibri", 13))
        self.input_categoria_antigua.grid(row=6, column=1)

        # Label Categoría nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=("Calibri", 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)

        # Entry Categoría nueva
        self.input_categoria_nueva = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=""),
                                           font=("Calibri", 13))
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=("Calibri", 13))
        self.etiqueta_stock_antiguo.grid(row=8, column=0)

        # Entry Stock antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                         state="readonly", font=("Calibri", 13))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=("Calibri", 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)

        # Entry Stock nuevo
        self.input_stock_nuevo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=""),
                                       font=("Calibri", 13))
        self.input_stock_nuevo.grid(row=9, column=1)

        # Botón Guardar cambios
        self.boton_actualizar = ttk.Button(frame_ep, text="Guardar cambios",
                                           command=lambda: self.actualizar_productos(
                                               self.input_nombre_nuevo.get(), self.input_nombre_antiguo.get(),
                                               self.input_precio_nuevo.get(), self.input_precio_antiguo.get(),
                                               self.input_categoria_nueva.get(), self.input_categoria_antigua.get(),
                                               self.input_stock_nuevo.get(), self.input_stock_antiguo.get()
                                           ))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio,
                             nueva_categoria, antigua_categoria, nuevo_stock, antiguo_stock):
        query = "UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?"
        parametros = (
            nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria,
            antiguo_stock)
        self.db_consulta(query, parametros)
        self.ventana_editar.destroy()
        self.mensaje["text"] = "El producto {} ha sido actualizado con éxito".format(antiguo_nombre)
        self.get_productos()


if __name__ == "__main__":
    root = Tk()
    app = Producto(root)
    root.mainloop()
