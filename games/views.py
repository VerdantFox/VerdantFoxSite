from django.shortcuts import render
from django.http import HttpResponse
from .models import Video
from .connect4 import Player, Grid, AI


def home(request):
    return render(request, 'games/games_index.html')


def twisted_towers(request):
    # ttvideo = Video.objects.get(name__exact='twisted_towers')

    return render(request, 'games/twisted_towers.html')


def moth_hunt(request):
    return render(request, 'games/moth_hunt.html')


def connect_4(request):
    return render(request, 'games/connect_4.html')


def ajax_connect_4(request):
    p1 = Player('red', 'Bob', turn=True)
    p2 = Player('blue', 'I am robot')
    board = Grid(p1, p2)
    robot = AI(ai=p2, opponent=p1, grid=board, Grid=Grid)

    board.grid[1][2] = 'green'

    board.show_grid()


    # while True:
    #     print(f"{board.current_player.name} ({board.current_player.color})'s "
    #           f"turn.")
    #
    #     # Initialize row and column choices to None
    #     row_choice, column_choice = None, None
    #     # Get column choice from player
    #     while not column_choice:
    #         if board.current_player == p1:
    #             try:
    #
    #                 column_choice = int(
    #                     input(f'{board.current_player.color}, '
    #                           f'please select a column_choice: '))
    #                 if 0 <= column_choice <= 6:
    #                     row_choice = board.check_bottom(column_choice)
    #                     if row_choice is None:
    #                         print(f"column_choice {column_choice} is full")
    #                         column_choice = None
    #                 else:
    #                     print("column_choice number must be an integer "
    #                           "between 0 and 6")
    #                     column_choice = None
    #             except ValueError:
    #                 print("Must input integer for column_choice number")
    #         elif board.current_player == p2:
    #             column_choice = robot.decide_move()
    #             row_choice = board.check_bottom(column_choice)
    #
    #     print()
    #     print(f"{board.current_player.color} played in column {column_choice}")
    #     board.change_color(row_choice, column_choice,
    #                        board.current_player.color)
    #     winner = board.check_winner()
    #     board.show_grid()
    #
    #     if winner:
    #         print(f"{board.current_player.color} got a {winner}.")
    #         break
    #     else:
    #         board.change_turn()

    return render(request, 'games/ajax_connect_4.html',
                  {'board': board})
