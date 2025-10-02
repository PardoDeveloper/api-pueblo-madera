## ACTIVAR ENTORNO VIRTUAL
Windows (Powershell)
Invoke-Expression (poetry env activate)

UNIX
eval $(poetry env activate)

## INSTALAR DEPDENCIAS
poetry install

## AÑADIR DEPENDENCIAS
poetry add <dependencia>

## ARRANCAR PROYECTO
uvicorn main:app --reload