#!/usr/bin/env python
# coding: utf-8

# # Exercício de Programação 2: PageRank
# 
# <font color="red">**Prazo de submissão: 23:55 do dia 18/01/2021** </font>
# 
# 2020.2 Álgebra Linear Computacional - DCC - UFMG
# 
# Erickson e Fabricio
# 
# Instruções:
# * Antes de submeter suas soluções, certifique-se de que tudo roda como esperado. Primeiro, **reinicie o kernel** no menu, selecione Kernel$\rightarrow$Restart e então execute **todas as células** (no menu, Cell$\rightarrow$Run All)
# * **Apenas o arquivo .py deve ser submetido**. Você deve salvar o seu notebook em Python script (no menu, File $\rightarrow$ Download .py) e enviar o script Python no Ambiente de Programação Virtual.
# * **Preste bastante atenção nos nomes das variáveis e métodos** (irá estar em negrito), se elas estiverem diferentes do que foi pedido no exercício, *sua resposta será considerada incorreta pelo corretor automático*.
# * Os exercícios desse EP utilizam os conceitos do PageRank vistos em aula, inclusive o de *matrizes de transição*, porém, neste notebook em alguns exercícios as matrizes podem estar num formato **transposto** do que vimos em aula, ou seja, com os links de saída da página $i$ na linha $i$, ao invés da coluna (mais detalhes sobre isso no notebook).
# * Não deixe de preencher seu nome e número de matrícula na célula a seguir

# **Nome:** *Robert Garcia da Silva*
# 
# **Matrícula:** *2019436676*
# 
# * Todo material consultado na Internet deve ser referenciado (incluir URL).
# 
# Este trabalho está dividido em três partes:
#  * **Parte 0**: Esta parte não vale nota, mas é fundamental para entender o que se pede a seguir.
#  * **Parte 1**: Pagerank sem saltos aleatórios em grafo pequeno
#  * **Parte 2**: Pagerank (com saltos aleatórios) em grafo pequeno

# ## Parte 0: Revisão de conceitos
# 
# I. O **primeiro autovetor** (isto é, o autovetor associado ao maior autovalor em módulo) pode ser calculado rapidamente através do método da potência, desde que o *gap* entre o maior e o segundo maior autovalor (em módulo) seja grande. Uma implementação simples do método da potência é mostrada a seguir.

# In[13]:


import numpy as np

def powerMethod(A, niter=10):
    n = len(A)
    w = np.ones((n,1))/n
    for i in range(niter):
        w = A.dot(w)        
    return w


# 
# II. Dado um grafo $G=(V, E)$ com n vértices, podemos obter **uma matriz de transição** $A$ de tamanho $n \times n$ em que cada elemento $ij$ na matriz representa uma aresta direcionada do vértice $i$ para o vértice $j$. Por exemplo, para o seguinte grafo direcionado:
# 
# <img src='https://www.dropbox.com/s/wmk8v8worinoqk0/grafo-simples-2.PNG?raw=1'>
# 
# a matriz de transição seria:
# 
# $$
# A = 
# \begin{bmatrix}
# 0 & 1 & 0 & 0 & 0 \\ 
# 0 & 0 & 1 & 0 & 0 \\ 
# 1 & 0 & 0 & 1 & 0 \\ 
# 0 & 0 & 0 & 0 & 1 \\ 
# 0 & 1 & 0 & 0 & 0
# \end{bmatrix}
# $$
# 
# **Essa notação é um pouco diferente da que vimos em aula**, já que no vídeo e os slides as saídas de cada página eram dadas nas colunas, e não nas linhas. Mesmo com essa diferença, podemos realizar as mesmas operações que vimos em aula. Por exemplo: 
# 
# - Para multiplicar a matriz $A$ por um vetor, podemos usar por exemplo: $A^\top \textbf{v}$. Ou alternativamente podemos usar $\textbf{v}^\top A$.
# - Para obter a quantidade de links de saída, precisamos somar ao longo das linhas, ao invés das colunas.

# III. Dado um grafo $G=(V,E)$, podemos obter uma **matriz de probabilidade de transição** $P$ dividindo-se cada linha de $A$ pela soma dos elementos da linha. Seja $D$ a matriz diagonal contendo a soma das linhas de $A$. Temos que
# 
# $$
# P = D^{-1} \times A.
# $$

