from django.shortcuts import render
from django.http import HttpResponse
from .models import Video
from .connect4 import Player, Grid, AI, set_game


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
    (p1, p2, board, robot, message, error, deactivate, restart,
     p1_col, p1_row, p2_col, p2_row, p1_move_msg, p2_move_msg) = set_game()

    if request.method == "POST":
        # Restart if restart button hit (ie. return without updating board)
        if request.POST['ic-trigger-name'] == 'restart':
            return render(request, 'games/ajax_connect_4.html',
                          {'board': board,
                           'message': message,
                           'error': error,
                           'deactivate': deactivate,
                           'p1_row': p1_row, 'p1_col': p1_col,
                           'p2_row': p2_row, 'p2_col': p2_col,
                           'p1_move_msg': p1_move_msg,
                           'p2_move_msg': p2_move_msg,
                           })

        # Iterate over post items to update board circles
        for item in request.POST:
            # Get each individual post item and check if it's a circle
            if item[:7] == "circle-":
                # Pull out circle's row and column index numbers
                row, column = item[7:].split(',')
                row, column = int(row), int(column)
                # Update grid from post data
                board.grid[row][column] = request.POST[item]

        # Get chosen column (from button click)
        p1_col = int(request.POST['ic-element-name'])
        p1_row = board.check_bottom(p1_col)
        # Check if move is legal
        if p1_row is None:
            error = f"Column {p1_col} is full! Try somewhere else!"
            # Send render again so user can re-pick
            return render(request, 'games/ajax_connect_4.html',
                          {'board': board,
                           'message': message,
                           'error': error,
                           'deactivate': deactivate,
                           'p1_row': p1_row, 'p1_col': p1_col,
                           'p2_row': p2_row, 'p2_col': p2_col,
                           'p1_move_msg': p1_move_msg,
                           'p2_move_msg': p2_move_msg,
                           })
        # Move was legal
        else:
            board.change_color(p1_row, p1_col, p1.color)
            winner = board.check_winner()
            p1_move_msg = f"You moved into column {p1_col}"
            # End game with win message if player wins
            if winner:
                board.change_win_colors(winner, p1.color)
                message = f"You won!"
                p2_row, p2_col, p2_move_msg = None, None, None
                deactivate = True
                return render(request, 'games/ajax_connect_4.html',
                              {'board': board,
                               'message': message,
                               'error': error,
                               'deactivate': deactivate,
                               'p1_row': p1_row, 'p1_col': p1_col,
                               'p2_row': p2_row, 'p2_col': p2_col,
                               'p1_move_msg': p1_move_msg,
                               'p2_move_msg': p2_move_msg,
                               })
            # Else just change turn
            else:
                board.change_turn()

        # Mr. Roboto's turn, he makes a move
        p2_col = robot.decide_move()
        # Get the row for his column
        p2_row = board.check_bottom(p2_col)
        # Update move color
        board.change_color(p2_row, p2_col, p2.color)
        # Update Mr. Roboto's move message
        p2_move_msg = f"Mr. Roboto moved into column {p2_col}"
        # Check for winner
        winner = board.check_winner()
        # End game with lose message if Mr. Roboto wins
        if winner:
            message = f"Mr. Roboto won!"
            board.change_win_colors(winner, p2.color)
            deactivate = True
            return render(request, 'games/ajax_connect_4.html',
                          {'board': board,
                           'message': message,
                           'error': error,
                           'deactivate': deactivate,
                           'p1_row': p1_row, 'p1_col': p1_col,
                           'p2_row': p2_row, 'p2_col': p2_col,
                           'p1_move_msg': p1_move_msg,
                           'p2_move_msg': p2_move_msg,
                           })
        # Else just change turn
        else:
            board.change_turn()

        return render(request, 'games/ajax_connect_4.html',
                      {'board': board,
                       'message': message,
                       'error': error,
                       'deactivate': deactivate,
                       'p1_row': p1_row, 'p1_col': p1_col,
                       'p2_row': p2_row, 'p2_col': p2_col,
                       'p1_move_msg': p1_move_msg,
                       'p2_move_msg': p2_move_msg,
                       })

    return render(request, 'games/ajax_connect_4.html',
                  {'board': board,
                   'message': message,
                   'error': error,
                   'deactivate': deactivate,
                   'p1_row': p1_row, 'p1_col': p1_col,
                   'p2_row': p2_row, 'p2_col': p2_col,
                   'p1_move_msg': p1_move_msg,
                   'p2_move_msg': p2_move_msg,
                   })
