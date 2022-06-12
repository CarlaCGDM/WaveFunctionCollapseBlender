###########################################################################################
#                                                                                         #
#                                  GENERADOR DE MAPAS                                     #
#                                     SquirrelCarla                                       #
#                                         v1.0                                            #
#                                                                                         #
#                                      Referencias:                                       #
#                                                                                         #
#                                 1. shorturl.at/cdhzI                                    #
#                                 2. shorturl.at/gilA2                                    #
#                                                                                         #
#-----------------------------------------------------------------------------------------#
#                                                                                         #
#  1. Partimos de un set de baldosas con algunos bordes coincidentes.                     #
#                                                                                         #
#  2. Generamos un índice de referencia con las demás baldosas con las que cada baldosa   #
#     conecta en cada dirección (arriba, abajo, derecha, izquierda).                      #
#                                                                                         #
#  3. Creamos una cuadrícula vacía de X por Y dimensiones.                                #
#                                                                                         #
#  4. Elegimos una baldosa al azar y la colocamos en la posición (0,0) de la cuadrícula.  #
#                                                                                         #
#  5. Evaluamos las baldosas adyacentes a esta y elegimos una baldosa al azar que pueda   #
#     conectar con todas las casillas ocupadas alrededor de cada una de ellas (de momento # 
#     una).                                                                               #
#                                                                                         #
#  6. Repetimos la operación hasta que ya no nos queden más casillas vacías por evaluar.  #
#                                                                                         #
########################################################################################### 


import bpy
import random
import math

###########################################################################################
#                                                                                         #
#                            GENERANDO EL INDICE DE REFERENCIA                            #
#                                                                                         #
###########################################################################################

#Función que comprueba si dos baldosas coinciden en una dirección dada:

def check_match(tile1,tile2,direction:tuple):
    
    X,Y = direction
    positions1 = set()
    positions2 = set()
    
    if X != 0:
        for vert in tile1.data.vertices:
            x = round(vert.co.x,1)
            y = round(vert.co.y,2)
            if x == 0.5*X:
                positions1.add(y) 
                
        for vert in tile2.data.vertices:
            x = round(vert.co.x,1)
            y = round(vert.co.y,2)
            if x == -0.5*X:
                positions2.add(y)
    else:
        for vert in tile1.data.vertices:
            x = round(vert.co.x,2)
            y = round(vert.co.y,1)
            if y == 0.5*Y:
                positions1.add(x) 
                
        for vert in tile2.data.vertices:
            x = round(vert.co.x,2)
            y = round(vert.co.y,1)
            if y == -0.5*Y:
                positions2.add(x)
                
    if positions1 == positions2:
        return True
    
    return False
    
#Función que genera el índice de referencia, utilizando la anterior:

def adyacency_matrix(tileset):
    
    UP = (0, 1)
    LEFT = (-1, 0)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    directions = [UP, DOWN, LEFT, RIGHT]
    
    matrix = {}
    for tile in tileset:
        matrix[tile.name] = {}
        for dir in directions:
            matrix[tile.name][dir] = []
            for tile2 in tileset:
                if check_match(tile,tile2,dir) == True:
                    matrix[tile.name][dir].append(tile2.name)
                    
    return matrix

###########################################################################################
#                                                                                         #
#                                RELLENANDO LA CUADRÍCULA                                 #
#                                                                                         #
###########################################################################################

#Funcion que genera la cuadrícula vacía:

def empty_grid(h,w):
    grid = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append("##No_Data##")
        grid.append(row)
    return grid

#Función que devuelve las celdas vacías adyacentes a una celda dada:

def empty_adjacents(grid:list,cell:list):
    adjacents = []
    dirs = [(0,1),(0,-1),(-1,0),(1,0)]
    
    y,x = cell
    for d in dirs:
        dy,dx = d
        new_cell = (y+dy,x+dx)
        if new_cell[0] in range(0,len(grid)) and new_cell[1] in range(0,len(grid[0])):
            value = grid[new_cell[0]][new_cell[1]]
            if value == "##No_Data##":
                adjacents.append(new_cell)
                print("Celda añadida: ")
                print(new_cell)
                print("Valor en grid: ")
                print(grid[new_cell[0]][new_cell[1]])
        
    return adjacents

#Función que devuelve las baldosas adyacentes a una celda dada junto con la dirección
#por la cual conectan con la celda:

def occupied_directions(grid:list,cell:list):
    neighbours = []
    dirs = [(0,1),(0,-1),(-1,0),(1,0)]
    
    y,x = cell
    for d in dirs:
        dy,dx = d
        new_cell = (y+dy,x+dx)
        if new_cell[0] in range(0,len(grid)) and new_cell[1] in range(0,len(grid[0])):
            value = grid[new_cell[0]][new_cell[1]]
            if value != "##No_Data##":
                neighbours.append(((-dy,-dx),value))
        
    return neighbours
                    
