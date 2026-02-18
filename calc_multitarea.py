"""
    Calculadora versátil para diferentes operaciones financieras.
    Modos disponibles: 'descuento' (descuento), 'impuesto' (impuestos), 'propina' (propina).
    La función valida los tipos de entrada y los rangos adecuados para cada modo.
    Ejemplos de uso al final del código.
"""
from datetime import datetime
import os

def aplicar_descuento(precio, descuento):
    """
    Aplica un descuento a un precio dado.
    Retorna el precio final o un mensaje de error si los parámetros no son válidos.
    """
    if not isinstance(precio, (int, float)):
        return "El precio debe ser un número"
    if not isinstance(descuento, (int, float)):
        return "El descuento debe ser un número"
    if precio <= 0:
        return "El precio debe ser mayor que 0"
    if not 0 <= descuento <= 100:
        return "El descuento debe estar entre 0 y 100"
    return round(precio * (1 - descuento / 100), 2)

def aplicar_impuesto(monto_base, tasa_impuesto):
    """
    Calcula el impuesto sobre un monto base.
    Retorna un diccionario con base, impuesto y total, o un mensaje de error.
    """
    if not isinstance(monto_base, (int, float)):
        return "El monto base debe ser un número"
    if not isinstance(tasa_impuesto, (int, float)):
        return "El porcentaje debe ser un número"
    if monto_base < 0:
        return "El monto base no puede ser negativo"
    valor_impuesto = monto_base * (tasa_impuesto / 100)
    total = monto_base + valor_impuesto
    return {"base": monto_base, "monto_impuesto": round(valor_impuesto, 2), "total": round(total, 2)}

def aplicar_propina(cuenta, porcentaje_propina):
    """
    Calcula la propina sobre una cuenta.
    Retorna un diccionario con cuenta, propina y total, o un mensaje de error.
    """
    if not isinstance(cuenta, (int, float)):
        return "El monto de la cuenta debe ser un número"
    if not isinstance(porcentaje_propina, (int, float)):
        return "El porcentaje debe ser un número"
    if cuenta <= 0:
        return "El monto de la cuenta debe ser mayor que 0"
    if not 0 <= porcentaje_propina <= 100:
        return "La propina debe estar entre 0 y 100"
    valor_propina = cuenta * (porcentaje_propina / 100)
    total = cuenta + valor_propina
    return {"cuenta": cuenta, "monto_propina": round(valor_propina, 2), "total": round(total, 2)}

def calculadora_universal(monto_calc, porcentaje_calc, modo_operacion="descuento"):
    """
    Calculadora financiera universal.
    Retorna el resultado según el modo: descuento, impuesto o propina.
    """
    if modo_operacion == "descuento":
        return aplicar_descuento(monto_calc, porcentaje_calc)
    elif modo_operacion == "impuesto":
        return aplicar_impuesto(monto_calc, porcentaje_calc)
    elif modo_operacion == "propina":
        return aplicar_propina(monto_calc, porcentaje_calc)
    else:
        return "Modo inválido. Elige 'descuento', 'impuesto' o 'propina'."

# --- HISTORIAL ---
archivo_historial = "historial_calculadora.txt"

def cargar_historial():
    """
    Carga el historial desde archivo.
    Retorna una lista de registros.
    """
    if os.path.exists(archivo_historial):
        with open(archivo_historial, "r", encoding="utf-8") as archivo:
            return [line.strip().split(" ", 1)[1] if line.strip()[0].isdigit() else line.strip()
                    for line in archivo.readlines() if line.strip() and not line.startswith("---")]
    return []

def guardar_historial(historial_datos):
    """
    Guarda el historial en archivo con un máximo de 8 registros.
    """
    with open(archivo_historial, "w", encoding="utf-8") as archivo:
        archivo.write("--- Historial de cálculos (máx. 8) ---\n")
        for idx, entrada in enumerate(historial_datos, 1):
            archivo.write(f"{idx}. {entrada}\n")

# --- MENÚ ---
while True:
    historial = cargar_historial()
    print("\nBienvenido a la Calculadora Financiera Universal")
    print("Seleccione una opción:")
    print("1. Descuento")
    print("2. Impuesto")
    print("3. Propina")
    print("4. Limpiar historial")
    print("5. Salir")

    opcion = input("Ingrese el número de la opción: ")

    if opcion == "5":
        print("Programa cerrado. ¡Hasta luego!")
        break

    if opcion == "4":
        historial = []
        guardar_historial(historial)
        print("✅ Historial limpiado exitosamente. El archivo está vacío.")
        continue

    if opcion == "1":
        modo = "DESCUENTO"
    elif opcion == "2":
        modo = "IMPUESTO"
    elif opcion == "3":
        modo = "PROPINA"
    else:
        print("Opción inválida, intente de nuevo.")
        continue

    while True:
        try:
            monto = float(input("Ingrese el monto base: "))
            break
        except ValueError:
            print("Error: El monto debe ser un número. Intente de nuevo.")

    while True:
        try:
            porcentaje = float(input("Ingrese el porcentaje (%): "))
            break
        except ValueError:
            print("Error: El porcentaje debe ser un número. Intente de nuevo.")

    resultado = calculadora_universal(monto, porcentaje, modo.lower())
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if modo == "DESCUENTO" and isinstance(resultado, (int, float)):
        print(f"Precio base: {monto:.2f}")
        print(f"Descuento aplicado: {porcentaje:.2f}%")
        print(f"Precio final después del descuento: {resultado:.2f}")
        registro = f"[{fecha_hora}] {modo} | Base: {monto:.2f} | {porcentaje:.2f}% | Final: {resultado:.2f}"
    elif modo == "IMPUESTO" and isinstance(resultado, dict):
        print(f"Base: {resultado['base']:.2f}")
        print(f"Impuesto aplicado ({porcentaje:.2f}%): {resultado['monto_impuesto']:.2f}")
        print(f"Total con impuesto: {resultado['total']:.2f}")
        registro = f"[{fecha_hora}] {modo} | Base: {resultado['base']:.2f} | {porcentaje:.2f}% | Total: {resultado['total']:.2f}"
    elif modo == "PROPINA" and isinstance(resultado, dict):
        print(f"Cuenta: {resultado['cuenta']:.2f}")
        print(f"Propina aplicada ({porcentaje:.2f}%): {resultado['monto_propina']:.2f}")
        print(f"Total con propina: {resultado['total']:.2f}")
        registro = f"[{fecha_hora}] {modo} | Cuenta: {resultado['cuenta']:.2f} | {porcentaje:.2f}% | Total: {resultado['total']:.2f}"
    else:
        registro = f"[{fecha_hora}] RESULTADO INVÁLIDO"

    historial.append(registro)
    if len(historial) > 8:
        historial = historial[-8:]
    guardar_historial(historial)

    ver_historial = input("¿Desea consultar el historial de cálculos? (s/n): ")
    if ver_historial.lower() == "s":
        if not historial:
            print("\n--- Historial vacío, no hay cálculos guardados ---")
        else:
            print("\n--- Historial de cálculos (máx. 8) ---")
            for i, registro in enumerate(historial, 1):
                print(f"{i}. {registro}")
