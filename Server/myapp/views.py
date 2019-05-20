from rest_framework import viewsets
from myapp.serializers import findSerializer, selectSerializer
from myapp.models import MyappFood

# 1차 추천 레시피 탐색
class findViewSet(viewsets.ModelViewSet):
    user_ingredient = ["우유", "달걀", "닭", "두부"]  # 사용자로 부터 입력 받은 재료 예시

    cntnum = [0 for _ in range(999)]  # 사용자 재료와 DB재료의 매치 갯수
    recipe_DB = MyappFood.objects.all()

    for i in range(0, 999):
        cntnum[i] = 0
        for j in range(0, len(user_ingredient)):
            comparing = recipe_DB[i].ingredients.find(user_ingredient[j])
            # find() 를 통해서 사용자의 재료가 DB 재료에 매칭 되는 지 확인(매칭되면 >=0, 매칭 되지 않으면 -1)
            if comparing >= 0:
                cntnum[i] += 1  # 매칭 되었을 때 갯수 ++

    maxi = 0  # 최대 매칭 레시피를 찾기 위한 변수

    for m in range(0, 999):  # 최대 매칭 레시피의 매칭 재료 개수 설정(maxi의 최신화)
        if cntnum[m] > maxi:
            maxi = cntnum[m]
            # print(maxi)

    for m in range(0, 999):
        if cntnum[m] == maxi:
            a = m
            break

    queryset = MyappFood.objects.filter(id=a+1) # 매칭 레시피 중 첫 번째 레시피만 일단 넣는다.

    for m in range(0, 999):  # maxi에 해당하는 최대 매칭 레시피 모두 출력
        if cntnum[m] == maxi:
            if(m != a):
                # 합 연산자를 통해 queryset에 매칭 레시피 병합
                queryset |= MyappFood.objects.filter(id = m + 1)

    serializer_class = findSerializer


# 2차 최종 레시피 출력
class selectViewSet(viewsets.ModelViewSet):
    user_choice = ["크림닭"] # 만약 사용자가 여러 레시피 중 크림닭을 선택했다면,
    queryset = MyappFood.objects.filter(recipe_name = user_choice[0]) # filter함수를 통해 해당 쿼리셋만 받아옴
    serializer_class = selectSerializer


#이 코드는 view이다. 이 것을 단축한 코드가 위의 viewset이다.
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
#
#
# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer.render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONRenderer, self).__init__(content, **kwargs)
#
# @csrf_exempt
# def Food_list(request):
#     """
#     코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
#     """
#     if request.method == 'GET':
#         foods = MyappFood.objects.all()
#         serializer = FoodSerializer(foods, many=True)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = FoodSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def Food_detail(request, pk):
#     """
#     코드 조각 조회, 업데이트, 삭제
#     """
#     try:
#         food = MyappFood.objects.get(pk=pk)
#     except MyappFood.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = FoodSerializer(food)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = FoodSerializer(food, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         food.delete()
#         return HttpResponse(status=204)