# seed-data.ps1 - Poblar base de datos con datos de prueba
# Ejecutar después de iniciar el servidor

$API = "http://127.0.0.1:8000/api"

Write-Host "🌱 Fresh Bowl - Poblando datos de prueba..." -ForegroundColor Green
Write-Host ""

# Verificar que el servidor esté corriendo
try {
    $null = Invoke-RestMethod -Uri "$API/productos/" -Method GET -TimeoutSec 3
} catch {
    Write-Host "❌ Error: El servidor no está corriendo en $API" -ForegroundColor Red
    Write-Host "   Ejecuta primero: .\start-server.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Servidor detectado" -ForegroundColor Green

# Crear categorías
Write-Host "`n📂 Creando categorías..." -ForegroundColor Yellow
$categorias = @(
    '{"nombre":"Ensaladas","descripcion":"Ensaladas frescas y nutritivas"}',
    '{"nombre":"Bowls","descripcion":"Bowls completos y balanceados"}',
    '{"nombre":"Proteínas","descripcion":"Opciones con proteína extra"}',
    '{"nombre":"Vegano","descripcion":"Opciones 100% vegetales"}'
)

foreach ($cat in $categorias) {
    try {
        $result = Invoke-RestMethod -Uri "$API/categorias/" -Method POST -Body $cat -ContentType "application/json" -ErrorAction SilentlyContinue
        Write-Host "  ✓ Categoría creada" -ForegroundColor Gray
    } catch {}
}

# Crear productos
Write-Host "`n🥗 Creando productos..." -ForegroundColor Yellow
$productos = @(
    '{"nombre":"Ensalada César","descripcion":"Lechuga romana, pollo grillado, queso parmesano, crutones y aderezo César","precio":6990,"disponible":true}',
    '{"nombre":"Bowl Mediterráneo","descripcion":"Quinoa, falafel, hummus, pepino, tomate y aceitunas","precio":7990,"disponible":true}',
    '{"nombre":"Ensalada Griega","descripcion":"Pepino, tomate, cebolla morada, aceitunas kalamata y queso feta","precio":5990,"disponible":true}',
    '{"nombre":"Bowl Tropical","descripcion":"Arroz, mango, pollo teriyaki, edamame y aguacate","precio":8490,"disponible":true}',
    '{"nombre":"Ensalada Caprese","descripcion":"Tomate fresco, mozzarella, albahaca y reducción de balsámico","precio":6490,"disponible":true}',
    '{"nombre":"Bowl Proteico","descripcion":"Base de espinaca, pollo, huevo, garbanzos y semillas","precio":8990,"disponible":true}',
    '{"nombre":"Ensalada Asiática","descripcion":"Repollo, zanahoria, edamame, maní y aderezo de jengibre","precio":6790,"disponible":true}',
    '{"nombre":"Bowl Vegano Power","descripcion":"Quinoa, tofu, aguacate, kale y tahini","precio":7490,"disponible":true}'
)

foreach ($prod in $productos) {
    try {
        $result = Invoke-RestMethod -Uri "$API/productos/" -Method POST -Body $prod -ContentType "application/json" -ErrorAction SilentlyContinue
        Write-Host "  ✓ Producto creado" -ForegroundColor Gray
    } catch {}
}

# Crear ingredientes
Write-Host "`n🥬 Creando ingredientes..." -ForegroundColor Yellow
$ingredientes = @(
    '{"nombre":"Lechuga","adicional":false,"precio_adicional":0,"stock":100,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Tomate","adicional":false,"precio_adicional":0,"stock":80,"stock_minimo":15,"disponible":true}',
    '{"nombre":"Pepino","adicional":false,"precio_adicional":0,"stock":5,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Zanahoria","adicional":false,"precio_adicional":0,"stock":0,"stock_minimo":10,"disponible":false}',
    '{"nombre":"Espinaca","adicional":false,"precio_adicional":0,"stock":60,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Pollo Grillado","adicional":true,"precio_adicional":1500,"stock":25,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Queso Feta","adicional":true,"precio_adicional":800,"stock":3,"stock_minimo":5,"disponible":true}',
    '{"nombre":"Palta","adicional":true,"precio_adicional":1200,"stock":0,"stock_minimo":8,"disponible":false}',
    '{"nombre":"Huevo Duro","adicional":true,"precio_adicional":500,"stock":40,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Quinoa","adicional":true,"precio_adicional":600,"stock":50,"stock_minimo":10,"disponible":true}',
    '{"nombre":"Tofu","adicional":true,"precio_adicional":900,"stock":30,"stock_minimo":8,"disponible":true}',
    '{"nombre":"Salmón","adicional":true,"precio_adicional":2500,"stock":15,"stock_minimo":5,"disponible":true}'
)

foreach ($ing in $ingredientes) {
    try {
        $result = Invoke-RestMethod -Uri "$API/ingredientes/" -Method POST -Body $ing -ContentType "application/json" -ErrorAction SilentlyContinue
        Write-Host "  ✓ Ingrediente creado" -ForegroundColor Gray
    } catch {}
}

# Crear usuarios de prueba
Write-Host "`n👤 Creando usuarios de prueba..." -ForegroundColor Yellow
$usuarios = @(
    '{"nombre":"Administrador","email":"admin@freshbowl.cl","password":"admin123","telefono":"+56912345678"}',
    '{"nombre":"Cliente Demo","email":"cliente@demo.cl","password":"demo123","telefono":"+56987654321"}'
)

foreach ($user in $usuarios) {
    try {
        $result = Invoke-RestMethod -Uri "$API/usuarios/" -Method POST -Body $user -ContentType "application/json" -ErrorAction SilentlyContinue
        Write-Host "  ✓ Usuario creado" -ForegroundColor Gray
    } catch {}
}

Write-Host "`n✅ ¡Datos de prueba creados exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "Usuarios disponibles:" -ForegroundColor Cyan
Write-Host "  • admin@freshbowl.cl / admin123"
Write-Host "  • cliente@demo.cl / demo123"
Write-Host ""
Write-Host "Ahora abre FrontEnd/index.html en tu navegador 🚀" -ForegroundColor Yellow
