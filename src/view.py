import tkinter as tk
from tkinter import scrolledtext
from generate_minizinc_model import GenerateMinizincCode
import unicodedata
import matplotlib.pyplot as plt

class View:
    def __init__(self,generateMinizincModel:GenerateMinizincCode):
        self.generateMinizincModel = generateMinizincModel
        self.root = tk.Tk()
        self.root.title("¿Dónde pongo mi concierto?")
        self.root.geometry("600x700")

        tk.Label(self.root, text="Pegue aquí la entrada (N, M, ciudades):").pack(pady=(10,0))
        self.text_input = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.text_input.pack(padx=10, pady=(0,10))

        self.btn = tk.Button(self.root, text="Solucionar", command=self.generate_output)
        self.btn.pack(pady=5)

        tk.Label(self.root, text="Código MiniZinc generado:").pack(pady=(10,0))
        self.text_output = scrolledtext.ScrolledText(self.root, width=70, height=20)
        self.text_output.pack(padx=10, pady=(0,10))

        self.root.mainloop()

    def remove_accents(self,texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
    )

    def generate_output(self):
        self.text_output.delete("1.0", tk.END)
        try:
            textLines = self.text_input.get("1.0", tk.END).strip().splitlines()
            if len(textLines) < 2:
                self.text_output.insert("1.0", "Error: entrada insuficiente.")
                return
            size_map = int(textLines.pop(0))
            total_cities = int(textLines.pop(0))
            cities_info = []
            for i in range(0,total_cities):
                line = textLines[i]
                line_split = line.split(' ')
                city_name = self.remove_accents(line_split[0].lower())
                coordenate_x = int(line_split[1])
                coordenate_y = int(line_split[2])
                cities_info.append([city_name,coordenate_x,coordenate_y])

            data_input={
                "size_map":size_map,
                "total_cities":total_cities,
                "cities_info":cities_info,
            }
            minizinc_code = self.generateMinizincModel.generate(data_input)
            self.text_output.insert("1.0",minizinc_code)
            #self.generate_graphic(data_input) #descomentar para visualizar coordenadas de las ciudades
        except Exception as e:
            if isinstance(e,ValueError):
                self.text_output.insert(f"1.0", "Error: Entrada incorrecta.")
            else:
                self.text_output.insert(f"1.0", "Error desconocido al generar codigo minizinc")

    def generate_graphic(self,data_input:dict):
        for i in data_input['cities_info']:
            plt.grid(True,'major')
            plt.plot(i[1],i[2],'bo',)
            plt.text(i[1],i[2],i[0])
        plt.show()