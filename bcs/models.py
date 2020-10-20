from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


CNH_CATEGORIA_CHOICES = [	(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, 'AB'), (6, 'AC'), (7, 'AD'), (8, 'AE'), (9, 'Não Informado')]

BC_SITUACAO_CHOICES = [('A','Ativo'), ('I','Inativo')]

USUARIO_ESTADO_CIVIL_CHOICES = [(0, 'Solteiro (a)'), (1, 'Casado (a)'), (2, 'Divorciado (a)'),
								(3, 'Separado (a)'), (4, 'Viúvo (a)'), (5,'Outro')]

USUARIO_ESCOLARIDADE_CHOICES = [(0, 'Ensino Fundamental Incompleto'), (1, 'Ensino Fundamental Completo'),
								(2, 'Ensino Médio Incompleto'), (3, 'Ensino Médio Completo'),
								(4, 'Ensino Superior Incompleto'), (5, 'Ensino Superior Completo')]


class Uf(models.Model):
	uf_nome = models.CharField(max_length=100, verbose_name="Estado:")
	uf_sigla = models.CharField(max_length=2, default="SC", verbose_name="Sigla:")

	def __str__(self):
		return self.uf_nome+" - "+self.uf_sigla


class Cidade(models.Model):
	cid_uf = models.ForeignKey("Uf", on_delete=models.CASCADE, verbose_name="Estado:")
	cid_nome = models.CharField(max_length=100, verbose_name="Cidade:")
	
	def __str__(self):
		return self.cid_nome+" / "+self.cid_uf.uf_sigla


class Endereco(models.Model):
	end_logradouro = models.CharField(max_length=200, verbose_name="Logradouro:")
	end_numero = models.CharField(max_length=10, verbose_name="Número:")
	end_complemento = models.CharField(default="", max_length=100, blank=True, null=True, verbose_name="Complemento:")
	end_bairro = models.CharField(max_length=100, verbose_name="Bairro:")
	end_cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, verbose_name="Cidade:")
	end_cep = models.CharField(max_length=100, verbose_name="CEP:")

	def __str__(self):
		return self.end_logradouro+", "+self.end_numero+" "+self.end_bairro+" - "+self.end_cidade.__str__()


class Graduacao(models.Model):
	gra_grau = models.CharField(max_length=200, verbose_name="Grau:")
	gra_simbolo = models.ImageField(upload_to='graduacao_pictures/', verbose_name="Símbolo:", blank=True, null=True)

	def __str__(self):
		return self.gra_grau


class Cnh(models.Model):
	cnh_numero = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número da CNH:")
	cnh_categoria = models.IntegerField(default=9, choices=CNH_CATEGORIA_CHOICES, verbose_name="Categoria:")
	cnh_validade = models.DateField(blank=True, null=True, verbose_name="Validade:")
	cnh_condutor_emergencia = models.BooleanField(verbose_name="Condutor de Emergência?")
	cnh_ultimo_cve = models.DateField(blank=True, null=True, verbose_name="Data do Último CVE:")

	def get_categoria(self):
		return CNH_CATEGORIA_CHOICES[self.cnh_categoria][1]

	def __str__(self):
		return self.cnh_numero


class Bc(models.Model):
	bc_usuario = models.OneToOneField("Usuario", on_delete=models.CASCADE, verbose_name="Usuário:")
	bc_nome_de_guerra = models.CharField(max_length=200, verbose_name="Nome de Guerra:")
	bc_graduacao = models.ForeignKey(Graduacao, on_delete=models.CASCADE, verbose_name="Graduação:")
	bc_data_formatura = models.DateField(blank=True, null=True, verbose_name="Data da Formatura:")
	bc_data_ultima_promocao = models.DateField(blank=True, null=True, verbose_name="Data da Última Promoção:")
	bc_situacao = models.BooleanField(default=True, verbose_name="Situação: (ativo/inativo)")

	bc_cnh = models.ForeignKey("Cnh", blank=True, null=True, on_delete=models.CASCADE, verbose_name="CNH:")
	bc_mergulhador = models.BooleanField(blank=True, null=True, verbose_name="Mergulhador?")

	def get_situacao(self):
		if self.bc_situacao:
			return 'Ativo'
		else:
			return 'Inativo'

	def __str__(self):
		return "BC "+self.bc_nome_de_guerra.upper()


