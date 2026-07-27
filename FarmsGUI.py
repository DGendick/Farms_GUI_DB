import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import math
import zip_util
from authenticationOOP import User
from tkcalendar import DateEntry
from controllers import MarketController

class FarmsApp:
    def __init__(self, root):
        self.current_user = None
        self.current_city = None
        self.current_state = None
        self.controller = MarketController()

        self.connection = sqlite3.connect("C:\PythonBasic\LR7_3NF_DB\LR7")
        self.cursor = self.connection.cursor()

        self.root = root
        self.root.title("Markets App")
        self.root.geometry("500x400")
        
        # Центрируем окно на экране
        self.center_window()
        
        # Создаем главный контейнер с отступами
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(
            fill=tk.X,
            side=tk.TOP,
            pady=5
        )
        # Пользователь
        self.user_label = ttk.Label(
            top_frame,
            text="Guest",
            font=("Arial", 10)
        )

        self.user_label.pack(
            side=tk.LEFT,
            padx = 10
        )

        self.unit_button = tk.Button(
            top_frame,
            text="Miles",
            command=self.change_distance_unit,
            bg = "white",
            width = 10
        )
        self.unit_button.pack(side=tk.RIGHT,
            padx = 10)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="Farm markets App",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(0, 0))
        
        # Подзаголовок
        subtitle_label = ttk.Label(
            main_frame,
            text="Choose action:",
            font=("Arial", 12)
        )
        subtitle_label.pack(pady=(0, 0))

        
        # Создаем фрейм для кнопок (чтобы они были ровно по центру)
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(expand=True)
        
        # Стиль для кнопок
        style = ttk.Style()
        style.configure("Menu.TButton", font=("Arial", 12), padding=5)
        
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(expand=True)

        self.create_main_buttons()
        
        # Статусная строка внизу
        self.status_var = tk.StringVar()
        self.status_var.set("Ready 4 search!")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.GROOVE,
            anchor=tk.E,
            padding=(5, 2)
        )
        status_label.pack(fill=tk.X, pady=(20, 0))

    def change_distance_unit(self):

        if self.controller.distance_unit == "miles":
            self.unit_button.config(bg="green",text= "KM")
            self.controller.distance_unit = "km"

        else:
            self.unit_button.config(bg="white",text="Miles")
            self.controller.distance_unit = "miles"

    def update_user_label(self):

        if self.current_user:

            self.user_label.config(
                text=f"User: {self.current_user.username}"
            )

        else:

            self.user_label.config(
                text="Guest"
            )    

    def create_main_buttons(self):

        # очищаем текущее содержимое
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.markets_btn = ttk.Button(
            self.button_frame,
            text="Show all Markets",
            command=self.open_markets,
            style="Menu.TButton",
            width=15
        )
        self.markets_btn.pack(pady=0)

        self.search_btn = ttk.Button(
            self.button_frame,
            text="Search market",
            command=self.open_search,
            style="Menu.TButton",
            width=15
        )
        self.search_btn.pack(pady=0)

        self.login_btn = ttk.Button(
            self.button_frame,
            text="Login",
            style="Menu.TButton",
            command=self.open_login,
            width=15
        )

        self.login_btn.pack(pady=0)


        self.register_btn = ttk.Button(
            self.button_frame,
            text="Register",
            style="Menu.TButton",
            command=self.open_register,
            width=15
        )

        self.register_btn.pack(pady=0)

        self.logout_btn = ttk.Button(
            self.button_frame,
            text="Logout",
            command=self.logout,
            style="Menu.TButton",
            width=15
        )

        self.logout_btn.pack(pady=0)
        
        self.update_menu()


    def logout(self):

        if self.current_user is None:

            messagebox.showinfo(
                "Logout",
                "No user logged in"
            )

            return

        self.current_user = None

        self.status_var.set(
            "Ready 4 search!"
        )

        messagebox.showinfo(
            "Logout",
            "You have been logged out"
        )
        self.update_user_label()
        self.update_menu()

    def update_menu(self):
        if self.current_user:

            self.login_btn.config(
                state="disabled"
            )

            self.logout_btn.config(
                state="normal"
            )

        else:

            self.login_btn.config(
                state="normal"
            )

            self.logout_btn.config(
                state="disabled"
            )

    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def auto_resize_columns(self, tree, columns):

        for column in columns:

            max_width = len(column)

            for item in tree.get_children():

                values = tree.item(item)["values"]

                index = columns.index(column)

                text = str(values[index])

                max_width = max(
                    max_width,
                    len(text)
                )

            tree.column(
                column,
                width=min(max_width * 8, 150)
            )


    def open_markets(self):
        #Обработчик кнопки All Markets
        self.status_var.set("Open Market list...")
        markets_window = tk.Toplevel(self.root)
        markets_window.title("All Markets")
        markets_window.geometry("600x400")
        
        self.cursor.execute("""SELECT 
                                m.*,
                                a.State ,
                                a.city ,
                                a.street,
                                a.County,
                                a.zip,
                                GROUP_CONCAT(p.Product, ', ') AS Products    
                            FROM Markets m
                            JOIN Address a 
                            ON a.FMID = m.FMID 
                            JOIN Products mp
                            ON m.FMID = mp.FMID
                            JOIN Product p
                            ON mp.ProductID = p.ProductID
                            GROUP BY m.FMID;""")
        markets  = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]

    # Создаем таблицу
        table_frame = ttk.Frame(
            markets_window,
            padding=5
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=tree.yview
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        tree.configure(
            yscrollcommand=vertical_scroll.set
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=tree.xview
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        tree.configure(
            xscrollcommand=horizontal_scroll.set
        )       

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        # Создаем заголовки
        for column in columns:
            tree.heading(
                column,
                text=column
            )

        # Заполняем таблицу
        for market in markets:
            tree.insert(
                "",
                tk.END,
                values=market
            )
        
        tree.bind(
        "<Double-1>",
        lambda event: self.show_reviews(tree)
        )

        self.auto_resize_columns(tree, columns)
    
    def load_ratings(self):

        with open(
            "market_rating_feedback.json",
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def open_search(self):
        #Выбираем тип поиска
        self.status_var.set("Choose search type")

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        city_btn = ttk.Button(
            self.button_frame,
            style="Menu.TButton",
            text="City",
            width=15,
            command=self.search_city
        )
        city_btn.pack(pady=0)

        state_btn = ttk.Button(
            self.button_frame,
            style="Menu.TButton",
            text="State",
            command=self.search_state,
            width=15
        )
        state_btn.pack(pady=0)

        zip_btn = ttk.Button(
            self.button_frame,
            style="Menu.TButton",
            text="ZIP",
            command=self.open_zip_search,
            width=15
        )
        zip_btn.pack(pady=0)

        back_btn = ttk.Button(
            self.button_frame,
            style="Menu.TButton",
            text="Back",
            command=self.create_main_buttons,
            width=15
        )
        back_btn.pack(expand=True,pady=0)
   
    def get_distance(self, lat1, lon1, lat2, lon2):

        R = 3958.8  
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2)**2
            +
            math.cos(lat1)
            *
            math.cos(lat2)
            *
            math.sin(dlon / 2)**2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1-a)
        )
        return R * c

    def get_zip_coordinates(self, zip_code):

        for z in zip_codes:

            if z[0] == zip_code:

                return (
                    float(z[1]), # latitude
                    float(z[2])  # longitude
                )


        return None

    def find_fmid_radius(self, zip_code, radius):


        zip_coord = self.get_zip_coordinates(zip_code)


        if zip_coord is None:
            return []


        zip_lat = zip_coord[0]
        zip_lon = zip_coord[1]


        self.cursor.execute(
            """
            SELECT 
                FMID,
                x,
                y
            FROM Location
            """
        )

        locations = self.cursor.fetchall()

        result = []

        for loc in locations:

            fmid = loc[0]

            if loc[1] == "" or loc[2] == "":
                continue

            market_lon = float(loc[1])
            market_lat = float(loc[2])

            distance = self.get_distance(
                zip_lat,
                zip_lon,
                market_lat,
                market_lon
            )
            # MVC расстояние
            distance = self.controller.convert_distance(
                distance
            )

            if distance <= radius:

                result.append((fmid, distance))

        return result
    
    def open_zip_search(self):

        self.zip_window = tk.Toplevel(
            self.root
        )

        self.zip_window.title(
            "Search by ZIP"
        )

        self.zip_window.geometry(
            "300x250"
        )

        ttk.Label(
            self.zip_window,
            text="ZIP code"
        ).pack(
            pady=5
        )

        self.zip_entry = ttk.Entry(
            self.zip_window
        )

        self.zip_entry.pack()

        ttk.Label(
            self.zip_window,
            text="Radius (miles)"
        ).pack(
            pady=5
        )

        self.radius_entry = ttk.Entry(
            self.zip_window
        )

        self.radius_entry.pack()

        ttk.Button(
            self.zip_window,
            text="Search",
            command=self.search_by_zip_radius
        ).pack(
            pady=15
        )
    
    def search_by_zip_radius(self):

        zip_code = self.zip_entry.get()

        radius = self.radius_entry.get()

        if not zip_code or not radius:

            messagebox.showerror(
                "Error",
                "Enter ZIP and radius"
            )

            return

        try:

            radius = float(radius)

        except:

            messagebox.showerror(
                "Error",
                "Radius must be number"
            )

            return

        markets_distance  = self.find_fmid_radius(
            zip_code,
            radius
        )

        fmids = []

        for item in markets_distance:
            fmids.append(item[0])

        if not fmids:
            messagebox.showinfo(
                "Search",
                "Markets not found"
            )
            return

        markets = self.get_markets_by_fmid(
            fmids
        )

        ratings = self.load_ratings()

        result = []


        for market in markets:

            fmid = str(market[0])


            rating = ratings[fmid]["rating"]


            # ищем расстояние
            distance = ""

            for item in markets_distance:

                if str(item[0]) == fmid:
                    distance = item[1]
                    break


            market = list(market)


            market.append(
                rating if rating != "" else "No rating"
            )


            market.append(
                round(distance, 2)
            )


            result.append(market)


        self.show_markets_table(result,show_distance=True)


    def get_markets_by_fmid(self, fmids):

        placeholders = ",".join(
            "?" * len(fmids)
        )

        query = f"""
            SELECT 
                m.*,
                a.State,
                a.city,
                a.street,
                a.County,
                a.zip,
                GROUP_CONCAT(
                    p.Product,
                    ', '
                ) AS Products

            FROM Markets m

            JOIN Address a
            ON a.FMID = m.FMID

            JOIN Products mp
            ON m.FMID = mp.FMID

            JOIN Product p
            ON mp.ProductID = p.ProductID


            WHERE m.FMID IN ({placeholders})

            GROUP BY m.FMID
            ORDER BY a.city
        """


        self.cursor.execute(
            query,
            fmids
        )


        return self.cursor.fetchall()

    def search_state(self):
            self.status_var.set("Search by state")
            # очищаем кнопки
            for widget in self.button_frame.winfo_children():
                widget.destroy()


            label = ttk.Label(
                self.button_frame,
                text="Enter state:"
            )

            label.pack(pady=5)


            self.state_entry = ttk.Entry(
                self.button_frame,
                width=20
            )

            self.state_entry.pack(pady=5)


            search_btn = ttk.Button(
                self.button_frame,
                text="Search",
                style="Menu.TButton",
                command=self.find_by_state
            )

            search_btn.pack(pady=5)


            back_btn = ttk.Button(
                self.button_frame,
                text="Back",
                style="Menu.TButton",
                command=self.open_search
            )

            back_btn.pack(pady=5)

    def find_by_state(self):
            
            if self.state_entry.get():
                self.current_state = self.state_entry.get().lower()

            state = self.current_state


            self.cursor.execute(
                """SELECT 
                    m.*,
                    a.State ,
                    a.city ,
                    a.street,
                    a.County,
                    a.zip,
                    GROUP_CONCAT(p.Product, ', ') AS Products    
                FROM Markets m
                JOIN Address a 
                ON a.FMID = m.FMID 
                JOIN Products mp
                ON m.FMID = mp.FMID
                JOIN Product p
                ON mp.ProductID = p.ProductID
                WHERE  LOWER(a.State) = ?
                GROUP BY m.FMID
                ORDER BY a.State;""",
                (state,)
            )


            markets = self.cursor.fetchall()

            #self.show_markets_table(markets)

            ratings = self.load_ratings()


            result = []

            for market in markets:

                fmid = str(market[0])

                rating = ratings[fmid]["rating"]

                market = list(market)

                market.append(
                    rating if rating != "" else "No rating"
                )

                result.append(market)

            self.show_markets_table(result)

    def search_city(self):
        self.status_var.set("Search by city")
        # очищаем кнопки
        for widget in self.button_frame.winfo_children():
            widget.destroy()


        label = ttk.Label(
            self.button_frame,
            text="Enter city:"
        )

        label.pack(pady=5)


        self.city_entry = ttk.Entry(
            self.button_frame,
            width=20
        )

        self.city_entry.pack(pady=5)


        search_btn = ttk.Button(
            self.button_frame,
            text="Search",
            style="Menu.TButton",
            command=self.find_by_city
        )

        search_btn.pack(pady=5)


        back_btn = ttk.Button(
            self.button_frame,
            text="Back",
            style="Menu.TButton",
            command=self.open_search
        )

        back_btn.pack(pady=5)

    def find_by_city(self):
        
        if self.city_entry.get():
            self.current_city = self.city_entry.get().lower()

        city = self.current_city


        self.cursor.execute(
            """SELECT 
                m.*,
                a.State ,
                a.city ,
                a.street,
                a.County,
                a.zip,
                GROUP_CONCAT(p.Product, ', ') AS Products    
            FROM Markets m
            JOIN Address a 
            ON a.FMID = m.FMID 
            JOIN Products mp
            ON m.FMID = mp.FMID
            JOIN Product p
            ON mp.ProductID = p.ProductID
            WHERE  LOWER(a.city) = ?
            GROUP BY m.FMID
            ORDER BY a.city;""",
            (city,)
        )


        markets = self.cursor.fetchall()

        #self.show_markets_table(markets)

        ratings = self.load_ratings()


        result = []

        for market in markets:

            fmid = str(market[0])

            rating = ratings[fmid]["rating"]

            market = list(market)

            market.append(
                rating if rating != "" else "No rating"
            )

            result.append(market)

        self.show_markets_table(result)

    def sort_treeview(self, tree, column, reverse):

        data = []

        for item in tree.get_children():
            value = tree.set(item, column)
            data.append((value, item))


        def sort_key(item):

            value = item[0]

            # No rating всегда в конец
            if value == "No rating" or value == "":
                return (1, 0)

            try:
                return (0, float(value))

            except ValueError:
                return (0, value.lower())


        if reverse:
            # сортируем только реальные значения в обратную сторону
            rated = []
            no_rating = []

            for item in data:
                if item[0] == "No rating" or item[0] == "":
                    no_rating.append(item)
                else:
                    rated.append(item)

            rated.sort(
                key=sort_key,
                reverse=True
            )

            data = rated + no_rating

        else:
            data.sort(
                key=sort_key
            )


        for index, (_, item) in enumerate(data):
            tree.move(
                item,
                "",
                index
            )


        tree.heading(
            column,
            command=lambda:
                self.sort_treeview(
                    tree,
                    column,
                    not reverse
                )
        )

    def show_markets_table(self, markets,  show_distance=False):

         # если данных нет
        if not markets:
            messagebox.showinfo(
                "Search",
                "Markets not found"
            )
            return
        
        if hasattr(self, "result_window"):
            self.result_window.destroy()

        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Search result")
        self.result_window.geometry("600x400")     

        # получаем названия столбцов
        columns = [
            description[0]
            for description in self.cursor.description
        ]

        columns.append("Rating")
        if show_distance:
            if self.controller.distance_unit == "km":
                columns.append(
                    "Distance, km"
                )

            else:

                columns.append(
                    "Distance, miles"
                )

        # создаем Frame
        table_frame = ttk.Frame(
            self.result_window,
            padding=5
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        # создаем таблицу
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # вертикальный скролл
        y_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=tree.yview
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # горизонтальный скролл
        x_scroll = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=tree.xview
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        # заголовки
        for column in columns:

            tree.heading(
                column,
                text=column,
                command=lambda col=column:
                    self.sort_treeview(
                        tree,
                        col,
                        False
                    )
            )

        # данные
        for market in markets:
            tree.insert(
                "",
                tk.END,
                values=market
            )

        # растягивание
        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        tree.bind(
                "<Double-1>",
                lambda event: self.show_reviews(tree)
        )

        ttk.Button(
                self.result_window,
                text="Refresh",
                command=self.find_by_city
            ).pack(side="left", pady=5)
        

        
        # автоширина
        self.auto_resize_columns(tree, columns)


    def show_reviews(self, tree):

        selected = tree.selection()

        if not selected:
            return

        item = tree.item(selected[0])

        values = item["values"]

        # FMID у нас первый столбец
        fmid = str(values[0])

        with open(
            "market_rating_feedback.json",
            "r",
            encoding="utf-8"
        ) as file:
            ratings = json.load(file)

        reviews = ratings[fmid]["comment"]

        review_window = tk.Toplevel(self.root)
        review_window.title(
            f"Reviews {fmid}"
        )
        review_window.geometry(
            "600x300"
        )

        columns = (
            "User",
            "Comment",
            "Rating"
        )

        review_table = ttk.Treeview(
            review_window,
            columns=columns,
            show="headings"
        )

        review_table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        for col in columns:
            review_table.heading(
                col,
                text=col
            )

        for review in reviews:

            review_table.insert(
                "",
                tk.END,
                values=(
                    review[0],
                    review[1],
                    review[2]
                )
            )

            # Кнопка добавления отзыва
        add_btn = ttk.Button(
            review_window,
            text="Add review",
            command=lambda: self.add_review(fmid)
        )
        add_btn.pack(side=tk.RIGHT,pady = 10)

        delete_btn = ttk.Button(
            review_window,
            text="Delete my review",
            command=lambda: self.delete_review(
                review_table,
                fmid,
                review_window
            )
        )
        delete_btn.pack(side=tk.LEFT, pady=10)

    def add_review(self, fmid):

        review_window = tk.Toplevel(self.root)

        review_window.title("Add review")
        review_window.geometry("350x300")


        ttk.Label(
            review_window,
            text="Comment"
        ).pack(pady=5)


        comment = tk.Text(
            review_window,
            height=5,
            width=35
        )

        comment.pack()


        ttk.Label(
            review_window,
            text="Rating (0-10)"
        ).pack(pady=5)


        rating = ttk.Entry(
            review_window
        )

        rating.pack()


        def save():

            text = comment.get(
                "1.0",
                tk.END
            ).strip()


            score = rating.get()


            if not score.isdigit():

                messagebox.showerror(
                    "Error",
                    "Rating must be number"
                )

                return


            score = int(score)


            if score < 0 or score > 10:

                messagebox.showerror(
                    "Error",
                    "Rating from 0 to 10"
                )

                return


            self.save_review(
                fmid,
                text,
                score
            )


            review_window.destroy()


        ttk.Button(
            review_window,
            text="Save",
            command=save
        ).pack(pady=15)
    
    def delete_review(self, review_table, fmid, window):

        # проверяем логин
        if self.current_user is None:

            messagebox.showerror(
                "Error",
                "Please login first"
            )

            return

        selected = review_table.selection()

        if not selected:

            messagebox.showinfo(
                "Delete",
                "Select review first"
            )

            return

        item = review_table.item(
            selected[0]
        )

        review = item["values"]

        username = review[0]

        # можно удалить только свой отзыв
        if self.current_user.username != "Admin":
            if username != self.current_user.username:

                messagebox.showerror(
                    "Error",
                    "You can delete only your reviews"
                )

                return
        
        with open(
        "market_rating_feedback.json",
        "r",
        encoding="utf-8"
        ) as file:

            data = json.load(file)

        comments = data[str(fmid)]["comment"]

        for comment in comments:

            if (
                comment[0] == username
                and comment[1] == review[1]
                and str(comment[2]) == str(review[2])
            ):
                comments.remove(comment)
                break

        if comments:

            total = 0

            for comment in comments:
                total += comment[2]
            data[str(fmid)]["rating"] = round(total / len(comments),1)

        else:

            data[str(fmid)]["rating"] = ""

        with open(
            "market_rating_feedback.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

            messagebox.showinfo(
                "Success",
                "Review deleted"
            )

            window.destroy()
            
    def save_review(self, fmid, comment, rating):

        if self.current_user is None:

            messagebox.showerror(
                "Error",
                "Please login first"
            )

            return

        with open(
            "market_rating_feedback.json",
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        username = self.current_user.username

        data[str(fmid)]["comment"].append(
            [
                username,
                comment,
                rating
            ]
        )

        # пересчитываем среднюю оценку

        total = 0

        reviews = data[str(fmid)]["comment"]

        for review in reviews:
            total += review[2]

        data[str(fmid)]["rating"] = (
            round(total / len(reviews),1)
        )

        with open("market_rating_feedback.json","w", encoding="utf-8") as file:

            json.dump(data, file,indent=4,ensure_ascii=False)

        messagebox.showinfo(
                "Success",
                "Review added"
            )

    def open_register(self):
        #Обработчик кнопки Register
        self.status_var.set("Start registration...")
        register_window = tk.Toplevel(self.root)

        register_window.title("Registration")
        register_window.geometry("350x450")


        fields = [
            "Username",
            "Firstname",
            "Surname",
            "Date of birth",
            "Email",
            "Password",
            "Confirm password"
        ]


        entries = {}


        for field in fields:

            ttk.Label(
                register_window,
                text=field
            ).pack(pady=3)


            if field == "Date of birth":

                entry = DateEntry(
                    register_window,
                    date_pattern="dd-mm-yyyy"
                )

            else:

                entry = ttk.Entry(
                    register_window
                )

            if field in ["Password", "Confirm password"]:
                entry.configure(show="*")

            entry.pack()

            entries[field] = entry

        ttk.Button(
            register_window,
            text="Register",
            style="Menu.TButton",
            command= lambda:
            self.register_user(entries,register_window)
        ).pack(pady=15)
   
    def open_login(self):
        # Обработчик кнопки Login
        self.status_var.set("Authentication...")
        
        login_window = tk.Toplevel(self.root)

        login_window.title("Authentication")
        login_window.geometry("300x200")


        ttk.Label(
            login_window,
            text="Username"
        ).pack(pady=5)


        username_entry = ttk.Entry(login_window)
        username_entry.pack()

        ttk.Label(
            login_window,
            text="Password"
        ).pack(pady=5)

        password_entry = ttk.Entry(
            login_window,
            show="*"
        )
        password_entry.pack()

        ttk.Button(
            login_window,
            text="Login",
            command=lambda:
            self.login(
                username_entry.get(),
                password_entry.get(),
                login_window
            )
        ).pack(pady=10)

    def login(self, username, password, window):

        user = User.authenticate(
            "users/users_data.csv",
            username,
            password
        )

        if user:

            self.current_user = user

            self.status_var.set(
                f"Welcome {user.username}"
            )

            messagebox.showinfo(
                "Login",
                f"Welcome {user.username}"
            )
            self.update_user_label()
            self.update_menu()

            window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Wrong username or password"
            )
    
    

    def register_user(self, entries, window):

        username = entries["Username"].get()
        firstname = entries["Firstname"].get()
        surname = entries["Surname"].get()
        dob = entries["Date of birth"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        password_confirm = entries["Confirm password"].get()


        if password != password_confirm:

            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )

            return
        elif password == "":
            messagebox.showerror(
                "Error",
                "Password shoudn't be empty"
            )
            return
        
        user, result = User.register(
        "users/users_data.csv",
        username,
        firstname,
        surname,
        dob,
        email,
        password
        )
        if user == None and result == "Username exists":
            messagebox.showerror(
                "Error",
                f"{result}"
            )
        if user == None and result == "Email exists":
            messagebox.showerror(
                "Error",
                f"{result}"
            )
        if result == "Success":
            messagebox.showinfo(
                f"{result}",
                f"User {user.username} succsessfully registred"
            )


if __name__ == "__main__":
    zip_codes = zip_util.read_zip_all("zip_codes_states.csv")
    root = tk.Tk()
    app = FarmsApp(root)
    root.mainloop()