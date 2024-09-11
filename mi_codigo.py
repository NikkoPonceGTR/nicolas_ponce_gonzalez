<?php
// db_connect.php
$servername = "localhost";
$username = "root";
$password = ""; // Cambia esta línea si tienes una contraseña configurada para MySQL
$dbname = "AGENCIA";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>

<?php
// index.php
session_start();
include 'db_connect.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['add-vuelo'])) {
        $origen = $_POST['origen'];
        $destino = $_POST['destino'];
        $fecha = $_POST['fecha'];
        $plazas_disponibles = $_POST['plazas_disponibles'];
        $precio = $_POST['precio'];

        $stmt = $conn->prepare("INSERT INTO VUELO (origen, destino, fecha, plazas_disponibles, precio) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$origen, $destino, $fecha, $plazas_disponibles, $precio]);

        echo "Vuelo agregado correctamente.";
    } elseif (isset($_POST['add-hotel'])) {
        $nombre = $_POST['nombre'];
        $ubicacion = $_POST['ubicacion'];
        $habitaciones_disponibles = $_POST['habitaciones_disponibles'];
        $tarifa_noche = $_POST['tarifa_noche'];

        $stmt = $conn->prepare("INSERT INTO HOTEL (nombre, ubicacion, habitaciones_disponibles, tarifa_noche) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$nombre, $ubicacion, $habitaciones_disponibles, $tarifa_noche]);

        echo "Hotel agregado correctamente.";
    } elseif (isset($_POST['add-reserva'])) {
        $id_cliente = $_POST['id_cliente'];
        $fecha_reserva = $_POST['fecha_reserva'];
        $id_vuelo = $_POST['id_vuelo'];
        $id_hotel = $_POST['id_hotel'];

        $stmt = $conn->prepare("INSERT INTO RESERVA (id_cliente, fecha_reserva, id_vuelo, id_hotel) VALUES (?, ?, ?, ?)");
        $stmt->execute([$id_cliente, $fecha_reserva, $id_vuelo, $id_hotel]);

        echo "Reserva agregada correctamente.";
    }
}

function displayReservas($conn) {
    $stmt = $conn->prepare("SELECT * FROM RESERVA");
    $stmt->execute();
    $reservas = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($reservas as $reserva) {
        echo "ID Reserva: " . $reserva['id_reserva'] . " - ID Cliente: " . $reserva['id_cliente'] . " - Fecha: " . $reserva['fecha_reserva'] . " - ID Vuelo: " . $reserva['id_vuelo'] . " - ID Hotel: " . $reserva['id_hotel'] . "<br>";
    }
}

function displayHotelesConMasDeDosReservas($conn) {
    $stmt = $conn->prepare("SELECT HOTEL.nombre, COUNT(*) as num_reservas FROM RESERVA JOIN HOTEL ON RESERVA.id_hotel = HOTEL.id_hotel GROUP BY HOTEL.nombre HAVING num_reservas > 2");
    $stmt->execute();
    $hoteles = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($hoteles as $hotel) {
        echo "Hotel: " . $hotel['nombre'] . " - Reservas: " . $hotel['num_reservas'] . "<br>";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agencia de Viajes - Gestión de Vuelos, Hoteles y Reservas</title>
</head>
<body>
    <h2>Agregar Vuelo</h2>
    <form method="POST">
        <label for="origen">Origen:</label>
        <input type="text" id="origen" name="origen" required><br>

        <label for="destino">Destino:</label>
        <input type="text" id="destino" name="destino" required><br>

        <label for="fecha">Fecha:</label>
        <input type="date" id="fecha" name="fecha" required><br>

        <label for="plazas_disponibles">Plazas Disponibles:</label>
        <input type="number" id="plazas_disponibles" name="plazas_disponibles" required><br>

        <label for="precio">Precio:</label>
        <input type="number" step="0.01" id="precio" name="precio" required><br>

        <button type="submit" name="add-vuelo">Agregar Vuelo</button>
    </form>

    <h2>Agregar Hotel</h2>
    <form method="POST">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre" required><br>

        <label for="ubicacion">Ubicación:</label>
        <input type="text" id="ubicacion" name="ubicacion" required><br>

        <label for="habitaciones_disponibles">Habitaciones Disponibles:</label>
        <input type="number" id="habitaciones_disponibles" name="habitaciones_disponibles" required><br>

        <label for="tarifa_noche">Tarifa por Noche:</label>
        <input type="number" step="0.01" id="tarifa_noche" name="tarifa_noche" required><br>

        <button type="submit" name="add-hotel">Agregar Hotel</button>
    </form>

    <h2>Agregar Reserva</h2>
    <form method="POST">
        <label for="id_cliente">ID Cliente:</label>
        <input type="number" id="id_cliente" name="id_cliente" required><br>

        <label for="fecha_reserva">Fecha de Reserva:</label>
        <input type="date" id="fecha_reserva" name="fecha_reserva" required><br>

        <label for="id_vuelo">ID Vuelo:</label>
        <input type="number" id="id_vuelo" name="id_vuelo" required><br>

        <label for="id_hotel">ID Hotel:</label>
        <input type="number" id="id_hotel" name="id_hotel" required><br>

        <button type="submit" name="add-reserva">Agregar Reserva</button>
    </form>

    <h2>Reservas Realizadas</h2>
    <?php displayReservas($conn); ?>

    <h2>Hoteles con más de dos reservas</h2>
    <?php displayHotelesConMasDeDosReservas($conn); ?>
</body>
</html>

