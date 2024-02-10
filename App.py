import tkinter as tk

# Primero, definimos la función sum_digits para sumar los dígitos de un número.
def sum_digits(number):
    return sum(int(digit) for digit in str(number))


# Definimos la función letter_to_value para convertir letras a su valor numérico correspondiente (A=10, ..., Z=35).
def letter_to_value(letter):
    return ord(letter.upper()) - 55


# Definimos la función isin para validar un código ISIN.
def isin(isin):

    numeric_values = []  # Para almacenar los valores numéricos del codigo ISIN

    # Convertir cada caracter del ISIN a su valor numérico y aplicar la regla de duplicar cada segundo número empezando desde la derecha.
    for char in isin:
        if char.isdigit():
            numeric_values.append(int(char))
        else:   
            numeric_value = letter_to_value(char)
        
            # Aquí nos aseguramos de descomponer el valor numérico en sus dígitos individuales si es mayor a 9
            if numeric_value > 9:
                numeric_values.extend(divmod(numeric_value, 10))
            else:
                numeric_values.append(numeric_value)

    # Duplicar cada segundo número empezando desde la derecha y suma los dígitos de los números mayores a 9
    double_numeric_values = [sum_digits(numeric_values[i] * 2) if i % 2 == 0 and numeric_values[i] * 2 > 9 else
                       numeric_values[i] * 2 if i % 2 == 0 else numeric_values[i] for i in range(len(numeric_values))]
    
    # Sumar todos los valores numéricos
    numeric_value = sum(double_numeric_values)

    is_valid_isin = numeric_value % 10 == 0

    # Si la suma total no es un múltiplo de 10, buscar la cifra de control.
    control_digit = None
    if not is_valid_isin:
        for x in range(10):
            if (numeric_value + x) % 10 == 0:
                control_digit = x
                break

    return numeric_values, double_numeric_values, numeric_value, is_valid_isin, control_digit


def on_submit():
    # Obtener el ISIN del campo de entrada y calcular los resultados
    isin_code = entry.get()
    numeric_values, double_numeric_values, numeric_value, validate_isin, control_digit = isin(isin_code)
    
    # Mostrar los resultados en la interfaz
    result_text.set(
        f"ISIN: {isin_code}\n"
        f"Valor numérico de la ISIN: {numeric_values}\n"
        f"Valor calculado numérico de la ISIN: {double_numeric_values}\n"
        f"Suma de los valores numéricos de la ISIN es: {numeric_value}\n"
        f"Validación de ISIN: {'Válido' if validate_isin else 'No válido'}\n"
        f"Cifra de control necesaria (si aplica): {control_digit if control_digit is not None else 'N/A'}"
    )

# Configurar la ventana principal de Tkinter
root = tk.Tk()
root.title("Validador de ISIN")

# Configurar el texto de resultados
result_text = tk.StringVar()

# Crear y colocar los widgets
label = tk.Label(root, text="Ingrese el código ISIN:")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="Validar", command=on_submit)
submit_button.pack()

result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT)
result_label.pack()

# Iniciar el bucle principal de Tkinter
root.mainloop()
