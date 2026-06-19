import flet as ft
from db import main_db
def main(page : ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Список покупок"
    filter_type = 'all'
    
    product_list = ft.Column()
    
    product_number = 0
    product_total = ft.TextField(read_only = False, value = f"Всего куплено {product_number} продуктов")
    
    def load_products():
        product_list.controls.clear() #очистить перед добавлением
        for product_id, product_text, completed, quantity in main_db.get_products(filter_type):
            product_list.controls.append(view_products(
                product_id = product_id,
                product_text = product_text,
                completed = completed,
                quantity = quantity
            ))

        def product_count():
            number = main_db.count_products()
            return number
        
        nonlocal product_number
        product_number = product_count()
        product_total.value = f"Всего куплено {product_number} продуктов"
        
    def view_products(product_id, product_text, completed = None, quantity = None):  
        
        checkbox = ft.Checkbox(
            value = bool(completed),
            on_change= lambda e: toggle_product(product_id = product_id, is_completed = e.control.value))
        
        def save_product():
            main_db.update_product(product_id=product_id, new_product=product_field.value, quantity = quantity)
            print(f"Продукт изменен - {product_field.value}")
            product_field.read_only = True
            load_products()
            
        def enable_edit(e):
            if product_field.read_only:
                product_field.read_only = False
            else:
                product_field.read_only = True
        
        def delete_product():
            main_db.delete_product(product_id=product_id)
            load_products()
        
        
        product_field = ft.TextField(read_only = True, value = product_text, expand = True)
        edit_button = ft.IconButton(icon = ft.Icons.EDIT, on_click = enable_edit)
        save_button = ft.IconButton(icon = ft.Icons.SAVE, on_click = save_product)
        delete_button = ft.IconButton(icon = ft.Icons.DELETE, on_click= delete_product)
        
        
        def change_quantity():
            if quantity_field.value.isdigit():
                print("Ful")
                quantity = int(quantity_field.value)
                main_db.update_product(product_id = product_id, new_product = None, completed = None, quantity = quantity)
                print(f"Количество продукта изменено - {quantity_field.value}")
                load_products()
            else:
                quantity_field.value = main_db.get_quantity(product_id = product_id)
                
        def increment_quantity():
            quantity = main_db.get_quantity(product_id = product_id)+1
            main_db.update_product(product_id = product_id, new_product = None, completed = None, quantity = quantity)   
            load_products()
            
        def decrement_quantity():
            quantity = main_db.get_quantity(product_id = product_id)
            
            #Если количество упадет до 0, логично будет удалить продукт
            if quantity == 1:
                main_db.delete_product(product_id=product_id)
                load_products()
            else:
                quantity-=1
                main_db.update_product(product_id = product_id, new_product = None, completed = None, quantity = quantity) 
                load_products()
                
                
        quantity_field = ft.TextField(value = quantity, on_submit=change_quantity)
        increment_button = ft.IconButton(icon = ft.Icons.ADD, on_click = increment_quantity)
        decrement_button = ft.IconButton(icon = ft.Icons.REMOVE, on_click = decrement_quantity)
        
        return ft.Row([checkbox, product_field, edit_button, save_button, delete_button, quantity_field, increment_button, decrement_button])

    
    def toggle_product(product_id, is_completed):
            main_db.update_product(product_id=product_id, completed=int(is_completed))
            load_products() #necessary
        
    def add_product_db(e):
        if product_input.value:
            product = product_input.value
            
            product_id = main_db.add_product(product = product, quantity = 1)
            
            print(f"Продукт - {product} добавлен! Его ID = {product_id}")
            
            product_list.controls.append(view_products(product_id=product_id, product_text = product, quantity = 1))
            
            product_input.value = None
            load_products()
    
             
    product_input = ft.TextField(label = "Введите продукт", expand = True, on_submit = add_product_db)
    product_button = ft.IconButton(icon = ft.Icons.ADD, on_click=add_product_db)
    
    send_product=ft.Row([product_input, product_button])
    
    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_products()
        
    
    filter_buttons = ft.Row([
        ft.ElevatedButton('Все продукты', on_click=lambda e:set_filter('all'), icon = ft.Icons.ALL_INBOX, icon_color = ft.Colors.BLACK_87),
        ft.ElevatedButton('Некупленные', on_click=lambda e:set_filter('uncompleted'), icon = ft.Icons.LOCK_CLOCK, bgcolor = ft.Colors.YELLOW_700 ),
        ft.ElevatedButton('Купленные', on_click=lambda e:set_filter('completed'),icon = ft.Icons.CHECK_BOX, bgcolor = ft.Colors.GREEN_700)],
        alignment = ft.MainAxisAlignment.SPACE_AROUND)
    
    page.add(
        send_product,
        filter_buttons,
        product_list,
        product_total
    )
    
    load_products()
    
    
if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view = ft.AppView.WEB_BROWSER)
    