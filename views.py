from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin_data
import uuid

class StartScraping(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not coins:
            return Response({'error': 'No coins provided'}, status=status.HTTP_400_BAD_REQUEST)
        job_id = str(uuid.uuid4())
        task_results = [scrape_coin_data.apply_async(args=[coin], task_id=f"{job_id}_{coin}") for coin in coins]
        return Response({'job_id': job_id, 'tasks': [result.id for result in task_results]}, status=status.HTTP_200_OK)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        coins = request.GET.getlist('coins', [])
        results = {coin: AsyncResult(f"{job_id}_{coin}").result for coin in coins}
        return Response({'job_id': job_id, 'tasks': results}, status=status.HTTP_200_OK)
