# Stealth Pool v2 iOS

Suite de trucos para 8 Ball Pool en iPhone con instalacion directa por OTA (Over The Air) desde Safari, sin necesidad de computadora.

## Version actual

2.4.0 (build 1)

## Instalacion en iPhone

1. Entra a https://xpeee-banned.github.io/Stealth-Pool-iOS/ desde Safari en tu iPhone.
2. Toca el boton Instalar en iPhone.
3. Safari pide confirmacion, toca Instalar.
4. Ve a Ajustes, General, Gestion de VPN y Dispositivos.
5. Confia el perfil de desarrollador de la app.
6. Abre Stealth Pool desde la pantalla de inicio.

Se requiere iOS 14 o superior. El IPA se firma de forma ad-hoc, por eso hay que confiar el certificado en Ajustes la primera vez.

## Que incluye

- Streamer mode: oculta el HUD de trucos cuando estas transmitiendo.
- Autoplay: el juego juega los tiros automaticamente.
- Auto-update: la app avisa cuando hay una version nueva.
- Menu superpuesto configurable con estilo oscuro.

## Como funciona

El inyector embebe FridaGadget dentro del proceso de 8 Ball Pool y ejecuta un script de Frida que inyecta el menu de trucos. Al abrir 8 Ball Pool veras el HUD de Stealth Pool superpuesto.

## Actualizaciones

La app revisa el archivo version.json en cada inicio. Cuando existe una version mas reciente, la pagina de descarga muestra el boton de instalacion actualizado. El workflow de GitHub Actions compila el IPA, crea un release y publica la pagina automaticamente en cada push a main.

## Compilar el IPA

Opcion A: GitHub Actions (recomendada)

- Haz push a main y el workflow build-ipa.yml compila, firma y publica el IPA.

Opcion B: Local en Windows

- Ejecuta ios/build_ipa.bat o python ios/ipa_builder.py.
- El script descarga FridaGadget, arma el bundle y genera artifacts/StealthPool-2.4.0.ipa.

Opcion C: Local en macOS

- Compila con xcrun: xcrun -sdk iphoneos clang -arch arm64 -fobjc-arc -framework Foundation ios/launcher.m -o Payload/StealthPool.app/StealthPool
- Firma con codesign --force --deep --sign - Payload/StealthPool.app
- Empaqueta con zip -qry artifacts/StealthPool-2.4.0.ipa Payload

## Estructura

- ios/ — codigo de la app, inyector y scripts de build
- site/ — pagina de descarga e instalacion OTA
- scripts/ — utilidades de version y build
- .github/workflows/ — CI con GitHub Actions

## Aviso

Proyecto de uso educativo y de investigacion. Usalo bajo tu propia responsabilidad y respeta los terminos de servicio del juego. No esta afiliado con Miniclip ni con 8 Ball Pool.
