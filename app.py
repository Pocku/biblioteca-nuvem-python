# Frontend
import database
import globals

from flet import *
from enum import Enum
from enum import StrEnum
from datetime import datetime, timedelta

from globals import BookStatus
from globals import DATE_FORMAT

class Pages(Enum):
    PAGINA_INICIAL = 0
    CADASTRAR_LIVRO = 1
    TODOS_OS_LIVROS = 2
    PROCURAR_LIVRO = 3
    LIVROS_EMPRESTADOS = 4
    LIVROS_PENDENTES = 5
    LIVRO_INFORMACOES = 6
    LIVRO_PREPARANDO_PARA_EMPRESTAR = 7
    LIVRO_EDITANDO_INFORMACOES = 8
    LIVRO_DEVOLVER_CONFIRMACAO = 9
    LIVRO_EXCLUIR_CONFIRMACAO = 10

PLACEHOLDER_IMAGE_SRC = 'https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM='
GENEROS = [
    'Ficção',
    'Romance',
    'Fantasia',
    'Ficção científica',
    'Mistério',
    'Suspense',
    'Aventura',
    'Não-ficção',
    'Biografias',
    'Autobiografias',
    'Ensaios',
    'História',
    'Ciências',
    'Autoajuda',
    'Literatura Infantil',
    'Contos de fadas',
    'Livros ilustrados',
    'Literatura juvenil',
    'Poesia',
    'Poemas',
    'Antologias',
    'Drama',
    'Peças de teatro',
    'Roteiros',
    'HQs e Graphic Novels',
    'Mangás',
    'Quadrinhos',
    'Clássicos',
    'Obras renomadas da literatura',
    'Terror',
    'Histórias de horror',
    'Suspense psicológico',
    'Romance',
    'Romance Erótico',
    'Literatura Fantástica',
    'Mundos imaginários',
    'Mitologias',
]

current_book = ''