# IV. A matriz de probabilidade de transição $P$ de certos grafos direcionados satisfaz
# 
# $$
# v^\top P = v^\top \textrm{ou $P^\top v = v$},
# $$
# 
# onde $v$ é o primeiro autovetor de $P^\top$. A equação da direita é mais fácil de ser utilizada, pois ela tem a forma canônica $Ax=b$. Já a equação da esquerda é mais fácil de ser interpretada. Para todo $j=1,\ldots,n$,
# 
# $$
# \sum_{i=1} v_i P_{ij} = v_j \\
# \Rightarrow \sum_{i=1} v_i \frac{A_{ij}}{D_{ii}} = v_j \\
# \Rightarrow \sum_{i:(i,j) \in E} v_i \frac{1}{D_{ii}} = v_j
# $$
# 
# em que nesse último somatório, a soma se dá apenas aos vértices $i$ que possuem link para $j$, ou seja, a aresta $(i,j)$ pertence ao conjunto $E$ de arestas $i:(i,j) \in E$.

# V. Assuma que $v$ seja normalizado de forma que $\sum_j v_j = 1$. O PageRank (sem saltos) de um vértice $j$ é dado por $v_j$, onde $v$ é o primeiro autovetor de $P^\top$. Esta é uma maneira de medir sua relevância. A intuição da Equação $\sum_{i:(i,j) \in E} v_i /D_{ii} = v_j$ é que a relevância de $j$ é a soma das relevâncias dos vértices $i$ que apontam para $j$ normalizados pelos seus respectivos graus de saída.

# ## Parte 1: Pagerank sem saltos aleatórios em grafo pequeno
# 
# Considere o grafo a seguir composto por $n=4$ vértices e $m=8$ arestas. 
# <img src='https://www.dropbox.com/s/oxibt5daw1g4dw3/directedgraph.png?raw=1'>
# 
# Certifique-se de que encontrou as $m=8$ arestas.

# **1.1** Crie um numpy array chamado <b> A </b>, contendo a matriz de adjacência.

# In[14]:


#Insira seu código para a questão 1.1 aqui

import numpy as np

A = np.array([[0, 1, 1, 0],[0, 0, 1, 1], [0, 0, 0, 1],[1, 1, 1, 0]]); 

# 'A:'
print(A)


# **1.2** Escreva uma função chamada <b>matrizDeTransicao</b> que recebe como entrada uma matriz $n \times n$ e retorna a matriz de probabilidade de transição desta matriz. Aplique a função em <b>A</b> e armazene o resultado na variável <b>P</b>, e depois imprima <b>P</b>.

# In[15]:


#Insira seu código para a questão 1.2 aqui

import numpy as np

def matrizDeTransicao(M):
    matTransicao = np.array([])
    
    for line in M:
        sumLine = sum(line)
        matTransicao = np.append(matTransicao, line/sumLine)
    
    matTransicao = matTransicao.reshape(-1,len(M))
    return matTransicao


#solução alternativa

def matrizDeTransicao2(M):
    vdiag = []
    
    for line in M:
        vdiag.append(sum(line))
    
    D = np.diag(vdiag)
    P = np.matmul(np.linalg.inv(D), M)
    return P
    

    
P = matrizDeTransicao(A)
    
#'Matriz de Transicao P:\n'
print(P)
    


# **1.3** Use a função <i>np.linalg.eig</i> para calcular o primeiro autovetor de $P^\top$. Normalize o autovetor pela sua soma em uma variável chamada <b>autovec</b> e imprima o resultado. (Observação: os elementos do autovetor serão retornados como números complexos, mas a parte imaginária será nula e pode ser ignorada.)

# In[16]:


#Insira seu código para a questão 1.3 aqui


import numpy as np

autoVet, autoVec_ = np.linalg.eig(P.T)
autoVec_ = autoVec_[:,0] # auto vetor correspondendo ao autovalor autoVet[0]
#print(autoVec_)


autovec = autoVec_/sum(autoVec_)

#Autovec
print(autovec)

#References: 
#[1]https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html


