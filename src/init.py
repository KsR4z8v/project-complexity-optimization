from functools import reduce
from datetime import datetime
import matplotlib.pyplot as plt
import unicodedata


def remove_accents(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def read_input_file(path):
    with open(f'./{path}') as inputFile:
      readLines = inputFile.readlines()
      size_map = int(readLines.pop(0))
      total_cities = int(readLines.pop(0))
      cities_info = []

      for i in range(0,total_cities):
          line =readLines[i]
          line_split = line.split(' ')
          city_name = remove_accents(line_split[0].lower())
          coordenate_x = int(line_split[1])
          coordenate_y = int(line_split[2])
          cities_info.append([city_name,coordenate_x,coordenate_y])
    return {
      "size_map":size_map,
      "total_cities":total_cities,
      "cities_info":cities_info,
    }



def map_input_to_minizinc(data_input:dict):
  output:str = ''
  output+='% tamaño del mapa y posibles ubicaciones del concierto\n'
  output+= f'var 0..{data_input['size_map']}:limit_x;\n'
  output+=f'var 0..{data_input['size_map']}:limit_y;\n\n'
  max_diference_variables = []

  output_minizinc = ['"Ubicacion concierto: (",show(limit_x),",",show(limit_y),");\\n"']

  for i in range(0,data_input['total_cities']):
      city_info = data_input['cities_info'][i]
      variable_name:str = city_info[0]
      variable_x_value:int = city_info[1]
      variable_y_value:int = city_info[2]
      output+= f'var int: {variable_name}_x = {variable_x_value};\n'
      output+= f'var int: {variable_name}_y = {variable_y_value};\n'
      output+= f'var int: {variable_name}_distance = abs(limit_x - {variable_name}_x) + abs(limit_y - {variable_name}_y);\n'
      output_minizinc.append(f'"Distancia a {variable_name.upper()}: ",show({variable_name}_distance),"km\\n"')
      for j in range(i+1,data_input['total_cities']):
        next_city_name = data_input['cities_info'][j][0]
        name_variable_distance = f'{variable_name}_{next_city_name}_difference'
        max_diference_variables.append(name_variable_distance)
        output+=f'var int: {name_variable_distance} = abs({variable_name}_distance - {next_city_name}_distance);\n'

      output+= f'constraint not (limit_x = {variable_name}_x /\ limit_y = {variable_name}_y);'
      output+='\n\n'


  output+= f'var int:max_difference = max([{reduce(lambda x,y:f'{x},{y}',max_diference_variables)}]);\n\n'
  output+="solve minimize max_difference;\n\n"
  output+= f'output [{reduce(lambda x,y:f'{x},{y}',output_minizinc)}];\n\n'

  return output



def write_output(content:str):
  with open(f'./outputs/output_{datetime.now().isoformat()}.mzn','w') as file:
     file.write(content)
     file.close()



def generate_graphic(data_input:dict):
   for i in data_input['cities_info']:
      plt.grid(True,'major')
      plt.plot(i[1],i[2],'bo',)
      plt.text(i[1],i[2],i[0])
   plt.show()



def main():
  if(__name__ == '__main__'):
    data_input = read_input_file('./inputs/input2.txt')
    minizincCode = map_input_to_minizinc(data_input)
    write_output(minizincCode)
    generate_graphic(data_input)


main()