def main(page: Page):
    page.title = 'Biblioteca'
    page.theme_mode = 'light'
    page.theme = Theme(color_scheme_seed='green')
    page.appbar = AppBar(
        title = Row(
            expand = True,
            controls = [
                Text('Biblioteca', size = 24),
                Text(str(database.userdata['Collection']['name']).replace('"', ""), size = 16, color = colors.GREEN, expand = True, text_align = TextAlign.RIGHT)
            ]
        ),
        bgcolor = colors.GREEN_50,
        leading = Icon(icons.BOOKMARK),
    )

    def on_navigation_rail_changed(event):
        index = event.control.selected_index
        change_page_to(index)

    def change_page_to(index):
        # Pegamos a index do button pressionado
        body = Row()

        # Removemos a cena anterior
        root.controls.pop(1)
        root.update()

        match int(index):
            case Pages.PAGINA_INICIAL.value:
                body = Row(
                    expand = True,
                    alignment = MainAxisAlignment.CENTER,
                    controls = [
                        Container(
                            content = Column(
                                expand = True,
                                alignment = MainAxisAlignment.CENTER,
                                controls = [
                                    Text(value = 'Livros Cadastrados', size = 16, width = 240, text_align = TextAlign.CENTER),
                                    Text(value = f'{database.get_books_total()}', width = 240, size = 42, color = colors.GREEN_600, text_align = TextAlign.CENTER)
                                ]
                            ),
                            width = 240, 
                            height = 240, 
                            border = border.all(2, colors.BLACK),
                            border_radius = 16,
                        ),
                        Container(
                            content = Column(
                                expand = True,
                                alignment = MainAxisAlignment.CENTER,

                                controls = [
                                    Text(value = 'Livros emprestados:', size = 16, width = 240, text_align = TextAlign.CENTER),
                                    Text(value = f'{len(database.get_borrowed_books())}', width = 240, size = 42, color = colors.GREEN_600, text_align = TextAlign.CENTER)
                                ]
                            ),
                            width = 240, 
                            height = 240, 
                            border = border.all(2, colors.BLACK),
                            border_radius = 16,
                        ),
                        Container(
                            content = Column(
                                expand = True,
                                alignment = MainAxisAlignment.CENTER,

                                controls = [
                                    Text(value = 'Livros pendentes:', size = 16, width = 240, text_align = TextAlign.CENTER),
                                    Text(value = f'{len(database.get_pendent_books())}', width = 240, size = 42, color = colors.RED_600, text_align = TextAlign.CENTER)
                                ]
                            ),
                            width = 240, 
                            height = 240, 
                            border = border.all(2, colors.BLACK),
                            border_radius = 16,
                        )
                    ]
                )

            case Pages.TODOS_OS_LIVROS.value:
                list = ListView(expand = True, padding = 10)

                def on_book_button_arrow_pressed(event):
                    # Maneira mais simples e suja de pegar o id do livro, é um objeto invisivel contendo o id como texto, deve ser a decima vez q eu to copiando esse codigo, Deus me perdoe
                    globals.current_book_id = event.control.parent.controls[4].value
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def create_book_button(book):
                    item = Row(
                        expand = True,
                        controls = [
                            IconButton(icon = icons.KEYBOARD_ARROW_RIGHT, on_click = on_book_button_arrow_pressed),
                            Text(book['data']['nome']),
                            Text(' - '),
                            Text(book['data']['autor']),
                            Text(book['id'], visible = False)
                        ]
                    )
                    list.controls.append(item)

                def create_all_book_buttons():
                    for data in database.get_latest_books_in_collection():
                        create_book_button(data)

                body = Column(
                    expand = True,
                    alignment = MainAxisAlignment.START,
                    controls = [
                        Container(
                            expand = True,
                            content = list,
                            border = border.all(1, colors.BLACK)
                        )
                    ]
                )
                create_all_book_buttons()

            case Pages.LIVRO_PREPARANDO_PARA_EMPRESTAR.value:
                def on_confirm_button_pressed(event):
                    parent = event.control.parent
                    children = parent.controls

                    prazo_em_dias = int(children[3].value)

                    now = datetime.now()
                    current_date = now.strftime(DATE_FORMAT)
                    future_date = (now + timedelta(days = prazo_em_dias)).strftime(DATE_FORMAT)

                    usuario = {
                        'nome': children[1].value,
                        'turma': children[2].value,
                        'prazo': children[3].value,
                        'dia_registrado': current_date,
                        'dia_prazo': future_date
                    }
                    
                    # Pegamos o livro atual e atualizamos a área sobre o usuario com os novos dados coletados
                    book = database.get_book(globals.current_book_id)
                    book['status'] = BookStatus.EMPRESTADO
                    book['usuario'] = usuario
                    database.edit_book(globals.current_book_id, book)

                    # Redirecinamos para a página do livro para mostrar as informações atuais
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def on_exit_button_pressed():
                    pass

                days = []
                for i in range(1, 30):
                    option =  dropdown.Option(f'{i}')
                    days.append(option)

                body = Row(
                    expand = True,
                    alignment = MainAxisAlignment.CENTER,
                    controls = [
                        Container(expand = True),
                        Column(
                            expand = True,
                            alignment = MainAxisAlignment.CENTER,
                            controls = [
                                Text('Informações sobre o usuário', text_align = TextAlign.LEFT, size = 24, width = 320),
                                TextField(label='Nome', hint_text = 'Insira o nome do usuário aqui'),
                                TextField(label='Turma', hint_text = 'Ex: 9° Ano - Tarde'),
                                Dropdown(
                                    label = 'Prazo em dias',
                                    hint_text = 'Prazo em dias',
                                    value = '1',
                                    options = days
                                ),
                                Container(height = 12),
                                OutlinedButton(text = 'Emprestar livro', width = 640, icon = icons.FACT_CHECK_OUTLINED, on_click = on_confirm_button_pressed),
                                OutlinedButton(text = 'Cancelar e voltar', width = 640, icon = icons.EXIT_TO_APP, on_click = on_exit_button_pressed)
                            ], 
                        ),
                        Container(expand = True)
                    ]
                )
                pass

            case Pages.LIVRO_EXCLUIR_CONFIRMACAO.value:
                def on_confirm_button_pressed(event):
                    database.delete_book(globals.current_book_id)
                    change_page_to(Pages.TODOS_OS_LIVROS.value)

                def on_cancel_button_pressed(event):
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                body = Row(
                    expand = True,
                    alignment = MainAxisAlignment.CENTER,
                    controls = [
                        Column(
                            alignment = MainAxisAlignment.CENTER,
                            controls = [
                                Text('Tem certeza que deseja deletar este livro?'),
                                TextButton(text = 'Sim', width = 260, icon = icons.CHECK_CIRCLE_OUTLINE_OUTLINED, on_click = on_confirm_button_pressed),
                                TextButton(text = 'Não', width = 260, icon = icons.WARNING_AMBER_ROUNDED, on_click = on_cancel_button_pressed)
                            ]
                        )
                    ]
                )

            case Pages.LIVRO_DEVOLVER_CONFIRMACAO.value:
                def on_confirm_button_pressed(event):
                    # Alteramos o status atual do livro e removemos os dados sobre o usuario anterior
                    book = database.get_book(globals.current_book_id)
                    book['status'] = BookStatus.DISPONIVEL
                    book['usuario'] = {}
                    database.edit_book(globals.current_book_id, book)
                    
                    # Voltamos a pagina que contem todos os livros
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def on_cancel_button_pressed(event):
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                body = Row(
                    expand = True,
                    alignment = MainAxisAlignment.CENTER,
                    controls = [
                        Column(
                            alignment = MainAxisAlignment.CENTER,
                            controls = [
                                Text('Tem certeza que deseja devolver este livro?'),
                                TextButton(text = 'Sim', width = 260, icon = icons.CHECK_CIRCLE_OUTLINE_OUTLINED, on_click = on_confirm_button_pressed),
                                TextButton(text = 'Não', width = 260, icon = icons.WARNING_AMBER_ROUNDED, on_click = on_cancel_button_pressed)
                            ]
                        )
                    ]
                )
                pass

            case Pages.LIVRO_INFORMACOES.value:
                def on_lend_book_button_pressed(event):
                    change_page_to(Pages.LIVRO_PREPARANDO_PARA_EMPRESTAR.value)
                    pass

                def on_return_book_button_pressed(event):
                    change_page_to(Pages.LIVRO_DEVOLVER_CONFIRMACAO.value)

                def on_edit_book_information_button_pressed(event):
                    pass

                def on_delete_book_button_pressed(event):
                    change_page_to(Pages.LIVRO_EXCLUIR_CONFIRMACAO.value)

                def on_return_page_button_pressed(event):
                    change_page_to(Pages.PROCURAR_LIVRO.value)

                book = database.get_book(globals.current_book_id)
                nome = book['nome']
                autor = book['autor']
                genero = book['genero']
                sinopse = book['sinopse']
                condicao = book['condicao']
                capa_url = book['capa_url']
                status = book['status']
                data_publicacao = book['data_publicacao']

                usuario = book['usuario']
                usuario_content = Column()
                action_button = Container()

                if usuario:
                    usuario_content.controls = [
                        Row(
                            controls = [
                                Icon(name = icons.PERSON),
                                Text('Atualmente nas mãos de:', size = 20)
                            ]
                        ),
                        Text(f'Nome: {usuario['nome']}\nTurma: {usuario['turma']}\nDia registrado: {usuario['dia_registrado']}\nPrazo para devolver: {usuario['dia_prazo']}', size = 16)
                    ]
                    action_button = TextButton(text = 'Devolver livro', icon = icons.WAVING_HAND, on_click = on_return_book_button_pressed)
                
                if not usuario:
                    action_button = TextButton(text = 'Emprestar livro', icon = icons.HANDSHAKE, on_click = on_lend_book_button_pressed)

                body = Row(
                    expand = True,
                    alignment = MainAxisAlignment.SPACE_AROUND,
                    controls = [
                        Row(
                            controls = [
                                Column(
                                    expand = True,
                                    alignment = MainAxisAlignment.CENTER,
                                    controls = [
                                        Image(
                                            src = capa_url,
                                            width = 320,
                                            height = 320,
                                            fit = ImageFit.SCALE_DOWN,
                                            repeat = ImageRepeat.NO_REPEAT,
                                        ),
                                    ]
                                ),
                                Container(width = 24),
                                Column(
                                    expand = True,
                                    alignment = MainAxisAlignment.CENTER,
                                    controls = [
                                        Row(
                                            controls = [
                                                IconButton(icon = icons.ARROW_BACK, on_click = on_return_page_button_pressed),
                                                Text(nome, size = 20)
                                            ]
                                        ),
                                        Text(f'Status: {status}\nAutor: {autor}\nGênero: {genero}\nData da publicação: {data_publicacao}\nCondição: {condicao}', size = 16),
                                        Container(height = 32),
                                        usuario_content,
                                        Container(height = 32),
                                        Row(
                                            controls = [
                                                action_button,
                                                #TextButton(text = 'Editar informações', icon = icons.EDIT, on_click = on_edit_book_information_button_pressed),
                                                TextButton(text = 'Deletar livro', icon = icons.DELETE, on_click = on_delete_book_button_pressed)
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )                

            case Pages.PROCURAR_LIVRO.value:
                list = ListView(expand = True, padding = 10)

                def create_book_button(book):
                    item = Row(
                        expand = True,
                        controls = [
                            IconButton(icon = icons.KEYBOARD_ARROW_RIGHT, on_click = on_book_button_arrow_pressed),
                            Text(book['data']['nome']),
                            Text(' - '),
                            Text(book['data']['autor']),
                            Text(book['id'], visible = False)
                        ]
                    )
                    list.controls.append(item)

                def create_all_book_buttons():
                    for data in database.get_latest_books_in_collection():
                        create_book_button(data)

                def on_search_book_text_field_changed(event):
                    input_text = event.data
                    list.controls.clear()
                    list.update()

                    if len(input_text) > 0:
                        for book in database.get_latest_books_in_collection():
                            if input_text.lower() in book['data']['nome'].lower():
                                create_book_button(book)
                        list.update()
                    else:
                        create_all_book_buttons()
                        list.update()

                def on_book_button_arrow_pressed(event):
                    # Maneira mais simples e suja de pegar o id do livro, é um objeto invisivel contendo o id como texto
                    globals.current_book_id = event.control.parent.controls[4].value
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def on_reload_button_pressed(event):
                    event.control.visible = False
                    event.control.update()

                    database.update()
                    list.controls.clear()
                    create_all_book_buttons()
                    list.update()
                    

                body = Column(
                    expand = True,
                    alignment = MainAxisAlignment.START,
                    controls = [
                        Row(
                            controls = [
                                IconButton(icon = icons.RESTART_ALT_OUTLINED, on_click = on_reload_button_pressed),
                                TextField(hint_text = 'Insira o texto aqui', expand  = True, on_change = on_search_book_text_field_changed),
                                IconButton(icon = icons.DELETE_ROUNDED)
                            ]
                        ),
                        Container(
                            expand = True,
                            content = list,
                            border = border.all(1, colors.BLACK)
                        )
                    ]
                )
                create_all_book_buttons()

            case Pages.LIVROS_EMPRESTADOS.value:
                list = ListView(expand = True, padding = 10)

                def on_book_button_arrow_pressed(event):
                    # Maneira mais simples e suja de pegar o id do livro, é um objeto invisivel contendo o id como texto
                    globals.current_book_id = event.control.parent.controls[5].value
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def create_book_button(book):
                    item = Row(
                        expand = True,
                        controls = [
                            IconButton(icon = icons.KEYBOARD_ARROW_RIGHT, on_click = on_book_button_arrow_pressed),
                            Icon(name = icons.BOOKMARK),
                            Text(book['data']['nome']),
                            Text(' - '),
                            Text(book['data']['autor']),
                            Text(book['id'], visible = False)
                        ]
                    )
                    list.controls.append(item)

                for book in database.get_borrowed_books():
                    create_book_button(book)

                if len(list.controls) > 0:
                    body = Column(
                        expand = True,
                        alignment = MainAxisAlignment.CENTER,
                        controls = [
                            Container(
                                expand = True,
                                content = list,
                                border = border.all(1, colors.BLACK)
                            )
                        ]
                    )
                else:
                    body = Row(
                        expand = True,
                        alignment = MainAxisAlignment.CENTER,
                        controls = [
                            Text('Não há livros emprestados!', size = 24)
                        ]
                    )

            case Pages.LIVROS_PENDENTES.value:
                list = ListView(expand = True, padding = 10)

                def on_book_button_arrow_pressed(event):
                    # Maneira mais simples e suja de pegar o id do livro, é um objeto invisivel contendo o id como texto
                    globals.current_book_id = event.control.parent.controls[5].value
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                def create_book_button(book):
                    item = Row(
                        expand = True,
                        controls = [
                            IconButton(icon = icons.KEYBOARD_ARROW_RIGHT, on_click = on_book_button_arrow_pressed),
                            Icon(name = icons.BOOKMARK),
                            Text(book['data']['nome']),
                            Text(' - '),
                            Text(book['data']['autor']),
                            Text(book['id'], visible = False)
                        ]
                    )
                    list.controls.append(item)

                for book in database.get_pendent_books():
                    create_book_button(book)

                if len(list.controls) > 0:
                    body = Column(
                        expand = True,
                        alignment = MainAxisAlignment.CENTER,
                        controls = [
                            Container(
                                expand = True,
                                content = list,
                                border = border.all(1, colors.BLACK)
                            )
                        ]
                    )
                else:
                    body = Row(
                        expand = True,
                        alignment = MainAxisAlignment.CENTER,
                        controls = [
                            Text('Não há livros emprestados!', size = 24)
                        ]
                    )

            case Pages.CADASTRAR_LIVRO.value:
                def on_new_book_image_url_changed(event):
                    url = event.data
                    parent = event.control.parent
                    image_control = parent.controls[1]
                    image_control.src = url
                    image_control.update()

                def register_new_book(event):
                    parent = event.control.parent
                    children = parent.controls
                    content = {
                        'nome': children[1].value,
                        'status': BookStatus.DISPONIVEL,
                        'autor': children[2].value,
                        'genero': children[3].value,
                        'data_publicacao': children[4].value,
                        'sinopse': children[5].value,
                        'condicao': children[6].value,
                        'capa_url': body.controls[5].controls[2].value,
                        'usuario' : {}
                    }
                    id = database.add_book(content)
                    globals.current_book_id = id
                    change_page_to(Pages.LIVRO_INFORMACOES.value)

                body = Row(
                    alignment = MainAxisAlignment.SPACE_AROUND,
                    expand = True
                )

                genero_options = []
                for id in GENEROS:
                    option = dropdown.Option(id)
                    genero_options.append(option)

                body.controls = [
                    Container(expand = True),
                    Column(
                        controls = [
                            Text('Informações', text_align = TextAlign.LEFT, size = 24, width = 320),
                            TextField(label='Nome', hint_text = 'Insira o nome do livro aqui'),
                            TextField(label='Autor', hint_text = 'Insira o nome do autor aqui'),
                            Dropdown(
                                label = 'Gênero',
                                hint_text = 'Qual o gênero do livro?',
                                options = genero_options
                            ),
                            TextField(label='Data da publicação', hint_text = 'Insira a data da publicação aqui'),
                            TextField(label='Sinopse', hint_text = 'Descreva a sinopse do livro aqui', multiline = True, min_lines = 1, max_lines = 10),
                            Dropdown(
                                label = 'Condição',
                                hint_text='Em qual condição o livro se encontra?',
                                options = [
                                    dropdown.Option('Novo'),
                                    dropdown.Option('Como Novo'),
                                    dropdown.Option('Muito Bom'),
                                    dropdown.Option('Bom'),
                                    dropdown.Option('Razoável'),
                                    dropdown.Option('Ruim'),
                                ]
                            ),
                            Container(height = 12),
                            OutlinedButton(text = 'Cadastrar', width = 320, icon = icons.POST_ADD, on_click = register_new_book)
                        ], 
                        expand = True,
                        alignment = MainAxisAlignment.CENTER
                    ),
                    Container(expand = False, width = 240),
                    VerticalDivider(1),
                    Container(expand = False, width = 240),
                    Column(
                        expand = True,
                        alignment = MainAxisAlignment.CENTER,
                        controls = [
                            Text('Capa do livro', text_align = TextAlign.LEFT, size = 24, width = 320),
                            Image(
                                src = PLACEHOLDER_IMAGE_SRC,
                                width = 320,
                                height = 320,
                                fit = ImageFit.SCALE_DOWN,
                                repeat = ImageRepeat.NO_REPEAT,
                            ),
                            TextField(label='Link da imagem', hint_text = 'Insira o link da imagem do livro.', on_change = on_new_book_image_url_changed, width = 320 ),
                        ]
                    ),
                    Container(expand = True)
                ]
        
        # Adicionamos a cena atual
        root.controls.append(body)
        root.update()

    navbar = NavigationRail(
        min_width = 120,
        min_extended_width = 400,
        label_type = NavigationRailLabelType.ALL,
        bgcolor = colors.GREEN_50,
        destinations = [
            NavigationRailDestination(
                icon = icons.HOME, selected_icon=icons.HOME_OUTLINED, label='Página inicial'
            ),
            NavigationRailDestination(
                icon = icons.LIBRARY_ADD, selected_icon=icons.LIBRARY_ADD_OUTLINED, label='Cadastrar livro'
            ),
            NavigationRailDestination(
                icon = icons.COLLECTIONS_BOOKMARK_ROUNDED, selected_icon=icons.COLLECTIONS_BOOKMARK_OUTLINED, label='Todos os livros'
            ),
            NavigationRailDestination(
                icon = icons.SEARCH, selected_icon=icons.SEARCH_OUTLINED, label='Procurar livro'
            ),
            NavigationRailDestination(
                icon = icons.MY_LIBRARY_BOOKS ,selected_icon=icons.MY_LIBRARY_BOOKS_OUTLINED, label='Livros Emprestados'
            ),
            NavigationRailDestination(
                icon = icons.REPORT ,selected_icon=icons.REPORT_OUTLINED, label='Livros Pendentes'
            ),
        ],
        on_change = on_navigation_rail_changed
    )

    # Tela de início padrão
    body = Row(expand = True)
    body.controls = [
        Text('Bem vindo!', size = 32, text_align = TextAlign.CENTER, expand = True)
    ]

    # Criamos o node principal
    root = Row([navbar, body], expand = True)

    # Adicionamos e atualizamos a página
    page.add(root)
    page.update()

    # Redirecionar para a página principal
    change_page_to(Pages.PAGINA_INICIAL.value)

# Boot
app(target = main)