# **1.4** Verifique que o método da potência aplicado a $P^\top$ retorna uma aproximação para o primeiro autovetor. Atribua o resultado retornado pelo método na variável <b> result_pm </b> e imprima-o.

# In[17]:


#Insira seu código para a questão 1.4 aqui

result_pm = powerMethod(P.T)

#result_pm
print(result_pm)


# **1.5** Implemente uma função <b>powerMethodEps(A, epsilon)</b> que executa o método da potência até que a condição de convergência $\|w_{t} - w_{t-1}\| < \epsilon$ seja atingida. Para a matriz $P^\top$ com $\epsilon=10^{-5}$, armazene o resultado do método da potência na variável <b>result_pm_eps</b> *(1.5.1)*, e o número de iterações na variável <b>nb_iters</b> *(1.5.2)*.
# 
# Imprima o resultado das duas variáveis.

# In[18]:


#Insira seu código para a questão 1.5 aqui

import numpy as np

def powerMethodEps(A, epsilon):
    n = len(A)
    w = np.ones((n,1))/n
    
    epNom = 1
    ninter = 0
    w0 = np.copy(w)
    
    while((epNom < epsilon) == False):
        w = A.dot(w)
        
        ep = (w - w0)
        epNom = np.linalg.norm(ep)
        w0 = np.copy(w)
        ninter += 1
        
    return np.array(w), ninter

result_pm_eps, nb_iters = powerMethodEps(P.T, 10e-5)


#result_pm_eps
print(result_pm_eps)

#nb_Iters
print(nb_iters)


#References: 
#[1]https://stackoverflow.com/questions/9171158/how-do-you-get-the-magnitude-of-a-vector-in-numpy
#[2]https://pt.wikipedia.org/wiki/M%C3%A9todo_das_pot%C3%AAncias


# ## Parte II: Pagerank (com saltos aleatórios) em grafo pequeno
# 
# Agora iremos modificar a matriz A de forma a:
#  * adicionar um novo vértice 4, e
#  * adicionar uma aresta de 3 para 4.
#  
# Obviamente a matriz de probabilidade de transição não está definida para a nova matriz $A$. Vértices que não possuem arestas de saída (como o vértice 4) são conhecidos como *dangling nodes*. Para resolver este e outros problemas, incluiremos a possibilidade de realizar saltos aleatórios de um vértice para qualquer outro vértice.
# 
# Em particular, assume-se que com probabilidade $\alpha$, seguimos uma das arestas de saída em $A$ e, com probabilidade $1-\alpha$ realizamos um salto aleatório, isto é, transicionamos do vértice $v$ para um dos $n$ vértices do grafo (incluindo $v$) escolhido uniformemente. Quando não existem *dangling nodes*, a nova matriz de probabilidade de transição é dada por
# 
# $$
# P = \alpha D^{-1} A + (1-\alpha) \frac{\mathbf{1}\mathbf{1}^\top}{n}
# $$
# 
# Quando existem *dangling nodes*, a única possibilidade a partir desses nós é fazer saltos aleatórios. Mais precisamente, se $i$ é um vértice sem arestas de saída, desejamos que a $i$-ésima linha de $P$ seja o vetor $[1/n,\ldots,1/n]$. Uma forma de satisfazer essa definição é preencher com 1's as linhas de $A$ que correspondem aos *dangling nodes*. Uma desvantagem desta estratégia é que faz com que $A$ fique mais densa (mais elementos não-nulos).
# 
# Um valor típico usado para $\alpha$ é $0.85$.

# **2.1** Crie um novo numpy array chamado <b> A_new </b> contendo o vértice 4 e a aresta (3,4).

# In[19]:


#Insira seu código para a questão 2.1 aqui


import numpy as np

A_new = np.array([[0, 1, 1, 0,0],[0, 0, 1, 1,0], [0, 0, 0, 1,0],[1, 1, 1, 0,1],[0,0,0,0,0]]); 

# 'A:'
print(A_new)


