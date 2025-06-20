from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from .models import Car

# Create your views here.

def ping(request):
    return HttpResponse('pong')

@csrf_exempt
def createCar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get("name")
            speed = data.get("speed")


            if not (name and speed):  
                return HttpResponse('data missing', status=400)

            car = Car(name=name, speed=speed) 
            car.save()

            return HttpResponse(f'data created with id {car.id}', status=200)
        except Exception as e:
            return HttpResponse(f'data creation failed: {str(e)}', status=500)

def readCar(request, id):
    try:
        car = Car.objects.get(id=id)
        return JsonResponse({"id": car.id, "name": car.name, "speed": car.speed}, status=200)
    except Car.DoesNotExist:
        return HttpResponse("Car not found", status=404)
    

@csrf_exempt
def updateCar(request, id):
    if request.method == 'PATCH': # PATCH allows partial update
        try:
            data = json.loads(request.body)
            car = Car.objects.get(id=id)

            if "name" in data:
                car.name = data["name"]
            if "speed" in data:
                car.speed = data["speed"]

            car.save()
            return HttpResponse("Car updated successfully", status=200)
        except Car.DoesNotExist:
            return HttpResponse("Car not found", status=404)
        except Exception as e:
            return HttpResponse(f"Update failed: {str(e)}", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def deleteCar(request, id):
    if request.method == 'DELETE':
        try:
            car = Car.objects.get(id=id)
            car.delete()
            return HttpResponse("Car deleted successfully", status=200)
        except Car.DoesNotExist:
            return HttpResponse("Car not found", status=404)
        except Exception as e:
            return HttpResponse(f"Delete failed: {str(e)}", status=500)

def readAllCars(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        data = [{"id": car.id, "name": car.name, "speed": car.speed} for car in cars]
        return JsonResponse(data, safe=False, status=200)

