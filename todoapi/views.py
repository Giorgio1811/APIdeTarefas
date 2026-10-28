from django.http import JsonResponse


def home(_request):
    return JsonResponse(
        {
            'projeto': 'API de Tarefas',
            'status': 'online',
            'mensagem': 'API funcionando. Consulte /api/login/ e /api/tarefas/.',
        }
    )