# **2.2** Crie uma função **fixDangling(M)** que retorna uma cópia modificada da matriz de adjacência **M** onde cada *dangling node* do grafo original possui arestas para todos os vértices do grafo. *Dica:* Você pode criar um vetor $d$ com os graus de saída e acessar as linhas de $M$ correpondentes aos *dangling nodes* por $M[d==0,:]$. Imprima uma nova matriz chamada **A_fixed** retornada após chamar *fixDangling* para **A_new**.  

# In[20]:


#Insira seu código para a questão 2.2 aqui

import numpy as np

def fixDangling(M):
    M_fixed = np.array([])
    M_len = len(M)

    for line in M:
        for col in range(M_len):
            if(line[col] != 0):
                M_fixed = np.append(M_fixed, line)
                break
            if(col == M_len-1):
                M_fixed = np.append(M_fixed, line+1)

    M_fixed = M_fixed.reshape(-1,M_len)
    return M_fixed
    
A_fixed = fixDangling(A_new)

#A_fixed
print(A_fixed)


# **2.3** Crie uma função **matrizDeTransicao(M, alpha)** que receba como parâmetro também a probabilidade *alpha* de não fazermos um salto aleatório. Você pode assumir que **M** foi retornada por *fixDanglig*, logo, não possui *dangling nodes*. Imprima as matrizes:
#  * *(2.3.1)* **P_2** obtida ao chamar *matrizDeTransicao* para os parâmetros **A** e **alpha**=$0.85$;
#  * *(2.3.2)* **P_new** obtida ao chamar matrizDeTransicao para os parâmetros **A_fixed** e **alpha**=$0.85$.

# In[21]:


#Insira seu código para a questão 2.3 aqui

import numpy as np

def matrizDeTransicao(M, alpha):
    vDiag = []
    n = len(M)
    
    for line in M:
        vDiag.append(sum(line))
        D = np.diag(vDiag)

    D_inv = np.linalg.inv(D)
    
    P = np.matmul(alpha*D_inv,M) + ((1-alpha)/n)*(np.ones((n,n)).T)
    return P

P_2 = matrizDeTransicao(A, 0.85);
P_new = matrizDeTransicao(A_fixed, 0.85)

# Display out

#P_2
print(P_2, end='\n\n\n')

#P_new
print(P_new)


# **2.4** Armazene, respectivamente, o resultado do método da potência com:
# * *(2.4.1)* $P_2^\top$ e $\epsilon=10^{-5}$
# * *(2.4.2)* $P_\textrm{new}^\top$ e $\epsilon=10^{-5}$.
# 
# nas variáveis **pm_eps_P2** e **pm_eps_Pnew**; 

# In[29]:


#Insira seu código para a questão 2.4 aqui

pm_eps_P2, _ = powerMethodEps(P_2.T, 10e-5)
pm_eps_Pnew, _ = powerMethodEps(P_new.T, 10e-5)

print(pm_eps_P2, end='\n\n')
print(pm_eps_Pnew)


# **2.5** Sejam $i_\max$ e $i_\min$ os índices dos vértices com maior e menor PageRank de **A_fixed**. Vamos verificar como a adição de um novo link pode ajudar a promover uma página web (vértice). Adicione uma aresta do vértice $i_\max$ para o vértice $i_\min$ (se já houver aresta, aumente de 1 para 2 o elemento da matriz de adjacência). Salve o valor do novo pagerank na variável **new_pagerank**. Qual é o novo pagerank de $i_\min$?

# In[30]:


#Insira seu código para a questão 2.5 aqui

#Adicionando do vértice 3 para o vértice 0
Anew_fixed = np.copy(A_fixed); Anew_fixed[3,0] += 1
P2_new = matrizDeTransicao(Anew_fixed, 0.85)
new_pagerank, _ = powerMethodEps(P2_new.T, 10e-5)

print(new_pagerank)

#O novo valor do pagerank de imin é aproximadamente 0.16


# In[24]:



#Referencias Gerais
#[1]https://pt.wikipedia.org/wiki/PageRank
#[2]https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html
#[3]https://numpy.org/doc/stable/reference/generated/numpy.ones.html
#[4]https://pt.wikipedia.org/wiki/M%C3%A9todo_das_pot%C3%AAncias
#[5]https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html
#[6]https://pt.wikipedia.org/wiki/Matriz_de_adjac%C3%AAncia
