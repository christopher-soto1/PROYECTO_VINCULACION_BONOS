<?php

set_time_limit(300); // Establece el límite de ejecución a 300 segundos (5 minutos)

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require 'public/mailerPHP/Exception.php';  
require 'public/mailerPHP/PHPMailer.php';
require 'public/mailerPHP/SMTP.php';




//--------------------------------------------------------------------------------------------------------------
//LOG DE EXEPCIONES
//--------------------------------------------------------------------------------------------------------------

//FILE_APPEND: indica que el contenido se agregará al final del archivo existente.
// LOCK_EX: evita que otros procesos escriban al mismo tiempo, bloqueando el archivo momentáneamente.

function log_excep($texto) {
    log_inicio_excep();
    registro_log_excep($texto);
    log_final_excep();
    
}


function log_inicio_excep() {
    // Ruta del directorio y archivo log
    date_default_timezone_set('America/Santiago');
    $directorio = "logsProceso";
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Crear el directorio si no existe
    if (!file_exists($directorio)) {
        mkdir($directorio, 0777, true);
    }

    // Obtener la fecha y hora actuales
    $fecha_inicio = date('Y-m-d H:i:s');

    // Texto a escribir en el log
    $texto_inicio  = "******************LOG PROCESO PAGO FACTURAS******************\n";
    $texto_inicio .= "Fecha Inicio: $fecha_inicio\n";

    // Escribir el texto en el archivo log (reescribiendo el contenido)
    try {
        file_put_contents($archivoLog, $texto_inicio, LOCK_EX); // NO usamos FILE_APPEND
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}



function registro_log_excep($texto) {
    $directorio = "logsProceso";
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Crear el directorio si no existe
    if (!file_exists($directorio)) {
        mkdir($directorio, 0777, true);
    }

    // Agregar marca de tiempo
    $textoLog = $texto . "\n";

    // Escribir en el archivo log con manejo de excepciones
    try {
        file_put_contents($archivoLog, $textoLog, FILE_APPEND | LOCK_EX);
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}



function log_final_excep() {
    date_default_timezone_set('America/Santiago');
    $directorio = "logsProceso";
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Obtener la fecha y hora actuales
    $fecha_fin = date('Y-m-d H:i:s');

    // Texto de cierre del log
    $texto_final  = "Fecha Fin: $fecha_fin\n";
    $texto_final .= "***********************************************\n";

    // Escribir en el archivo log
    try {
        file_put_contents($archivoLog, $texto_final, FILE_APPEND | LOCK_EX);
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}

//FIN--------------------------------------------------------------------------------------------------------------


//------------------------------------------------------------------------------------------------------------------
//LOG PROCESO REGISTRO VINCULACION DE BONOS Y COPIADO LOG ROBOT
//------------------------------------------------------------------------------------------------------------------
function log_inicio($isapre) {
    date_default_timezone_set('America/Santiago');
    // Ruta del archivo log (en el subdirectorio "logs")
    $directorio = "logs/".$isapre;
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Crear el directorio si no existe
    if (!file_exists($directorio)) {
        mkdir($directorio, 0777, true);
    }

    // Verificar si el archivo no existe, y crearlo vacío si es necesario
    if (!file_exists($archivoLog)) {
        file_put_contents($archivoLog, '', LOCK_EX);
    }

}


function log_encabezado($isapre) {
    // Ruta del archivo log (en el subdirectorio "logs")
    $directorio = "logs/".$isapre;
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Obtener la fecha y hora actuales
    $fecha_inicio = date('Y-m-d H:i:s');

    // Texto a escribir en el log
    $texto_inicio  = "******************LOG PROCESO VINCULACION BONOS******************\n";
    $texto_inicio .= "Fecha Inicio: $fecha_inicio\n";

    // Escribir en el archivo log
    try {
        file_put_contents($archivoLog, $texto_inicio, FILE_APPEND | LOCK_EX);
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}



function copiar_log($isapre) {
    
    $origen = 'C:\\Users\\programadorll\\Documents\\sistemas_python\\RPA\\RPA_VINCULACION_BONOS\\' . $isapre . '\\LogProceso.log';
    $destino = 'C:\\xampp\\htdocs\\vinculacion_bonos\\logs\\' . $isapre . '\\log_' . date('Y-m-d') . '.log';

    // Asegurar que el directorio destino existe
    $directorioDestino = dirname($destino);
    if (!file_exists($directorioDestino)) {
        mkdir($directorioDestino, 0777, true);
    }

    // Verificar si el archivo de origen existe
    if (file_exists($origen)) {
        $contenido = file_get_contents($origen);

        // Agregar salto de línea antes del contenido
        $contenidoFinal = "\n" . $contenido;

        // Agregar contenido al archivo destino sin sobrescribir
        if (file_put_contents($destino, $contenidoFinal, FILE_APPEND | LOCK_EX) !== false) {
            echo "✅ Log copiado y agregado con salto de línea.";
        } else {
            echo "❌ Error al escribir en el archivo destino.";
        }
    } else {
        echo "❌ El archivo de origen no existe.";
    }
}



function log_proceso($txt, $isapre){
    $directorio = "logs/".$isapre;
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    $texto_proceso  = "$txt \n";

    // Escribir en el archivo log
    try {
        file_put_contents($archivoLog, $texto_proceso, FILE_APPEND | LOCK_EX);
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}


function log_final($isapre) {
    date_default_timezone_set('America/Santiago');
     $directorio = "logs/".$isapre;
    $archivoLog = $directorio . "/log_" . date("Y-m-d") . ".log";

    // Obtener la fecha y hora actuales
    $fecha_fin = date('Y-m-d H:i:s');

    // Texto de cierre del log
    $texto_final  = "Fecha Fin: $fecha_fin\n";
    $texto_final .= "*************************************************************\n";

    // Escribir en el archivo log
    try {
        file_put_contents($archivoLog, $texto_final, FILE_APPEND | LOCK_EX);
    } catch (Exception $e) {
        echo "Error al escribir en el archivo de log: " . $e->getMessage();
    }
}

//FIN----------------------------------------------------------------------------------------------------------------------



//-------------------------------------------------------------------------------------------------------------------------
//EJECUTAR ROBOT DE PYTHON 
//-------------------------------------------------------------------------------------------------------------------------
function ejecutar_tarea_banmedica_vidaTres($isapre){
    // Ruta al script Python
    #$pythonScriptPath = 'C:/Users/programadorll/Documents/sistemas_python/RPA/RPA_VINCULACION_BONOS/web-scrapping-isapres.py'; #ruta pc marcos
    $pythonScriptPath = 'C:/Users/programadorll/Desktop/PROYECTO_VINCULACION_BONOS/RPA_VINCULACION_BONOS/web-scrapping-isapres.py'; #ruta pc chris
    // Ejecutar el script Python sin parametros
    // $output = shell_exec("python \"$pythonScriptPath\" 2>&1");
     // Ejecutar el script Python con los parámetros
     $output = shell_exec("python \"$pythonScriptPath\" \"$isapre\" 2>&1");
    // Devolver la salida al navegador
    // echo $output;
    return $output;
     

}

function ejecutar_tarea_colmena(){
    // Ruta al script Python
    $pythonScriptPath = 'C:/Users/programadorll/Documents/sistemas_python/RPA/RPA_VINCULACION_BONOS/web-scrapping-isapres.py';

    // Ejecutar el script Python
    $output = shell_exec("python \"$pythonScriptPath\" 2>&1");
     // Ejecutar el script Python con los parámetros
    //  $output = shell_exec("python \"$pythonScriptPath\" \"$banco\" \"$proceso_item\" 2>&1");

    // Devolver la salida al navegador
    // echo $output;
    return $output;
}

// Continuar proceso de tareas de descaga de bonos isapres...




function ejecutarScriptPythontest(){
    $funcion = 'ejecutar_con_reintentos_bonos';
    // Ruta al script Python
    $pythonScriptPath = 'C:/Users/programadorll/Documents/sistemas_python/RPA/RPA_VINCULACION_BONOS/web-scrapping-isapres.py';
    // Ejecutar el script Python con los parámetros
    $output = shell_exec("python $pythonScriptPath $funcion 2>&1");
    // Devolver la salida al navegador
    // echo $output;
    return $output;
     

}


//TEST 
function ejecutarScriptPythonSaludar($param1, $param2) {

    $funcion = 'saludar'; // Nombre de la función Python que se desea ejecutar
    //$funcion = 'despedir';
    // Ruta al script Python
    $pythonScriptPath = 'C:/Users/programadorll/Documents/sistemas_python/RPA/RPA_VINCULACION_BONOS/web-scrapping-isapres.py';
    // Ejecutar el script Python con los parámetros
    $output = shell_exec("python \"$pythonScriptPath\" \"$funcion\" \" \"$param2\" 2>&1");
    echo $output;
    // return $output;
}

//FIN-----------------------------------------------------------------------------------------------------------------------------------



//---------------------------------------------------------------------------------------------------------------------------------------
// FUNCIONES PAGOS DE FACTURAS SISTEMAS SOFTLAND Y REBSOL 
//---------------------------------------------------------------------------------------------------------------------------------------

function validar_cirujia_pacientes($rutPaciente, $nhg) {
    try {
       

        // Llamar a la API
       $resultado = llamarApi("validar_cirujia_paciente", "GET", [
                                'rut' => $rutPaciente,
                                'nhg' => $nhg
                            ]);

        // Verificar si es un array
        if ($resultado && is_array($resultado)) {
            // Convertimos a string para buscar "error"
            $contenido = json_encode($resultado);
            
            // Si no contiene la palabra "error", retornar el resultado
            if (stripos($contenido, 'error') === false) {
                return $resultado;
            } else {
                // Contiene "error", lo retornamos tal cual para manejarlo después
                return $resultado;
            }
        }

        // Si no es un array válido, retornar error
        return ['error' => 'Respuesta inválida o vacía de la API'];

    } catch (Exception $e) {
        // Retornar el error capturado
        return ['error' => $e->getMessage()];
    }
}

//FIN-----------------------------------------------------------------------------------------------------------------------------------------


//---------------------------------------------------------------------------------------------------------------------------------------------
// ACCESO API
//---------------------------------------------------------------------------------------------------------------------------------------------
function llamarApi1($endpoint, $metodo = 'GET', $data = null) {
       
    $baseUrl ='http://localhost/apiRest/public/api/';

    // Inicializar cURL
    $ch = curl_init();
    
    // Configurar la URL completa
    $url = $baseUrl . $endpoint;
    curl_setopt($ch, CURLOPT_URL, $url);
    
    // Configurar el método
    if (strtoupper($metodo) === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true); // Definir que es una petición POST
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); // Datos en formato JSON
    } elseif (strtoupper($metodo) === 'PUT') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT'); 
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); 
    } elseif (strtoupper($metodo) === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE'); 
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); 
        
    } else {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($metodo)); // Para otros métodos
        if ($data !== null) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); // Enviar datos si no es NULL
        }
    }

    // Configurar opciones generales
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Desactivar la verificación SSL
    
    // Headers
    $headers = [
        "Authorization: Bearer ef67c3bc52c879bf724afff06bcda380",
        "Content-Type: application/json"
    ];

    // Encabezados HTTP que serán enviados junto con la solicitud cURL para asegurar que la API reciba la información en el formato adecuado y con la autorización requerida.
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    // Esta línea desactiva la verificación del certificado del servidor al que se está haciendo la solicitud.
    // curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);

    // Ejecutar la solicitud
    // $response = curl_exec($ch);
    $response = curl_exec($ch);

    // Imprime la respuesta para ver el contenido
    // echo "<pre>";
    // var_dump('imprime curl');
    // var_dump($response);
    // echo "</pre>";
    // exit();

    // Manejar errores
    if ($response === false) {
        echo "Error: " . curl_error($ch);
        return null;
    } else {
        // Retornar la respuesta decodificada
        return json_decode($response, true);
    }

    // Cerrar cURL
    curl_close($ch);
}





