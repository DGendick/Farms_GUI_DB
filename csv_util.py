def read_csv(filename):
    i = 0
    header = []
    farm_org_data = []
    farm_data = []
   
    for line in open(filename).read().split("\n"):
        # --- ПРОПУСКАЕМ ПУСТЫЕ СТРОКИ ---
        if not line.strip():
            continue
        # --- КОНЕЦ ПРОВЕРКИ ---
        
        # Парсим строку с учетом кавычек
        m = []
        current = ''
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                m.append(current)
                current = ''
            else:
                current += char
        m.append(current)
        
        i += 1
        
        if i == 1:
            # Заголовок
            for val in m:
                header.append(val)
        else:
            farm_org_data = []
            
            # Идем по всем колонкам заголовка
            for idx in range(0, len(header)):
                # Если в m есть значение для этого индекса - берем его
                if idx < len(m):
                    val = m[idx]
                else:
                    val = ''
                
                # Для координат x и y конвертируем в числа
                if header[idx] in ("x", "y"):
                    if val.strip() != "":
                        val = float(val)
                    else:
                        val = None
                
                farm_org_data.append(val)
            farm_data.append(farm_org_data)
    
    return farm_data, header


# Загружаем данные
""" farm_data = read_csv("export.csv")
print(type(farm_data))
print(f"Загружено строк: {len(farm_data)}")

# Сохраняем в файл
with open('output.csv', 'w', encoding='utf-8') as file:
    for row in farm_data:
        file.write(','.join(map(str, row)) + '\n') """
#print(f"File read successfully\n")