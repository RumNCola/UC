import pyperclip
usuario = input('Ingrese su nombre: ')

def mensaje():
    print()
    print('[0] Mensaje Insistencia')
    print('[1] Mensaje Breve')
    print('[2] Mensaje ')
    print('[3] Menu Mail')
    print()
    opcion = int(input('Ingrese opcion: '))
    if opcion == 1:
        print()
        nombre = input('Nombre receptor: ')
        print()
        empresa = input('Nombre empresa: ')
        print('================================ \n')
        texto = (
        f"Hola {nombre}, ¿cómo estás?\n\n"
        f"Soy {usuario} de eVink, empresa de eficiencia energética dedicada a generar ahorros en la factura eléctrica de sus clientes. Me gustaría saber, ¿quién es la persona encargada del tema eléctrico en {empresa}?\n\n"
        f"Quedo atento. ¡Muchas gracias!")

        print(texto)
        pyperclip.copy(texto)
        print('================================ \n')
        return mensaje()

    elif opcion == 0:
        nombre = input('Nombre receptor: ')
        print()
        empresa = input('Empresa: ')
        texto = (f'Hola {nombre}, quisiera comentarte que nuestra asesoría energética ha generado un ahorro del 18% en costos eléctricos para clientes industriales y agrícolas, optimizando el consumo y la contratación de suministro. \n'
                 f'¿Sabes quién es la persona encargada de este tema en {empresa}? Me encantaría ofrecerle una evaluación inicial para conseguir ahorros similares. \n'
                 f'¡Quedo atento!')
        pyperclip.copy(texto)
        print(texto)
        print('================================ \n')
        return mensaje()

    elif opcion == 2:
        print()
        nombre = input('Nombre receptor: ')
        print()
        empresa = input('Nombre empresa: ')
        print()
        print('================================')
        texto = (f"Hola, {nombre}. ¿Cómo estás?\n\n"
                f"Soy {usuario} de eVink, una empresa de eficiencia energética enfocada en generar ahorros en la factura eléctrica de diversas industrias.\n\n"
                f"Quisiera saber, ¿quién es la persona encargada de este tema en {empresa}? Mi intención es ponerla en contacto con nuestro asesor para que puedan explorar soluciones y coordinar una evaluación inicial.\n\n"
                f"Quedo atento. ¡Muchas gracias!")
        pyperclip.copy(texto)
        print(texto)
        print('================================')
        return mensaje()
    elif opcion == 3:
        return menu_mail()
    else:
        print('Ingrese opción válida: \n')
        return mensaje()
                 
def menu_mail():
    print('[1] Mail Referencia')
    print('[2] Mail Directo')
    print('[3] Volver')
    print()

    opcion = int(input('Ingrese opcion: '))

    if opcion == 1:
        nombre = input('Nombre receptor: ')
        print()
        referencia = input('nombre referencia: ')
        print()
        empresa = input('empresa: ')
        bloque1 = input('Bloque 1 reunion: ')
        print()
        bloque2 = input('Bloque 2 reunion: ')
        print()
        texto = (f'Estimado {nombre}, espero que estés muy bien. \n'
f''
f'Soy {usuario} de eVink y {referencia} me pidió que te contactara ya que eres la persona encargada de ver el tema de ahorro energético en {empresa}. \n' 
f''
f'En eVink entregamos servicios de asesorías y monitoreo energético con el propósito de reducir costos en la factura de electricidad.'
f''
f'¿Tienes disponibilidad para conversar brevemente de esto el {bloque1} o el {bloque2}?  \nSi te acomoda en otro momento por favor házmelo saber. \n')
        pyperclip.copy(texto)
        print(texto)
        return mensaje()

    elif opcion == 2:
        nombre = input('Nombre receptor: ')
        print()
        bloque1 = input('Bloque 1 reunion: ')
        print()
        bloque2 = input('Bloque 2 reunion: ')
        print()
        texto = (f'Hola {nombre}, espero que estés muy bien. \n'
f''
f'Soy {usuario} de eVink y recientemente hablamos por Linkedln para ponerte en contacto con nuestro asesor y conversar el tema del ahorro y la eficiencia energética de tu planta. Nuestro foco son las industrias productivas como la tuya, en las cuales a través de la gestión eficiente de los consumos logramos generar ahorros en las facturas. \n'
f''
f'¿Tendrías disponibilidad para agendar una breve reunión el {bloque1} o el {bloque2}? \n'
f''
f'Si te acomoda otro horario durante la semana queda atento.')
        pyperclip.copy(texto)
        print(texto)
        return mensaje()
    
    elif opcion == 3:
        return mensaje()
    
    else:
        return menu_mail()
    
mensaje()