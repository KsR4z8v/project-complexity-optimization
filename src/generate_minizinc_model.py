from functools import reduce

class GenerateMinizincCode():
  def generate(self,data_input:dict):
    output:str = ''
    constraints:str = ''
    variables_ubication_cities:str = ''
    variables_distances_concert:str = ''
    variables_differences_cities:str =''
    output+= f'var int:concert_x; %Coordenada x del concierto\n'
    output+=f'var int:concert_y; %Coordenada y del concierto\n\n'
    max_diference_variables:list = []
    output_minizinc:list = ['"Ubicacion concierto: (",show(concert_x),",",show(concert_y),");\\n"']
    constraints+= f'constraint concert_x <={data_input['size_map']};'
    constraints+=f'\nconstraint concert_y <={data_input['size_map']};'
    constraints+='\nconstraint concert_x >=0;'
    constraints+='\nconstraint concert_y >=0;\n'

    for i in range(0,data_input['total_cities']):
        city_info = data_input['cities_info'][i]
        variable_name:str = city_info[0]
        variable_x_value:int = city_info[1]
        variable_y_value:int = city_info[2]
        variables_ubication_cities+= f'var int: {variable_name}_x = {variable_x_value};\n'
        variables_ubication_cities+= f'var int: {variable_name}_y = {variable_y_value};\n'
        variables_distances_concert+= f'var int: {variable_name}_distance = abs(concert_x - {variable_name}_x) + abs(concert_y - {variable_name}_y);\n'
        output_minizinc.append(f'"Distancia a {variable_name.upper()}: ",show({variable_name}_distance),"km\\n"')
        constraints+= f'constraint not (concert_x = {variable_name}_x /\\ concert_y = {variable_name}_y);\n'
        for j in range(i+1,data_input['total_cities']):
          next_city_name = data_input['cities_info'][j][0]
          name_variable_distance = f'{variable_name}_{next_city_name}_difference'
          max_diference_variables.append(name_variable_distance)
          variables_differences_cities+=f'var int: {name_variable_distance} = abs({variable_name}_distance - {next_city_name}_distance);\n'

    output+=f'%Ubicaciones de cada ciudad\n{variables_ubication_cities}\n'
    output+= f'%Cálculo de distancias Manhattan a cada ciudad\n{variables_distances_concert}\n'
    output+=f'%Diferencias de distancias manhattan entre ciudades\n{variables_differences_cities}\n'
    output+= f'%Recoge todas las diferencias en un arreglo y extrae el mayor\nvar int:max_difference = max([{reduce(lambda x,y:f'{x},{y}',max_diference_variables)}]);\n'
    output+=f'\n%Restricciones\n{constraints}\n'
    output+="solve minimize max_difference;\n\n"
    output+= f'output [{reduce(lambda x,y:f'{x},{y}',output_minizinc)}];\n\n'

    return output
