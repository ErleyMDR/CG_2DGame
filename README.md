# RTCB — Real Time Card Battle

Jogo 2D criado para avaliação da cadeira de **Computação Gráfica**.

O RTCB é um jogo de combate em tempo real em que o jogador controla um gladiador numa arena e usa um baralho de cartas para atacar, lançar magias e se defender. Diferente de um jogo de cartas por turnos, aqui as ações acontecem ao mesmo tempo e uma jogada pode ser interrompida pela resposta do adversário.

Link para vídeo da execução: <https://drive.google.com/file/d/1BGX39ofw8ufHUC_TGd073rQM3X3N1HNx/view?usp=sharing>

---

## Mecânicas

### Movimentação

O gladiador anda livremente pelo chão da arena e o sprite espelha conforme a direção horizontal. Os limites do chão acompanham a perspectiva (um trapézio). Um minimapa no canto da tela mostra a posição do personagem.

### O baralho

Cada jogador possui um baralho de **30 cartas**:

| Tipo | Quantidade | Função |
|---|---|---|
| **Ataque** (vermelha) | 12 | Golpe físico |
| **Magia** (azul) | 10 | Magia de **Fogo**, **Gelo** ou **Trovão** |
| **Defesa** (verde) | 8 | Postura defensiva |

Cada carta tem um **valor de 0 a 9**, impresso no centro. Todo baralho contém pelo menos uma carta de cada valor.

O baralho é **circular**. A carta selecionada fica em destaque no centro, elevada, com a carta anterior à esquerda e a seguinte à direita. O jogador navega pelas cartas e escolhe qual jogar.

### Como as cartas funcionam

1. **Jogar uma carta:** a carta selecionada sai do baralho imediatamente e passa a ser uma **carta ativa**, uma ação em andamento (ataque, magia ou defesa) com sua animação.
2. **Efeito atrasado:** o efeito da carta (dano, por exemplo) só é aplicado quando a ação **chega ao fim**. Iniciar um ataque não tira vida na hora.
3. **Janela de resposta:** enquanto a carta está ativa, o adversário pode jogar uma carta para **quebrá-la**.
4. **Carta quebrada:** a ação é **interrompida**, a animação é cancelada, o personagem volta ao estado normal e o efeito **nunca chega a acontecer**. Nenhum dano é aplicado e nada precisa ser desfeito.
5. **Carta não quebrada:** a ação termina normalmente e o efeito é resolvido.

Como a carta é gasta ao ser jogada, ela só volta ao jogo quando o baralho é **recarregado**.

### Quando uma carta quebra a outra

A comparação é feita entre a carta que acabou de ser jogada e a carta ativa do adversário:

- Normalmente, a carta de **maior valor** quebra a de menor valor.
- Cartas de **mesmo valor** não se quebram.
- O **0 é especial** e depende da **ordem em que as cartas foram jogadas**:
    - um **0 jogado depois** da carta do adversário a quebra, **independentemente do valor** dela;
    - um **0 jogado antes** vale como o menor valor possível e perde para qualquer outra carta jogada depois.

| Carta ativa | Carta nova | Resultado |
|:-:|:-:|---|
| 5 | 7 | o 7 quebra o 5 |
| 7 | 5 | o 5 não quebra o 7 |
| 5 | 0 | o 0 quebra o 5 |
| 0 | 5 | o 5 quebra o 0 |
| 0 | 0 | o segundo 0 quebra o primeiro |

### Vida

Cada combatente tem uma barra de HP ligada diretamente à vida atual. Quando o HP chega a zero, o personagem fica imóvel, tomba para o lado oposto ao que olhava e a tela de **GAME OVER** aparece, retornando depois ao menu.

---

## Controles

| Tecla | Ação |
|---|---|
| `W` `A` `S` `D` | Mover o gladiador |
| `Q` / `E` | Selecionar a carta anterior / seguinte |
| `Espaço` | Jogar a carta selecionada |
| `Esc` | Voltar (na tela de controles do menu) |
| `Ctrl` + `D` | Ativar/desativar o modo debug (FPS) |
| `Ctrl` + `F` | Debug: zera o HP do jogador |

---

## Computação gráfica

O trabalho exige que a parte gráfica seja implementada manualmente. O Pygame é usado apenas para criar a janela, tratar eventos, carregar imagens, acessar pixels (`set_at` / `get_at`) e exibir as superfícies na tela (`blit`).

Foram implementados à mão:

- **Primitivas:** retas (Bresenham e DDA), polígonos, círculos e elipses (algoritmos do ponto médio), retângulos e triângulos.
- **Preenchimento:** `flood_fill`, `scanline_fill`, preenchimento com gradiente de cor (círculos, elipses e polígonos) e preenchimento com **textura** por interpolação de coordenadas UV (usado nas cartas).
- **Recorte:** algoritmo de **Cohen-Sutherland** para recorte de retas.
- **Transformações geométricas:** translação, escala, rotação e composição por matrizes 3×3 (coordenadas homogêneas), usadas na conversão mundo → viewport do minimapa e na rotação do personagem ao morrer.
- **Transformações de imagem:** escala e espelhamento de sprites pixel a pixel.
- **Animação:** sprites animados por spritesheet e cenário com elementos animados.

---

## Como executar

### Requisitos

- **Python 3.12 ou superior**
- Uma tela com resolução de pelo menos **1820 × 920** (tamanho da janela do jogo)

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
```

### 2. (Recomendado) Criar um ambiente virtual

```bash
python -m venv venv
```

Ativar no Linux/macOS:

```bash
source venv/bin/activate
```

Ativar no Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

As dependências são `pygame-ce` e `numpy`.

### 4. Executar o jogo

Execute a partir da **raiz do projeto**, para que os caminhos relativos de `assets/` sejam encontrados:

```bash
python main.py
```