function llamarApi($endpoint, $metodo = 'GET', $data = null) {
    $baseUrl = 'http://localhost/apiRest/public/api/';
    
    // Si es GET y hay datos, agregarlos como query string
    if (strtoupper($metodo) === 'GET' && is_array($data)) {
        $queryString = http_build_query($data);
        $endpoint .= '?' . $queryString;
    }

    // Inicializar cURL
    $ch = curl_init();
    
    // Configurar la URL completa
    $url = $baseUrl . $endpoint;
    curl_setopt($ch, CURLOPT_URL, $url);

    // Configurar el método
    if (strtoupper($metodo) === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    } elseif (strtoupper($metodo) === 'PUT') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    } elseif (strtoupper($metodo) === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    } else {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($metodo));
        // Para GET, ya agregamos los parámetros a la URL
    }

    // Opciones generales
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    $headers = [
        "Authorization: Bearer ef67c3bc52c879bf724afff06bcda380",
        "Content-Type: application/json"
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    // Ejecutar la solicitud
    $response = curl_exec($ch);

    // Manejo de errores
    if ($response === false) {
        echo "Error: " . curl_error($ch);
        curl_close($ch);
        return null;
    }

    curl_close($ch);
    return json_decode($response, true);
}

//FIN ACCESO API--------------------------------------------------------------------------------------------------------------------------------------------



