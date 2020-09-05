
# Desafio1Estructura
## Cómo Ejecutar
`DesafioUno.py` se debe ejecutar como cualquier archivo python y por defecto viene con 4 problemas para resolver. 
Si desea crear un nuevo problema, se deberá editar el código y crear o editar un objeto Container.
Ejemplo:
```python
cont = Container(
	np.array(
		[[19, 2, 0, 0, 0],
		[16, 15, 0, 0, 0],
		[16, 14, 4, 7, 19],
		[10, 13, 0, 0, 0],
		[18, 13, 13, 7, 0]]
	)

)
```

Para instanciar un Container, se debera pasar un estado inicial como una matriz numpy.

Para resolver el problema, solo se tendrá que utilizar la función greedy_solve de esta manera:
```python
cont = Container(
	np.array(
		[[19, 2, 0, 0, 0],
		[16, 15, 0, 0, 0],
		[16, 14, 4, 7, 19],
		[10, 13, 0, 0, 0],
		[18, 13, 13, 7, 0]]
	)

)

#Retornara el estado final
res = greedy_solve(cont)

#Para renderizar el estado final, utilizaremos el metodo render.
res.render()
```


## Presentación de la Solución
https://drive.google.com/file/d/1ko8hgUEdhWLBQTd0ipu7LXmlsQnxO90c/view
