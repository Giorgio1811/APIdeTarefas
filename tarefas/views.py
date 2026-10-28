from rest_framework import generics

from .models import Tarefa
from .serializers import TarefaSerializer


class TarefaListCreateView(generics.ListCreateAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        queryset = Tarefa.objects.filter(usuario=self.request.user)

        concluida = self.request.query_params.get('concluida')
        if concluida is not None:
            queryset = queryset.filter(concluida=(concluida.lower() == 'true'))

        prioridade = self.request.query_params.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade.upper())

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class TarefaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        return Tarefa.objects.filter(usuario=self.request.user)