function descargar_bonos_isapres(){
  
    $proceso_isapres = array(
        "Banmedica",
        // "Vida Tres",
        // "Colmena",
        // "Consalud",
        // "Nueva Masvida",
        // "Isalud",
        // "Cruz Blanca" 
       
    );

    foreach ($proceso_isapres as $isapre) {
        switch ($isapre) {
            case 'Banmedica':
                $respuesta = ejecutar_tarea_banmedica_vidaTres($isapre);
                // echo "<pre>";
                // var_dump('DATA ejecutarScriptPython BONOS');
                // var_dump($respuesta);
                // echo "</pre>";
                copiar_log($isapre);
                $cleanedResult = str_replace("'", '"', $respuesta);
                // Decodificar el JSON
                $datos = json_decode($cleanedResult, true);
                // exit();
                // echo "<pre>";
                // var_dump('DATA ejecutarScriptPython BONOS');
                // var_dump($datos);
                // echo "</pre>";

                if (isset($datos['error'])) {
                    $mensaje = "❌ Error: {$datos['error']}\nProceso finalizado.";
                    log_proceso($mensaje, $isapre);
                    break;
                }

                $data_detalle_pacientes = $datos['arreglo_paciente'];
                // echo "<pre>";
                // var_dump('DATA data_detalle_pacientes');
                // var_dump($data_detalle_pacientes);
                // echo "</pre>";

                foreach ($data_detalle_pacientes as $index => $paciente) {
                    $folioPam = $paciente['folio_pam'];
                    $numCuenta = $paciente['num_cuenta'];
                    $rutAfiliado = str_replace('.', '', $paciente['rut_afiliado']);
                    $rutPaciente = str_replace('.', '', $paciente['rut_paciente']);
                    $nombrePaciente = $paciente['nombre_paciente'];
                    $montoFacturado = $paciente['monto_facturado'];
                    $montoBonificado = $paciente['monto_bonificado'];
                    $fechaIngreso = $paciente['fecha_ingreso_estado_pam'];

                    $respuesta = validar_cirujia_pacientes($rutPaciente, 0);
                    echo "<pre>";
                    var_dump('respuesta endpoint validar_cirujia_pacientes');
                    var_dump($respuesta);
                    echo "</pre>";
                    exit();


                }
                
                // exit();
                $data_detalle_bonos = $datos['arreglo_bonos'];
                echo "<pre>";
                var_dump('DATA data_detalle_bonos');
                var_dump($data_detalle_bonos);
                echo "</pre>";
                exit();


                
                log_inicio($isapre);
                log_encabezado($isapre);
                log_proceso($txt, $isapre);
                log_final($isapre);
                
                break;

            case 'Colmena':
                echo "Procesando Colmena...\n";
                break;

            case 'Consalud':
                echo "Procesando Consalud...\n";
                break;

            case 'Nueva Masvida':
                echo "Procesando Nueva Masvida...\n";
                break;

            case 'Vida Tres':
                echo "Procesando Vida Tres...\n";
                break;

            case 'Isalud':
                echo "Procesando Isalud...\n";
                break;

            case 'Cruz Blanca':
                echo "Procesando Cruz Blanca...\n";
                break;

            default:
                echo "Isapre no reconocida: $isapre\n";
                break;
        }
    }

    // $respuesta = ejecutarScriptPythonSaludar('Mateo', 'Huenchuñir');
    // $respuesta = ejecutarScriptPython();
    // copiar_log();
    // $cleanedResult = str_replace("'", '"', $respuesta);
    // // Decodificar el JSON
    // $datos = json_decode($cleanedResult, true);
    // echo "<pre>";
    // var_dump('DATA ejecutarScriptPython BONOS');
    // var_dump($datos);
    // echo "</pre>";
    // exit();

}


