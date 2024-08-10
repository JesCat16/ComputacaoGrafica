import vtk

# Leitura do arquivo OBJ
reader = vtk.vtkOBJReader()
reader.SetFileName("Wolf_One_obj.obj")
reader.Update()

# Mapeador
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Ator
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Renderizador (Cria um Cenário e adiciona o Ator a esse cenário)
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.3)  # Cor de fundo


# Janela de renderização
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(800, 600)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Inicializar a visualização
renderWindow.Render()
renderWindowInteractor.Start()
