# %%
import pandas as pd


# %%
nomes_f = pd.read_json(
    "https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=f")
nomes_m = pd.read_json(
    "https://servicodados.ibge.gov.br/api/v1/censos/nomes/ranking?qtd=200&sexo=m")


# %%
nomes = pd.concat([nomes_f, nomes_m])['nome'].to_frame()


# %%
import numpy as np
np.random.seed(123)


# %%
total_alunos = len(nomes)
total_alunos


# %%
nomes['id_aluno'] = np.random.permutation(total_alunos)+1


# %%
dominios = ['@dominiodoemail.com.br', '@servicodoemail.com']


# %%
nomes['dominio'] = np.random.choice(dominios, total_alunos)
nomes['email'] = nomes['nome'].str.lower()+nomes['dominio']
nomes


# %%
import html5lib
url = 'http://tabela-cursos.herokuapp.com/index.html'
cursos = pd.read_html(url)
cursos = cursos[0]
cursos.head()


# %%
cursos.rename(columns={'Nome do curso': 'nome_do_curso'}, inplace=True)
cursos.head(5)


# %%
cursos['id'] = cursos.index + 1
cursos.head(5)


# %%
cursos.set_index('id', inplace=True)
cursos.head(5)


# %%
nomes['matriculas'] = np.ceil(
    np.random.exponential(size=total_alunos)*1.5).astype(int)


# %%
nomes.matriculas.describe().round(2)


# %%
grupos = nomes.groupby('matriculas')['nome']
grupos.count()
# nomes.matriculas.value_counts()


# %%
import seaborn as sns
sns.distplot(nomes['matriculas'])


# %%
nomes.sample(5)


# %%
cursos


# %%


# %%
todas_matriculas = []
x = np.random.rand(20)
prob = x / sum(x)

for index, row in nomes.iterrows():
    id = row.id_aluno
    matriculas = row.matriculas
    cont = 0
    cursos_aluno = []
    while cont < matriculas:
        curso = np.random.choice(cursos.index, p=prob)
        if(curso not in cursos_aluno):
            todas_matriculas.append([id, curso])
            cursos_aluno.append(curso)
            cont += 1

# for index, row in nomes.iterrows():
#     id = row.id_aluno
#     matriculas = row.matriculas
#     for i in range(matriculas):
#         mat = [id, np.random.choice(cursos.index, p = prob)]
#         todas_matriculas.append(mat)

matriculas = pd.DataFrame(todas_matriculas, columns=['id_aluno', 'id_cursos'])
matriculas


# %%
matriculas.groupby('id_cursos').count().join(cursos['nome_do_curso']).rename(
    columns={'id_aluno': 'quantidade_alunos'})


# %%
nomes.sample(3)


# %%
cursos.head()


# %%
matriculas_por_curso = matriculas.groupby('id_cursos').count().join(
    cursos['nome_do_curso']).rename(columns={'id_aluno': 'quantidade_alunos'})


# %%
matriculas_por_curso.head()


# %%
matriculas.head()


# %%
matriculas_por_curso.to_csv('matriculas_por_curso.csv', index=False)


# %%
dados = pd.read_csv('matriculas_por_curso.csv')
dados


# %%
matriculas_por_curso.to_json('matriculas.json')


# %%
matriculas_por_curso.to_html('matriculas.html')


# %% [markdown]
# # Criando o Banco SQL

# %%
from sqlalchemy import create_engine, MetaData, Table, inspect # adicionando o método inspect

# %%
engine = create_engine('sqlite:///:memory:')
print(engine)
print(type(engine))

# %%
matriculas_por_curso.to_sql('matriculas', engine)

# %%
inspector = inspect(engine) # criando um Inspector object
print(inspector.get_table_names()) # Exibindo as tabelas com o inspecto

# %% [markdown]
# # Buscando do Banco SQL

# %%
query = 'select * from matriculas where quantidade_alunos < 20'


# %%
pd.read_sql(query, engine)


# %%
muitas_matriculas = pd.read_sql_table('matriculas', engine, columns=[
                                      'nome_do_curso', 'quantidade_alunos'])


# %%
muitas_matriculas


# %%
muitas_matriculas = muitas_matriculas.query('quantidade_alunos > 70')


# %% [markdown]
# # Escrevendo no Banco SQL

# %%
muitas_matriculas.to_sql('muitas_matriculas', con=engine)


# %%
inspector = inspect(engine)
print(inspector.get_table_names())


# %%
print(engine.table_names())


# %% [markdown]
# # Escrevendo em Excel

# %% [markdown]
# ## Nome dos alunos da próxima aula

# %%
matriculas_por_curso.head()


# %%
id_curso = 16


# %%
proxima_turma = matriculas.query(f'id_cursos == {id_curso}')
proxima_turma.head()


# %%
proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))


# %%
proxima_turma.set_index('id_aluno').join(nomes.set_index('id_aluno'))['nome']


# %%
proxima_turma.set_index('id_aluno').join(
    nomes.set_index('id_aluno'))['nome'].to_frame()


# %%
alunos_curso_id = proxima_turma.set_index('id_aluno').join(
    nomes.set_index('id_aluno'))['nome'].to_frame().sort_values(by=['nome'])

alunos_curso_id.head()


# %%
nome_curso = cursos.loc[id_curso]
nome_curso = nome_curso.nome_do_curso
nome_curso

# %%
alunos_curso_id.rename(columns={'nome': 'Alunos do curso de {}'.format(nome_curso)},inplace=True)
alunos_curso_id

# %%
alunos_curso_id.to_excel('nomes_curso{}.xlsx'.format(id_curso),index=False)

# %%
pd.read_excel('nomes_curso{}.xlsx'.format(id_curso))

# %%



