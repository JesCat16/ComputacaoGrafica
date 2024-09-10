import vtk
import numpy as np
from numpy.polynomial.polynomial import polyline

# Variáveis globais

STATUS = 0.0

points_positions = [] # Lista para armazenar as posições dos pontos clicados

# Função de callback para eventos de clique do mouse
# esta função é executada quando um clique do mouse
# esquerdo é acionado e o status é igual a 1
def on_left_button_press(obj, event):
     global STATUS
     if STATUS == 1.0:
        print_mouse_position(obj)


# Função de callback para eventos de teclado
def on_key_press(obj, event):
     global STATUS  # Referencia a variável global STATUS

     key = obj.GetKeySym()
     if key == "F1":  # se apertar F1, inicia a captura dos pontos de controle
         STATUS = 1.0
         print(f"STATUS alterado para: {STATUS}")
         # Mudar o estilo de interação para um que não responde a eventos do mouse
         no_interaction_style = vtk.vtkInteractorStyle()
         obj.SetInteractorStyle(no_interaction_style)
     elif key == "Escape":  # se apertar F2, encerra a captura dos cliques e inicia a plotagem
        STATUS = 0.0
        print(f"STATUS alterado para: {STATUS}")
        # Restaurar o estilo de interação original
        original_style = vtk.vtkInteractorStyleTrackballCamera()
        obj.SetInteractorStyle(original_style)
    # Se houver pontos salvos, plota a curva de Bézier
     if points_positions:
        renderer = obj.GetRenderWindow().GetRenderers().GetFirstRenderer()
        plot_bezier_curve(renderer, points_positions)


# Função para imprimir a posição do clique do mouse e plotar um ponto
def print_mouse_position(interactor):
    click_pos = interactor.GetEventPosition()
    print(f"Posição do mouse: {click_pos}")
    # Converter as coordenadas 2D da tela para coordenadas 3D na cena (z=0)
    picker = vtk.vtkWorldPointPicker()
    picker.Pick(click_pos[0], click_pos[1], 0, interactor.GetRenderWindow().GetRenderers().GetFirstRenderer())
    world_position = picker.GetPickPosition()
    # Salvar a posição globalmente
    points_positions.append(world_position)
    print(f"Posição global do ponto clicado salva: {world_position}")
    # Chamar a função para plotar o ponto
    plot_point(interactor.GetRenderWindow().GetRenderers().GetFirstRenderer(), world_position)

def plot_point(renderer, world_position):
    # Criar um ponto pequeno na posição clicada
    point_source = vtk.vtkSphereSource()
    point_source.SetCenter(world_position)
    point_source.SetRadius(0.01) # Raio pequeno para o ponto
    point_source.Update()
    # Mapeador para o ponto
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(point_source.GetOutputPort())
    # Ator para o ponto
    point_actor = vtk.vtkActor()
    point_actor.SetMapper(mapper)
    point_actor.GetProperty().SetColor(1, 1, 1) # Cor branca para o ponto
    # Adicionar o ponto ao renderizador
    renderer.AddActor(point_actor)
    # Atualizar a renderização
    renderer.GetRenderWindow().Render()

# Função para calcular e plotar a curva de Bézier
def plot_bezier_curve(renderer, control_points):
    if len(control_points) < 2:
        print("Não há pontos suficientes para formar uma curva de Bézier.")
        return
    # Criar um vtkPoints para armazenar os pontos da curva de Bézier
    bezier_points = vtk.vtkPoints()
    # Calcular os pontos da curva de Bézier
    num_samples = 100# Número de amostras para a curva

    for t in range(num_samples + 1):
        t_normalized = t / num_samples
        x, y, z = [0.0, 0.0, 0.0]
        n = len(control_points) - 1

        for i in range(len(control_points)):
            bernstein_poly = (
            vtk.vtkMath.Binomial(n, i) *
            (t_normalized ** i) *
            ((1 - t_normalized) ** (n - i))
            )
            x += bernstein_poly * control_points[i][0]
            y += bernstein_poly * control_points[i][1]
            z += bernstein_poly * control_points[i][2]
            bezier_points.InsertNextPoint(x, y, z)

    # Criar uma vtkCellArray para armazenar a polyline
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyline)
    # Criar um vtkPolyData para armazenar os pontos e a linha
    poly_data = vtk.vtkPolyData()
    poly_data.SetPoints(bezier_points)
    poly_data.SetLines(cells)
    # Mapeador para a curva de Bézier
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)
    # Ator para a curva de Bézier
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 1, 0)  # Cor amarela para a curva
    # Adicionar a curva ao renderizador
    renderer.AddActor(actor)
    # Atualizar a renderização
    renderer.GetRenderWindow().Render()

# Função principal para configurar e executar a renderização
def main():

     # Renderizador da cena
     renderer = vtk.vtkRenderer()
     renderer.SetBackground(0.1, 0.2, 0.4) # Cor de fundo da janela
     # Janela de renderização
     renderWindow = vtk.vtkRenderWindow()
     renderWindow.AddRenderer(renderer)
     renderWindow.SetSize(600, 600) # Tamanho da janela de renderização
     # Interactor para lidar com eventos de teclado e mouse
     renderWindowInteractor = vtk.vtkRenderWindowInteractor()
     renderWindowInteractor.SetRenderWindow(renderWindow)
     # Adicionar as funções de callback para eventos de teclado e mouse
     renderWindowInteractor.AddObserver("KeyPressEvent", on_key_press)
     renderWindowInteractor.AddObserver("LeftButtonPressEvent", on_left_button_press)
     # Inicializar a visualização
     renderWindow.Render()
     renderWindowInteractor.Start()

if __name__ == "__main__":
     main()