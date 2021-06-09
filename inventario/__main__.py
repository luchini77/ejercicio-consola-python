from .modelos.inventario import Inventario
from .modelos.producto import Producto
from .modelos.venta import Venta
import datetime
import os
import pickle


def mostrar_menu():
    """
    Muestra el menu de las operaciones disponibles.
    """
    print('1.- Registrar nuevo Producto.')
    print('2.- Vender un Producto.')
    print('3.- Buscar un producto por su codigo.')
    print('4.- Cambiar disponibilidad de un Producto.')
    print('5.- Productos vendidos en un rango de fechas.')
    print('6.- Ver top 5 de los productos mas vendidos.')
    print('7.- Ver top 5 de los productos menos vendidos.')
    print('0.- Salir.')


def capturar_entero(mensaje):
    """
    Captura un numero entero.Valida el ingreso de datos.

    Parametros:
    mensaje: Mensaje o texto personalizado a mostrar para la captura de un numero.

    Retorna: Numero entero, resultado de la captura.
    """

    while True:
        try:
            numero = int(input(f'{mensaje}: '))

            return numero

        except ValueError:
            print()
            print('Debe digitar un numero entero.')

        print()


def capturar_real(mensaje):
    """
    Captura un numero real.Valida el ingreso de datos.

    Parametros:
    mensaje: Mensaje o texto personalizado a mostrar para la captura de un numero.

    Retorna: Numero real, resultado de la captura.
    """

    while True:
        try:
            numero = float(input(f'{mensaje}: '))

            return numero

        except ValueError:
            print('Debe digitar un numero real.')

        print()


def capturar_cadena(mensaje):
    """
    Captura una cadena de caracteres.Valida el ingreso de datos.

    Parametros:
    mensaje: 
    Mensaje o texto personalizado a mostrar para la captura de una cadena de caracteres.

    Retorna: 
    Cadena de caracteres.
    """

    while True:

        cadena = input(f'{mensaje}: ').strip()

        if len(cadena):
            return cadena
        else:
            print('MENSAJE: Debe digitar una cadena de caracteres con un texto.')


        print()

def listar_productos(productos):
    """
    Muestra un listado de productos.

    Parametros:
    productos: Lista de productos.
    """
    for p in productos:
        print(f"{p.codigo} - {p.nombre}")


def continuar():
    """
    Muestra mensaje de continuación en la consola.
    """
    print()
    print('Presione Enter para continuar...', end='')
    input()
    print()


def cargar_inventario():
    while True:
        print('Desea cargar los datos del inventario y ventas desde el archivo?')
        print('1.- Si')
        print('2.- No')

        opcion = capturar_entero('Digite la opcion')

        if opcion == 1 or opcion == 2:
            break
    
    if opcion == 1:
        with open('inventario/inventario.pickle', 'rb') as f:
            inventario = pickle.load(f)

            return inventario

    return None


def guardar_datos(inventario):
    while True:
        print('Desea guardar los datos de productos y ventas desde el archivo?')
        print('1.- Si')
        print('2.- No')

        opcion = capturar_entero('Digite la opcion')

        if opcion == 1 or opcion == 2:
            break

    if opcion == 1:

        with open('inventario/inventario.pickle', 'wb') as f:

            pickle.dump(inventario, f)

        return True
    else:
        False



