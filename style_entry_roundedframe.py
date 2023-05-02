# --------------------
# This file is used for defining Ttk styles.
# Use the 'style' object to define styles.

# Pygubu Designer will need to know which style definition file
# you wish to use in your project.

# To specify a style definition file in Pygubu Designer:
# Go to: Edit -> Preferences -> Ttk Styles -> Browse (button)

# In Pygubu Designer:
# Assuming that you have specified a style definition file,
# - Use the 'style' combobox drop-down menu in Pygubu Designer
#   to select a style that you have defined.
# - Changes made to the chosen style definition file will be
#   automatically reflected in Pygubu Designer.
# --------------------


style.configure("Transparent.TEntry",
                background="#081B2E",  # Cor de fundo transparente
                fieldbackground="transparent",  # Cor de fundo do campo de texto transparente
                highlightthickness=0,  # Remover borda
                bd=0,  # Remover borda
                insertbackground="black",  # Cor do cursor
                font=('Arial', 12, 'bold'),
                foreground='white'
                )

style.configure('Tabless.TNotebook.Tab', background='#091b2e', foreground='#091b2e', padding=(0, 0, 0, 0),
                borderwidth=0, overrelief='flat', relief='flat')
# style.map('Tabless.TNotebook.Tab', background=[('selected', '#091b2e')])
# Remover as abas do Tabless.TNotebook
style.layout('Tabless.TNotebook.Tab', [])