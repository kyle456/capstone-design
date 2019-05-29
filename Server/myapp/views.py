import json
from myapp.serializers import Recommend, Final
from myapp.models import Menu
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response


# 인식한 재료를 바탕으로 여러 레시피 후보를 추천
class Recommend_recipes(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Menu.objects.all()
        serializer = Recommend(queryset, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # received_json_data = json.loads(request.body)
            # ingredient1 = received_json_data['Ingredient1']
            # ingredient2 = received_json_data['Ingredient2']
            # ingredient3 = received_json_data['Ingredient3']
            # ingredient4 = received_json_data['Ingredient4']
            # ingredient5 = received_json_data['Ingredient5']
            # user_ingredient = [ingredient1, ingredient2, ingredient3, ingredient4, ingredient5]
            user_ingredient = list(request.data.values())

            recipe_DB = Menu.objects.all()
            cntnum = [[0 for o in range(2)] for p in range(len(recipe_DB))]  # 사용자 재료와 DB재료의 매치 갯수

            for i in range(0, len(recipe_DB)):
                cntnum[i][1] = recipe_DB[i].mname
                for j in range(0, len(user_ingredient)):
                    comparing = recipe_DB[i].ingredient.find(user_ingredient[j])
                    # find() 를 통해서 사용자의 재료가 DB 재료에 매칭 되는 지 확인(매칭되면 >=0, 매칭 되지 않으면 -1)
                    if comparing >= 0:
                        cntnum[i][0] += 1  # 매칭 되었을 때 갯수 ++

            maxi = 0  # 최대 매칭 레시피를 찾기 위한 변수

            for m in range(0, len(recipe_DB)):  # 최대 매칭 레시피의 매칭 재료 개수 설정(maxi의 최신화)
                if cntnum[m][0] > maxi:
                    maxi = cntnum[m][0]
                    # print(maxi)

            for m in range(0, len(recipe_DB)):
                if cntnum[m][0] == maxi:
                    firstrecipe = cntnum[m][1]
                    break

            queryset = Menu.objects.filter(mname=firstrecipe)  # 매칭 레시피 중 첫 번째 레시피만 일단 넣는다.

            for m in range(0, len(recipe_DB)):  # maxi에 해당하는 최대 매칭 레시피 모두 출력
                if cntnum[m][0] == maxi:
                    if (cntnum[m][1] != firstrecipe):
                        # 합 연산자를 통해 queryset에 매칭 레시피 병합
                        queryset |= Menu.objects.filter(mname=cntnum[m][1])

            serializer = Recommend(queryset, many=True)

            return Response(serializer.data)


# 사용자가 최종 선택한 레시피 반환
class Final_recipes(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Menu.objects.all()
        serializer = Final(queryset, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # received_json_data = json.loads(request.body)
            # choice = received_json_data['Choice']
            choice = list(request.data.values())

            queryset = Menu.objects.filter(mname = choice[0]) # filter함수를 통해 해당 쿼리셋만 받아옴
            serializer = Final(queryset, many=True)

            return Response(serializer.data)