def main():
    """
    Punto de entrada a la aplicación.
    """

    inventario = Inventario()

    if os.path.isfile('inventario/inventario.pickle'):
        resultado = cargar_inventario()

        if resultado:
            inventario.productos = resultado['productos']
            inventario.ventas = resultado['ventas']


    while True:
        while True:
            try:
                mostrar_menu()
                print()
                opcion = int(input('Digite la opcion: '))
                print()
                if 0 <= opcion <= 7:
                    break
                else:
                    print('Mensaje: Debe digitar un numero mayor o igual a 0 y menor o igual a 7.')
            except ValueError:
                print('Debe digitar un valor entero valido.')

            continuar()

        if opcion == 0:
            break
        elif opcion == 1:
            while True:
                print()
                codigo_producto = capturar_entero('Digite el ID del nuevo producto')

                if codigo_producto > 0:
                    producto = inventario.buscar_productos(codigo_producto)

                    if producto is None:
                        break
                    else:
                        print()
                        print('MENSAJE: Ya existe un producto con el ID digitado.')
                else:
                    print()
                    print('MENSAJE: El ID del producto debe ser un número positivo.')

                continuar()
            
            print()
            nombre_producto = capturar_cadena('Digite el nombre del nuevo producto')

            while True:
                print()
                precio_producto = capturar_real('Digite el precio del nuevo producto')

                if precio_producto > 0:
                    break
                else:
                    print()
                    print('MENSAJE: Debe digitar un precio positivo para el producto.')

                continuar()
                
            
            while True:
                print()
                cantidad_producto = capturar_entero('Digite la cantidad del nuevo producto')

                if cantidad_producto > 0:
                    break
                else:
                    print()
                    print('MENSAJE: Debe digitar una cantidad positiva para el producto.')

                continuar()
                
            
            while True:
                print()
                print('1. Disponible')
                print('2. No Disponible')
                print()
                disponible = capturar_entero('Digite la opción para la disponibilidad del producto')

                if disponible == 1 or disponible == 2:
                    disponible = disponible == 1
                    break

                else:
                    print()
                    print('MENSAJE: La opción {} de disponibilidad no existe.'.format(disponible))
                
            
            nuevo_producto = Producto(codigo_producto,nombre_producto,precio_producto,cantidad_producto,disponible)
            
            inventario.registrar_productos(nuevo_producto)

            print()
            print('MENSAJE: El producto se ha creado de forma satisfactoria.')


        elif opcion == 2:

            if len(inventario.productos):
                while True:
                    listar_productos(inventario.productos)
                    print()
                    codigo_producto = capturar_entero('Digite el ID del producto')

                    producto = inventario.buscar_productos(codigo_producto)

                    if producto:
                        break
                    else:
                        print()
                        print('MENSAJE: Debe escribir un ID de producto existente.')


                while True:
                    print()
                    cantidad_producto = capturar_entero('Digite la cantidad del producto')

                    if cantidad_producto > 0:
                        if cantidad_producto <= producto.cantidad:
                            break
                        else:
                            print()
                            print('MENSAJE: No existe cantidad suficiente para la venta. Solo hay {} unidades.'.format(producto.cantidad))
                    else:
                        print()
                        print('MENSAJE:Debe digitar una cantidad positiva para este producto.')

                    continuar()

                nueva_venta = Venta(codigo_producto,cantidad_producto,producto.precio * cantidad_producto)
                
                print()

                inventario.realizar_venta(nueva_venta)
                print('Total: $%.2f' % (nueva_venta.total_sin_iva * 1.19))
                print()

                print('MENSAJE: La venta se a realizado de forma exitosa.')


            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )


        elif opcion == 3:
            if len(inventario.productos):
                while True:
                    listar_productos(inventario.productos)
                    codigo_producto = capturar_entero('Digite el ID del producto')

                    producto = inventario.buscar_productos(codigo_producto)

                    if producto:
                        break
                    else:
                        print()
                        print('MENSAJE: Debe escribir un ID de producto existente.')

                    continuar()

                print()
                inventario.mostrar_datos_producto(producto)

            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )


        elif opcion == 4:
            if len(inventario.productos):
                while True:
                    listar_productos(inventario.productos)
                    codigo_producto = capturar_entero('Digite el ID del producto')

                    producto = inventario.buscar_productos(codigo_producto)

                    if producto:
                        break
                    else:
                        print()
                        print('MENSAJE: Debe escribir un ID de producto existente.')

                    continuar()

                inventario.cambiar_estado_producto(producto)
                print()
                inventario.mostrar_datos_producto(producto)

            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )


        elif opcion == 5:
            if len(inventario.productos):
                if len(inventario.ventas):
                    while True:
                        try:
                            fecha_inicio = capturar_cadena('Digite la fecha de inicio (AAAA-MM-DD)')

                            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
                            break
                        except ValueError:
                            print()
                            print('ERROR: Debe digitar una fecha valida con el formato AAAA-MM-DD')

                        print()

                    while True:
                        try:
                            fecha_final = capturar_cadena('Digite la fecha final (AAAA-MM-DD)')

                            fecha_final = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')
                            break
                        except ValueError:
                            print()
                            print('ERROR: Debe digitar una fecha valida con el formato AAAA-MM-DD')

                        print()

                    ventas_rango = inventario.ventas_rango_fecha(fecha_inicio,fecha_final)

                    if len(ventas_rango):
                        for v in ventas_rango:
                            inventario.mostrar_datos_venta(v)
                            print()
                    else:
                        print()
                        print('MENSAJE: No hay ventas para el rango seleccionado.')

                else:
                    print()
                    print('MENSAJE: Aun no a efectuado ninguna venta.')

            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )


        elif opcion == 6:
            if len(inventario.productos):
                if len(inventario.ventas):
                    productos_vendidos = inventario.top_5_mas_vendidos()

                    for p in productos_vendidos:
                        inventario.mostrar_datos_venta_producto(p)
                        print()

                else:
                    print()
                    print('MENSAJE: Aun no a efectuado ninguna venta.')

            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )


        elif opcion == 7:
            if len(inventario.productos):
                if len(inventario.ventas):
                    productos_vendidos = inventario.top_5_menos_vendidos()

                    for p in productos_vendidos:
                        inventario.mostrar_datos_venta_producto(p)
                        print()

                else:
                    print()
                    print('MENSAJE: Aun no a efectuado ninguna venta.')

            else:
                print()
                print('MENSAJE: Aun no ha registrado productos.' )

        continuar()

    print()

    if len(inventario.productos):
        if guardar_datos(inventario):
            print('Los datos del inventario (productos y ventas) se han guardado en disco.')
        else:
            print('Ha omitido almacenar los datos en disco')
    print()

    print('El programa a finalizado.')




if __name__ == "__main__":
    main()
