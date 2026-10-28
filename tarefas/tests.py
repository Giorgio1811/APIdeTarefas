from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Tarefa


class TarefasAPITest(APITestCase):
    def setUp(self):
        self.ana = User.objects.create_user('ana', password='senha123')
        self.beto = User.objects.create_user('beto', password='senha123')
        self.tok_ana = Token.objects.create(user=self.ana)
        self.tok_beto = Token.objects.create(user=self.beto)
        self.t1 = Tarefa.objects.create(
            titulo='Estudar Django', prioridade='ALTA', usuario=self.ana,
        )
        self.t2 = Tarefa.objects.create(
            titulo='Lavar o carro', prioridade='BAIXA',
            concluida=True, usuario=self.ana,
        )
        self.t3 = Tarefa.objects.create(
            titulo='Tarefa do Beto', prioridade='ALTA', usuario=self.beto,
        )

    def como(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client

    def test_home_funciona(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'online')

    def test_login_devolve_token(self):
        response = self.client.post(
            reverse('api-login'), {'username': 'ana', 'password': 'senha123'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.tok_ana.key)

    def test_sem_token_401(self):
        self.assertEqual(self.client.get(reverse('tarefa-lista')).status_code, 401)

    def test_lista_so_do_proprio_usuario(self):
        response = self.como(self.tok_ana).get(reverse('tarefa-lista'))
        titulos = {tarefa['titulo'] for tarefa in response.data}
        self.assertEqual(titulos, {'Estudar Django', 'Lavar o carro'})

    def test_filtros(self):
        client = self.como(self.tok_ana)
        response = client.get(reverse('tarefa-lista') + '?prioridade=Alta')
        self.assertEqual([t['titulo'] for t in response.data], ['Estudar Django'])
        response = client.get(reverse('tarefa-lista') + '?concluida=true')
        self.assertEqual([t['titulo'] for t in response.data], ['Lavar o carro'])
        response = client.get(
            reverse('tarefa-lista') + '?concluida=false&prioridade=alta',
        )
        self.assertEqual([t['titulo'] for t in response.data], ['Estudar Django'])

    def test_criar_define_dono_pelo_token(self):
        response = self.como(self.tok_ana).post(
            reverse('tarefa-lista'), {'titulo': 'Nova', 'usuario': self.beto.id},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tarefa.objects.get(titulo='Nova').usuario, self.ana)

    def test_patch_altera_so_um_campo(self):
        response = self.como(self.tok_ana).patch(
            reverse('tarefa-detalhe', args=[self.t1.id]), {'concluida': True},
        )
        self.assertEqual(response.status_code, 200)
        self.t1.refresh_from_db()
        self.assertTrue(self.t1.concluida)
        self.assertEqual(self.t1.titulo, 'Estudar Django')
        self.assertEqual(self.t1.prioridade, 'ALTA')

    def test_isolamento_404_em_detalhe_de_outro(self):
        client = self.como(self.tok_beto)
        url = reverse('tarefa-detalhe', args=[self.t1.id])
        self.assertEqual(client.get(url).status_code, 404)
        self.assertEqual(client.patch(url, {'concluida': True}).status_code, 404)
        self.assertEqual(client.delete(url).status_code, 404)
        self.assertTrue(Tarefa.objects.filter(pk=self.t1.id).exists())

    def test_delete_proprio(self):
        response = self.como(self.tok_ana).delete(
            reverse('tarefa-detalhe', args=[self.t2.id]),
        )
        self.assertEqual(response.status_code, 204)
