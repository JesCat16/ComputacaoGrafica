import vtk
import numpy as np

# Variáveis globais
STATUS = 0.0  # esta variável global indica se vc está clicando ou olhando a curva
points = []  # esta variável global serve apenas para guardar os pontos inicial e final

tanges1 = [1, 1, 0]  # Tangentes (tx1, ty1, tz1) para o ponto 1
tanges2 = [1, 1, 0]  # Tangentes (tx2, ty2, tz2) para o ponto 2


# Função de callback para eventos de teclado
def on_key_press(obj, event):
    global STATUS  # Referencia a variável global STATUS

    key = obj.GetKeySym()

    if key == "F1":
        STATUS = 1.0
        print(f"STATUS alterado para: {STATUS}")

        # Mudar o estilo de interação para um que não responde a eventos do mouse
        no_interaction_style = vtk.vtkInteractorStyle()
        obj.SetInteractorStyle(no_interaction_style)

    elif key == "Escape":
        STATUS = 0.0
        print(f"STATUS alterado para: {STATUS}")

        # Restaurar o estilo de interação original
        original_style = vtk.vtkInteractorStyleTrackballCamera()
        obj.SetInteractorStyle(original_style)

    elif key == "F2":
        renderer = obj.GetRenderWindow().GetRenderers().GetFirstRenderer()
        renderer.RemoveAllViewProps()  # Remove todos os atores do renderizador
        points.clear()
        print("Cenário redefinido e lista de pontos limpa.")
        obj.GetRenderWindow().Render()


# Função de callback para eventos de clique do mouse
def on_left_button_press(obj, event):
    global STATUS
    if STATUS == 1.0:
        renderer = obj.GetRenderWindow().GetRenderers().GetFirstRenderer()
        print_mouse_position(obj, renderer)


# Função para criar a curva após os pontos serem clicados
def create_curve(renderer):
    p0 = points[0]
    p1 = points[1]
    # Usar as tangentes definidas para os pontos
    t0 = tanges1
    t1 = tanges2
    # Criar a curva de Hermite
    create_hermite_curve(renderer, p0, p1, t0, t1)


# Função para imprimir a posição do clique do mouse e plotar um ponto
def print_mouse_position(interactor, renderer):
    click_pos = interactor.GetEventPosition()
    # Converter as coordenadas 2D da tela para coordenadas 3D na cena (z=0)
    picker = vtk.vtkWorldPointPicker()
    picker.Pick(click_pos[0], click_pos[1], 0, renderer)
    world_position = picker.GetPickPosition()
    points.append(world_position)
    # Criar um ponto pequeno na posição clicada
    point_source = vtk.vtkSphereSource()
    point_source.SetCenter(world_position)
    point_source.SetRadius(0.002)  # Raio pequeno para o ponto
    point_source.Update()
    # Mapeador para o ponto
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(point_source.GetOutputPort())
    # Ator para o ponto
    point_actor = vtk.vtkActor()
    point_actor.SetMapper(mapper)
    point_actor.GetProperty().SetColor(1, 1, 1)  # Cor branca para o ponto
    # Adicionar o ponto ao renderizador
    renderer.AddActor(point_actor)
    # Atualizar a renderização
    renderer.GetRenderWindow().Render()
    # Verifica se dois pontos foram clicados
    if len(points) == 2:
        create_curve(renderer)


# Função para criar a curva de Hermite
def create_hermite_curve(renderer, p0, p1, t0, t1):
    num_samples = 100
    hermite_points = vtk.vtkPoints()
    # Parâmetro t varia de 0 a 1
    for t in np.linspace(0, 1, num_samples):
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1
        h01 = -2 * t ** 3 + 3 * t ** 2
        h10 = t ** 3 - 2 * t ** 2 + t
        h11 = t ** 3 - t ** 2
        x = h00 * p0[0] + h10 * t0[0] + h01 * p1[0] + h11 * t1[0]
        y = h00 * p0[1] + h10 * t0[1] + h01 * p1[1] + h11 * t1[1]
        z = h00 * p0[2] + h10 * t0[2] + h01 * p1[2] + h11 * t1[2]
        ## aqui guarda só os pontos
        hermite_points.InsertNextPoint(x, y, z)
        # Criar uma polyline para criar as linhas que conectam os pontos da curva
    # aqui cria só as linhas
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(hermite_points.GetNumberOfPoints())
    for i in range(hermite_points.GetNumberOfPoints()):
        polyline.GetPointIds().SetId(i, i)

    # Criar uma vtkCellArray para armazenar as linhas da polyline
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyline)
    # Criar um vtkPolyData para armazenar os pontos e a linha
    poly_data = vtk.vtkPolyData()
    poly_data.SetPoints(hermite_points)
    poly_data.SetLines(cells)
    # Mapeador para a curva de Hermite
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)
    # Ator para a curva de Hermite
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 0)  # Cor amarela para a curva
    # Adicionar a curva ao renderizador
    renderer.AddActor(actor)
    # Atualizar a renderização
    renderer.GetRenderWindow().Render()

def main():
    # Função principal para configurar e executar a renderização
    # Renderizador da cena
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4)  # Cor de fundo da janela
    # Janela de renderização
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(600, 600)  # Tamanho da janela de renderização
    # Interactor para lidar com eventos de teclado e mouse
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Adicionar as funções de callback para eventos de teclado e mouse
    renderWindowInteractor.AddObserver("KeyPressEvent", on_key_press)
    renderWindowInteractor.AddObserver("LeftButtonPressEvent", on_left_button_press)
    # Inicializar a visualização
    renderWindow.Render()
    renderWindowInteractor.Start()


main()