//--------------------------------------------------------------
// INICIO PROCESO PAGO DE FACTURAS FONASA
//--------------------------------------------------------------

// Establecer zona horaria de Chile
date_default_timezone_set('America/Santiago');

// Función que deseas ejecutar
function ejecutarTarea() {
    
    descargar_bonos_isapres();
    // envir_email();
    
}

// Lista de feriados en Chile para 2025 (formato dd/mm/yyyy)
$feriados_chile = [
    '01/01/2025', '18/04/2025', '19/04/2025', '01/05/2025',
    '21/05/2025', '20/06/2025', '29/06/2025', '16/07/2025',
    '15/08/2025', '18/09/2025', '19/09/2025', '12/10/2025',
    '31/10/2025', '01/11/2025', '08/12/2025', '25/12/2025',
];

// Día actual
$diaSemana = date('N'); // 1 = lunes, 7 = domingo
// $diaSemana = 7; // 1 = lunes, 7 = domingo
$hoy = date('d/m/Y');

// Verifica si es de lunes a viernes y no es feriado
if ($diaSemana >= 1 && $diaSemana <= 5 && !in_array($hoy, $feriados_chile)) {
    // ejecutarTarea();

    $respuesta = validar_cirujia_pacientes('6743584-2', 0);
    echo "<pre>";
    var_dump('respuesta endpoint validar_cirujia_pacientes');
    var_dump($respuesta);
    echo "</pre>";
    exit();
   
} else {

    log_inicio("logs_dias_inhabiles");
    $fecha_fin = date('Y-m-d H:i:s');
    $texto_inicio = "******************LOG PROCESO VINCULACION DE BONOS******************\n";
    $texto_inicio .= "Fecha inicio: $fecha_fin";
    log_proceso($texto_inicio,"logs_dias_inhabiles");
    $mensaje = "⛔ Hoy es " . traducirDia(date('l')) . " " . date('d/m/Y') . ". No se ejecuta la tarea PROCESO VINCULACION DE BONOS.";
    log_proceso($mensaje . "\nProceso finalizado.", "logs_dias_inhabiles");
    log_final("logs_dias_inhabiles");

}

// Función para traducir días al español
function traducirDia($diaIngles) {
    $dias = [
        'Monday'    => 'Lunes',
        'Tuesday'   => 'Martes',
        'Wednesday' => 'Miércoles',
        'Thursday'  => 'Jueves',
        'Friday'    => 'Viernes',
        'Saturday'  => 'Sábado',
        'Sunday'    => 'Domingo',
    ];
    return $dias[$diaIngles] ?? $diaIngles;
}


?>