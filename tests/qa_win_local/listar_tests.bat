@echo off
echo.
echo ==========================================
echo   TESTS DISPONIBLES EN qa_win_local
echo ==========================================
echo.
echo === CASOS DE USO (8 tests) ===
echo 1. test_cu01_crear_pedido_simple.bat
echo 2. test_cu02_crear_pedido_con_opciones.bat
echo 3. test_cu03_listar_pedidos.bat
echo 4. test_cu04_cambiar_estado_pedido.bat
echo 5. test_cu05_validaciones_errores.bat
echo 6. test_cu06_crear_sesion.bat
echo 7. test_cu07_listar_sesiones.bat
echo 8. test_cu08_actualizar_cerrar_sesion.bat
echo.
echo === HISTORIAS DE USUARIO (5 tests) ===
echo 9. test_hu_c02.py ^(Python^)
echo 10. test_hu_c07_api.bat
echo 11. test_hu_c07_precios.py ^(Python^)
echo 12. test_hu_c08_comentarios.bat
echo.
echo === UTILIDADES ===
echo - run_all_tests.bat - Ejecutar todos
echo - verificar_entorno.bat - Verificar prerequisitos
echo - INICIO_RAPIDO.bat - Guia rapida
echo - README.md - Documentacion completa
echo - LISTA_TESTS.md - Lista detallada
echo.
echo ==========================================
echo   COMANDOS UTILES
echo ==========================================
echo.
echo Ejecutar todos los tests:
echo   run_all_tests.bat
echo.
echo Verificar entorno:
echo   verificar_entorno.bat
echo.
echo Ejecutar un test especifico:
echo   test_cu01_crear_pedido_simple.bat
echo   python test_hu_c02.py
echo.
echo Ver documentacion:
echo   type README.md
echo   type LISTA_TESTS.md
echo.
echo ==========================================
echo.
pause
