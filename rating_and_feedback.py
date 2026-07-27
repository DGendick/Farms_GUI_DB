import json
import os
import csv_util
vis_divider = '======================'      #разделитель для меню
farm_data, header = csv_util.read_csv("export.csv")
json_data = {}
step = 0

def delete_comment(data, comment_pool):
    del_step = 0
    com_id = 0
    while True:
        match del_step:
            case 0:
                try:
                    com_id = int(input("Введите номер отзыва, который хотите удалить > "))
                    del_step = 1
                except:
                    print("Значение должно быть числовым")
            case 1:
                i = 0
                for i in range(len(comment_pool)):
                    if com_id == comment_pool[i][0]:
                        com_to_del = comment_pool[i]
                        break
                try:    
                    data[com_to_del[1]]["comment"].remove(com_to_del[2:])
                except:
                    print(f"Введен не существующий номер отзыва")
                return data

def rating_sort_descending(farms_pool):
    with open("market_rating_feedback.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    data = json_data.copy()
    printer =[]
    i = 0
   
    for i in range(len(farms_pool)):
        
        j = 0
        for j in range(len(data)):
            fmid_check = list(data.keys())[j]
            if farms_pool[i][0] == fmid_check:
                printer.append(list(data[farms_pool[i][0]].values()))

    #int(value) if value != '' else 0
    sorted_printer = printer.copy()
    temp = []
    for i in range(len(sorted_printer)):
        
        for j in range(0, len(sorted_printer)-i-1):
            rating1 = float(sorted_printer[j][3]) if sorted_printer[j][3] != '' else 0
            rating2 = float(sorted_printer[j+1][3]) if sorted_printer[j+1][3] != '' else 0
            if rating1 < rating2:
                temp = sorted_printer[j]
                sorted_printer[j] = sorted_printer[j+1]
                sorted_printer[j+1] = temp
                
    fmid_list = []
    for i in range(len(sorted_printer)):
        fmid_list.append(sorted_printer[i][0])
    return [], fmid_list, json_data

def rating_sort_ascending(farms_pool):
    with open("market_rating_feedback.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    data = json_data.copy()
    printer =[]
    i = 0
   
    for i in range(len(farms_pool)):
        
        j = 0
        for j in range(len(data)):
            fmid_check = list(data.keys())[j]
            if farms_pool[i][0] == fmid_check:
                printer.append(list(data[farms_pool[i][0]].values()))

    #int(value) if value != '' else 0
    sorted_printer = printer.copy()
    temp = []
    for i in range(len(sorted_printer)):
        
        for j in range(0, len(sorted_printer)-i-1):
            rating1 = float(sorted_printer[j][3]) if sorted_printer[j][3] != '' else 0
            rating2 = float(sorted_printer[j+1][3]) if sorted_printer[j+1][3] != '' else 0
            if rating1 > rating2:
                temp = sorted_printer[j]
                sorted_printer[j] = sorted_printer[j+1]
                sorted_printer[j+1] = temp
                
    fmid_list = []
    for i in range(len(sorted_printer)):
        fmid_list.append(sorted_printer[i][0])
    return [], fmid_list, json_data

def rating(fmid, curr_user,step):
        
    with open("market_rating_feedback.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    #json_data[str(fmid)].update(json_temp)
    match step:
        case 0: #показать рейтинг и комментарии
            print(f"==== {json_data[str(fmid)]["Market name"]} ====")
            if json_data[str(fmid)]["rating"] == '':
                print("====Нет оценок====")
            else:
                print(f"====Средняя оценка: {json_data[str(fmid)]["rating"]:.1f}/10.0====")

                
            

            if "comment" in json_data[str(fmid)]:
                for i in range(len(json_data[str(fmid)]["comment"])):
                    print(f"{json_data[str(fmid)]["comment"][i][0]}: {json_data[str(fmid)]["comment"][i][1]} |{json_data[str(fmid)]["comment"][i][2]:.1f}|")

            with open("market_rating_feedback.json", "w", encoding="utf-8") as file:
                json.dump(json_data, file)
        case 2: #Оставить отзыв
            comment =  str(input('Введите текст вашего отзыва > '))
            
            rating =  int(input('Введите оценку от 0 до 10 > '))
            
            if rating < 0:
                rating = 0
            elif rating > 10:
                rating = 10
            
            com_text = ([curr_user, comment, rating])
            json_data[str(fmid)]["comment"].append(com_text)
            mean_rating = 0
            if json_data[str(fmid)]["comment"]:
                for i in range(len(json_data[str(fmid)]["comment"])):
                    mean_rating += json_data[str(fmid)]["comment"][i][2]

            else:
                mean_rating = json_data[str(fmid)]["comment"][i][2]
            
            mean_rating = mean_rating / len(json_data[str(fmid)]["comment"])           
            json_data[str(fmid)]["rating"] = mean_rating

            with open("market_rating_feedback.json", "w", encoding="utf-8") as file:
                json.dump(json_data, file)
        case 3:#Удалить отзыв
            printer = []
            index = 1
            for id in json_data.values():
                for comment in id["comment"]:
                    if comment[0] == curr_user:
                        printer_temp = comment.copy()
                        printer_temp.insert(0,id["FMID"])
                        printer_temp.insert(0,index)
                        printer.append(printer_temp)
                        
                        
                        index += 1
            print_market = ''
            i = 0
            print("==== Ваши отзывы ====")
            for i in range(len(printer)):
                if print_market != json_data[printer[i][1]]["Market name"]:
                    print(f"==== {json_data[printer[i][1]]["Market name"]} ====")
                    print_market = json_data[printer[i][1]]["Market name"]
                    print(f"{printer[i][0]}. {printer[i][2]}: {printer[i][3]} |{printer[i][4]:.1f}|")
                else:
                    print(f"{printer[i][0]}. {printer[i][2]}: {printer[i][3]} |{printer[i][4]:.1f}|")

            while True:
                print(vis_divider)
                print("1. Удалить отзыв")
                print("0. Выход")
                print(vis_divider)

                cmd = input("> ")
                
                if cmd == "1":
                    json_data = delete_comment(json_data,printer)
                    with open("market_rating_feedback.json", "w", encoding="utf-8") as file:
                        json.dump(json_data, file)
                    break
                elif cmd == "0":
                    break
                else:
                    print(f"Ошибка! {cmd} - не является командой")




if os.path.exists("market_rating_feedback.json"):
    #rating(fmid)
    ...
else:
    for i in range(len(farm_data)):
        json_temp = {"FMID": farm_data[i][0], 
                    "Market name": farm_data[i][1],
                    "comment":[],
                    "rating": ''
                    }
        json_data[farm_data[i][0]] = json_temp
    with open("market_rating_feedback.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file)

