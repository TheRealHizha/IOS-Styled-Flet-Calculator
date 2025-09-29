import flet as ft
import math

def main(page: ft.Page):
    # Page setup
    page.title = "iOS Calculator"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#000000"
    page.padding = 20
    
    # Initialize calculator state
    current_value = "0"
    previous_value = ""
    operation = None
    reset_screen = False
    
    # Display area
    display = ft.Text(
        value="0",
        size=64,
        color="white",
        text_align="right",
        weight="w300",
        selectable=True,
    )
    
    # Secondary display for showing previous operations
    secondary_display = ft.Text(
        value="",
        size=24,
        color="#a5a5a5",
        text_align="right",
        weight="w300",
    )
    
    # Function to update display
    def update_display():
        display.value = current_value
        secondary_display.value = previous_value + (f" {operation} " if operation else "")
        page.update()
    
    # Button click handler
    def button_click(e):
        nonlocal current_value, previous_value, operation, reset_screen
        
        # Get the button text
        button_text = e.control.data
        
        if button_text in "0123456789":
            if current_value == "0" or reset_screen:
                current_value = button_text
                reset_screen = False
            else:
                current_value += button_text
                
        elif button_text == ".":
            if "." not in current_value:
                current_value += "."
                
        elif button_text == "AC":
            current_value = "0"
            previous_value = ""
            operation = None
            
        elif button_text == "±":
            if current_value != "0":
                if current_value[0] == "-":
                    current_value = current_value[1:]
                else:
                    current_value = "-" + current_value
                    
        elif button_text == "%":
            current_value = str(float(current_value) / 100)
            
        elif button_text in ["+", "-", "×", "÷"]:
            if previous_value and not reset_screen:
                # Calculate the result if there's a previous operation
                calculate()
            previous_value = current_value
            operation = button_text
            reset_screen = True
            
        elif button_text == "=":
            if previous_value and operation:
                calculate()
                previous_value = ""
                operation = None
                reset_screen = True
                
        update_display()
    
    # Calculation function
    def calculate():
        nonlocal current_value, previous_value
        
        try:
            num1 = float(previous_value)
            num2 = float(current_value)
            
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "×":
                result = num1 * num2
            elif operation == "÷":
                if num2 == 0:
                    result = "Error"
                else:
                    result = num1 / num2
            
            # Format the result
            if result == "Error":
                current_value = result
            else:
                # Remove .0 if it's an integer
                current_value = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)
                
        except:
            current_value = "Error"
    
    # Create calculator buttons
    def create_button(text, bgcolor, color, expand=1, font_size=28):
        return ft.Container(
            content=ft.Text(
                text, 
                size=font_size, 
                color=color, 
                weight="bold",
                text_align="center"
            ),
            margin=4,
            border_radius=50,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            expand=expand,
            height=80,
            on_click=button_click,
            data=text,
            ink=True,
        )
    
    # Button layout
    buttons = [
        ft.Row(
            controls=[
                create_button("AC", "#a5a5a5", "black", 1),
                create_button("±", "#a5a5a5", "black", 1),
                create_button("%", "#a5a5a5", "black", 1),
                create_button("÷", "#ff9f0a", "white", 1),
            ],
            spacing=4,
        ),
        ft.Row(
            controls=[
                create_button("7", "#333333", "white", 1),
                create_button("8", "#333333", "white", 1),
                create_button("9", "#333333", "white", 1),
                create_button("×", "#ff9f0a", "white", 1),
            ],
            spacing=4,
        ),
        ft.Row(
            controls=[
                create_button("4", "#333333", "white", 1),
                create_button("5", "#333333", "white", 1),
                create_button("6", "#333333", "white", 1),
                create_button("-", "#ff9f0a", "white", 1),
            ],
            spacing=4,
        ),
        ft.Row(
            controls=[
                create_button("1", "#333333", "white", 1),
                create_button("2", "#333333", "white", 1),
                create_button("3", "#333333", "white", 1),
                create_button("+", "#ff9f0a", "white", 1),
            ],
            spacing=4,
        ),
        ft.Row(
            controls=[
                create_button("0", "#333333", "white", 2),
                create_button(".", "#333333", "white", 1),
                create_button("=", "#ff9f0a", "white", 1),
            ],
            spacing=4,
        ),
    ]
    
    # Calculator container
    calculator = ft.Container(
        width=400,
        padding=20,
        border_radius=20,
        bgcolor="#000000",
        content=ft.Column(
            controls=[
                # Secondary display
                ft.Container(
                    content=secondary_display,
                    padding=ft.padding.only(right=20, top=20, bottom=0),
                    alignment=ft.alignment.center_right,
                ),
                # Main display
                ft.Container(
                    content=display,
                    padding=ft.padding.only(right=20, bottom=20),
                    alignment=ft.alignment.center_right,
                ),
                # Buttons
                *buttons
            ],
            spacing=10,
        ),
    )
    
    # Add calculator to page
    page.add(
        ft.ResponsiveRow(
            controls=[
                calculator
            ],
            alignment="center",
        )
    )
    
    # Update the display initially
    update_display()

# Start the app
ft.app(target=main)
