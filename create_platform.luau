local Workspace = game:GetService("Workspace")
local CollectionService = game:GetService("CollectionService")

-- Crear la nueva parte
local platform = Instance.new("Part")
platform.Name = "PlataformaMagica"
platform.Anchored = true
platform.Size = Vector3.new(5, 1, 5)
platform.Position = Vector3.new(0, 5, 10)
platform.BrickColor = BrickColor.new("Cyan") -- Color visible

-- Es importante establecer el Parent antes o después, pero para Tags no importa tanto.
-- Lo pondremos en el Workspace ahora.
platform.Parent = Workspace

-- Asignar la etiqueta "Crystal" usando CollectionService
CollectionService:AddTag(platform, "Crystal")

print("Plataforma creada y etiquetada como 'Crystal'")