###################################################################################
#
#                              RANDOMLY PLACING ASSETS
#
###################################################################################

def randomized_detail(ground_mesh):
    detail_assets = [
        bpy.data.objects["Tree"],
        bpy.data.objects["Rock"]
    ]
    
    #le pasamos el suelo ya creado al 100%
    #evaluamos cada poligono y vemos el material
    #si el material es el material hierba, tiramos un dado de 10
    #si sale 1, elegimos al azar de la lista de assets
    #ponemos un linked duplicate de la asset en esa posicion
    #seguimos evaluando
    
    
###################################################################################
#
#                                 PROGRAMA PRINCIPAL
#
###################################################################################

if __name__ == "__main__":
    
    #Limpiar antiguo:

    coll = bpy.data.collections.get("Board")
    coll2 = bpy.data.collections.get("Details")
    # if it doesn't exist create it
    if coll is not None:
    
        for m in coll.objects:
            bpy.data.objects.remove(m)
        
        for m in coll2.objects:
            bpy.data.objects.remove(m)
        
        collection = bpy.data.collections.get('Board')
        bpy.data.collections.remove(collection)
        collection = bpy.data.collections.get('Details')
        bpy.data.collections.remove(collection)
    
    #Renombramos el mesh de cada objeto para que coincida con su nombre:
    for obj in bpy.data.collections["Tiles"].all_objects:
        if obj.type == 'MESH':
            obj.data.name = obj.name
    
    #Creamos nuestro tileset: (hacer automatico desde una coleccion)
    tileset = []
    
    for obj in bpy.data.collections["Tiles"].all_objects:
        tileset.append(obj)
        
    matrix = adyacency_matrix(tileset)
    
    #Generamos un grid vacío
    h = 10
    w = 10
    grid = empty_grid(h,w)
    
    board = bpy.data.collections.new('Board')
    bpy.context.scene.collection.children.link(board)
        
    #Rellenamos la primera celda y la dibujamos en 3D: 
    first = (0,0)
    y,x = first
    
    new_mesh = random.choice(tileset).data
    grid[y][x] = new_mesh.name
    
    ob = bpy.data.objects.new(new_mesh.name + '_Linked', new_mesh)
    board.objects.link(ob)
    ob.location = (x,y,0)
    
    #Creamos la cola de celdas pendientes de evaluar:
    stack = []
    
    adjacent_cells = empty_adjacents(grid,first)
    stack.extend(adjacent_cells)
    
    #Bucle que recorre todas las celdas de la cola:
    while len(stack) > 0:
        new_cell = stack.pop()
        y,x = new_cell
        
        #Neighbours with limiting information:
        neighbours = occupied_directions(grid,new_cell)
        
        #get a list for the ones that are possible in each direction
        #keep the ones present in all lists
        possibilities = []
        for neighbour in neighbours:
            dir,tile = neighbour
            possibilities.append(matrix[tile][dir])
        
        elements_in_all = list(set.intersection(*map(set, possibilities)))
        
        #pick a random one from those
        if len(elements_in_all) > 0:
            new_tile = random.choice(elements_in_all)
            grid[y][x] = new_tile
        
            #put the tile in the map
            new_tile_mesh = bpy.data.objects[new_tile].data
            ob = bpy.data.objects.new(new_tile + '_Linked', new_tile_mesh)
        
            board.objects.link(ob)
            ob.location = (y,x,0)
        
            #add others to stack
            adjacent_cells = empty_adjacents(grid,new_cell)
            for a in adjacent_cells:
                if a not in stack:
                    stack.append(a)
        else:
            print(new_cell)
            print(neighbours)
            print(possibilities)
            print(elements_in_all)
    
    #Unificar tablero
    
    #seleccionar todos los objetos de la coleccion
    #coll = bpy.data.collections.get('Board')
    #for obj in coll.objects:
        #obj.select_set(True)
    
    #bpy.context.view_layer.objects.active = coll.objects[0]
    
    #join selected
    #bpy.ops.object.join()
    
    #merge by distance ??
    
    #evaluate each tile:
    details = bpy.data.collections.new('Details')
    bpy.context.scene.collection.children.link(details)
    
    detail_assets = [
        bpy.data.objects["Tree"],
        bpy.data.objects["Rock"]
    ]
    
    for obj in bpy.data.collections.get('Board').objects:
        obj_loc = obj.location
        for face in obj.data.polygons:
            loc = obj_loc + face.center
            #if material is green
            if face.material_index == 0:
                if random.randint(0,5) == 1:
                    #add random mesh from assets in global position to board collection
                    asset = random.choice(detail_assets).data
                    ob = bpy.data.objects.new(asset.name, asset)
                    details.objects.link(ob)
                    ob.location = loc
                    ob.rotation_euler[2] = math.radians(random.randint(0,360))
                    
    #podemos hacer una version "borde" de cada tile asi si esta en el borde
    #se reemplaza por su "borde" correspondiente
                    