class Usuario(models.Model):
	usu_user = models.OneToOneField(User, related_name="Usuario", on_delete=models.CASCADE, verbose_name="Usuário:")

	usu_lotacao = models.ForeignKey("Unidade", on_delete=models.CASCADE, verbose_name="Lotação:", blank=True, null=True)
	# Informações Básicas
	usu_nome = models.CharField(max_length=200, verbose_name="Nome Completo:")
	usu_foto = models.ImageField(upload_to='usuario_pictures/', blank=True, verbose_name="Foto de Perfil:")
	usu_data_de_nascimento = models.DateField(verbose_name="Data de Nascimento:")
	usu_sexo = models.CharField(max_length=1, verbose_name="Sexo:", choices=[('M', "Masculino"), ('F', "Feminino"), ('O',"Não declarado")])
	usu_naturalidade = models.CharField(max_length=100, verbose_name="Naturalidade:")
	usu_cpf = models.CharField(max_length=100, verbose_name="CPF:")
	usu_rg = models.CharField(max_length=100, verbose_name="RG:")
	usu_filiacao = models.CharField(max_length=600, verbose_name="Filiação:")
	usu_estado_civil = models.IntegerField(blank=True, null=True, verbose_name="Estado civil:", choices=USUARIO_ESTADO_CIVIL_CHOICES)
	usu_numero_filhos = models.IntegerField(verbose_name="Número de Filhos:")

	# Informações de Contato
	usu_endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço:")
	usu_telefone = models.CharField(max_length=100, verbose_name="Telefone:")
	usu_whatsapp = models.CharField(max_length=100, verbose_name="WhatsApp:")
	usu_telefone_residencial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telefone Residêncial:")
	usu_email = models.EmailField(max_length = 254, verbose_name="E-mail:") 

	# Informações Adicionais
	usu_escolaridade = models.IntegerField(blank=True, null=True, choices=USUARIO_ESCOLARIDADE_CHOICES, verbose_name="Escolaridade:")
	usu_area_de_formacao = models.CharField(max_length=200, blank=True, null=True, verbose_name="Área de Formação:")
	usu_facebook = models.CharField(max_length=100, blank=True, null=True, verbose_name="Facebook:")
	usu_instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Instagram:")

	# Informações internas do sitema
	usu_is_adm = models.BooleanField(default= False, verbose_name="Administrador do sistema?")
	usu_data_de_cadastro = models.DateTimeField(default=timezone.now)
	usu_ultima_atualizacao = models.DateTimeField(default=timezone.now)

	def get_estado_civil(self):
		return USUARIO_ESTADO_CIVIL_CHOICES[self.usu_estado_civil][1]

	def get_escolaridade(self):
		return USUARIO_ESCOLARIDADE_CHOICES[self.usu_escolaridade][1]

	def __str__(self):
		return self.usu_nome


class FamiliarContato(models.Model):
	fm_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name="Usuário:")
	fm_nome = models.CharField(max_length=100, verbose_name="Nome do Familiar:")
	fm_parentesco = models.CharField(max_length=100, verbose_name="Grau de Parentesco:")
	fm_telefone = models.CharField(max_length=100, verbose_name="Telefone:")

	def __str__(self):
		return self.fm_nome+" - "+self.fm_parentesco+" - "+self.fm_telefone


class Unidade(models.Model):
	unidade_nome = models.CharField(max_length=100, verbose_name='Local:')
	unidade_descricao = models.CharField(max_length=200, verbose_name='Descrição:')
	unidade_endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço:")
	unidade_foto = models.ImageField(upload_to='usuario_pictures/', blank=True, verbose_name="Foto do Local:")
	unidade_rbm = models.CharField(max_length=20, verbose_name="RBM (Região de Bombeiro Militar):", choices=[
		('1ª Região', "1ª Região"),
		('2ª Região', "2ª Região"), 
		('3ª Região', "3ª Região")
	])
	unidade_bbm = models.CharField(max_length=20, verbose_name="BBM (Batalhão de Bombeiro Militar):", choices=[
		('1º BBM', "1º BBM"),
		('2º BBM', "2º BBM"),
		('3º BBM', "3º BBM"),
		('4º BBM', "4º BBM"),
		('5º BBM', "5º BBM"),
		('6º BBM', "6º BBM"),
		('7º BBM', "7º BBM"),
		('8º BBM', "8º BBM"),
		('9º BBM', "9º BBM"),
		('10º BBM', "10º BBM"),
		('11º BBM', "11º BBM"),
		('12º BBM', "12º BBM"),
		('13º BBM', "13º BBM"),
		('14º BBM', "14º BBM"),
		('15º BBM', "15º BBM"),
	])

	def __str__(self):
		return self.unidade_nome + " - " + self.unidade_bbm

	
	