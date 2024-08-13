import vtk

# Leitura do arquivo OBJ
reader = vtk.vtkOBJReader()
reader.SetFileName("Wolf_One_obj.obj")
reader.Update()

# Mapeador
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Criar uma transformação para o ator do cubo
transform = vtk.vtkTransform()

# Ator
ator = vtk.vtkActor()
ator.SetMapper(mapper)
ator.SetUserTransform(transform)

# Renderizador
renderer = vtk.vtkRenderer()
renderer.AddActor(ator)
renderer.SetBackground(0.1, 0.2, 0.3) # Cor de fundo

# Janela de renderização
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(800, 600)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# função para transformações geométricas com o teclado
def meu_teclado (obj, event): # nome da função
 key = obj.GetKeySym() # aqui captura a tecla pressionada
 if key == "h": # se for a tela “h” executa a ação
    transform.Translate(1.2, 1, 1) # Translada 10 unidades no eixo Y
    renderWindow.Render() # Atualizar a renderização

# Inicializar a visualização
# Associar a função de callback ao evento de tecla
renderWindowInteractor.AddObserver("KeyPressEvent", meu_teclado)
renderWindow.Render()
renderWindowInteractor.Start()