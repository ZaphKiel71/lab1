from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Alumno, Carrera
from .serializers import AlumnoSerializer, CarreraSerializer
from .permission import IsDirectorOrReadOnly

from rest_framework.authentication import TokenAuthentication


from rest_framework.authtoken.models import Token


# Método de login
@api_view(['POST'])
@permission_classes([AllowAny])  # Permite acceso sin autenticación
def login(request):
    username = request.data.get('nombre')
    password = request.data.get('contraseña')
    user = authenticate(username=username, password=password)

    if user is not None:
        token,create = Token.objects.get_or_create(user = user)
        return Response({ "token": token.key, "message": "Login exitoso"}, status=status.HTTP_200_OK)
    return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


# Método para agregar una carrera
@api_view(['POST'])
@permission_classes([IsDirectorOrReadOnly]) 
def add_carrera(request):
    serializer = CarreraSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Método para agregar un alumno
@api_view(['POST'])
@permission_classes([IsDirectorOrReadOnly]) 
def add_alumno(request):
    serializer = AlumnoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Método para obtener una carrera específica y sus alumnos
@api_view(['GET'])
def get_carrera(request, id):
    carrera = get_object_or_404(Carrera, id=id)  # Obtiene la carrera o devuelve un 404 si no existe
    alumnos = Alumno.objects.filter(carrera=carrera)  # Filtra los alumnos por la carrera
    carrera_serializer = CarreraSerializer(carrera)
    alumnos_serializer = AlumnoSerializer(alumnos, many=True)
    
    return Response({
        'carrera': carrera_serializer.data,
        'alumnos': alumnos_serializer.data
    }, status=status.HTTP_200_OK)

# Método para listar las carreras
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_carreras(request):
    carreras = Carrera.objects.all()
    serializer = CarreraSerializer(carreras, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

# Metodo para actualizar carreras
@api_view(['PATCH'])
@permission_classes([IsDirectorOrReadOnly]) 
def update_carrera(request, id):
    carrera = get_object_or_404(Carrera, id=id)  # Busca la carrera o devuelve un 404 si no existe
    serializer = CarreraSerializer(carrera, data=request.data, partial=True)  # partial=True permite actualizaciones parciales
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Metodo para Eliminar una carrera

@api_view(['DELETE'])
@permission_classes([IsDirectorOrReadOnly]) 
def delete_carrera(request, id):
    carrera = get_object_or_404(Carrera, id=id)  # Busca la carrera o responde con un 404 si no existe
    carrera.delete()  # Elimina la carrera de la base de datos
    return Response({"message": "Carrera eliminada exitosamente"}, status=status.HTTP_204_NO_CONTENT)

# Metodo para listar alumnos
@api_view(['GET'])
def list_alumnos(request):
    alumnos = Alumno.objects.all()  # Recupera todos los alumnos
    serializer = AlumnoSerializer(alumnos, many=True)  # Serializa los datos
    return Response(serializer.data, status=status.HTTP_200_OK)


#Metodo para listar un alumno en especifico y su carrera

@api_view(['GET'])
def get_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)  # Busca el alumno o devuelve 404
    alumno_serializer = AlumnoSerializer(alumno)  # Serializa los datos del alumno
    carrera_serializer = CarreraSerializer(alumno.carrera)  # Serializa la carrera del alumno

    return Response({
        'alumno': alumno_serializer.data,
        'carrera': carrera_serializer.data
    }, status=status.HTTP_200_OK)

# Metodo para actualizar un alumno 
@api_view(['PATCH'])
@permission_classes([IsDirectorOrReadOnly]) 
def update_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)  # Busca el alumno o devuelve 404
    serializer = AlumnoSerializer(alumno, data=request.data, partial=True)  # Permite actualizaciones parciales
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Metodo para eliminar un alumno


@api_view(['DELETE'])
@permission_classes([IsDirectorOrReadOnly]) 
def delete_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)  # Busca el alumno o devuelve 404
    alumno.delete()  # Elimina el alumno de la base de datos
    return Response({"message": "Alumno eliminado exitosamente"}, status=status.HTTP_204_NO_CONTENT)


