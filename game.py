#! /bin/env python3

from api_file import *
import chess, time, chess.pgn, cairosvg
import pygame as pg


#----------------- Pygame stuff ----------------- 
pg.init()

SCREEN_W = 600
SCREEN_H = 600

SURF = pg.display.set_mode( (SCREEN_W, SCREEN_H) )

frameRate = pg.time.Clock()
#----------------- Pygame stuff ----------------- 

ref = "Stock Fish"

WHITE = "deepseek/DeepSeek-V3-0324"
BLACK = "openai/gpt-4o-mini"

board = chess.Board()
game = chess.pgn.Game()

game.headers["Event"] = "Test"
game.headers["White"] = WHITE
game.headers["Black"] = BLACK

# Creates a initial node for tracking moves into pgn
node = game

counter = 1
while( not board.is_game_over() and not board.is_repetition() ):

    for event in pg.event.get():
        if( event.type == pg.QUIT ): break

    board_state = board.fen()
    moves = [ board.san(i) for i in board.legal_moves ]

    prompt_str = ( f"You are playing chess as {ref}. "
                   f"Here is the current board state: '{board_state}'. "
                   f"Here is a list with the legal moves: {moves} "
                   f"Please pick just one best move for next board state. "
                   f"Tell the move without context. "
                   f"Do not repeat twice a position."
                  )

    if( (counter % 2) != 0 ):

        try:
            text = chat_llm( WHITE, prompt_str )
            node = node.add_variation( board.push_san(text) )
            print( "WHITE: " + text )
            
        except chess.InvalidMoveError: continue
        except KeyError:
            print( "Rate limit" )
            exit()
        
    else:

        try:
            text = chat_llm( BLACK, prompt_str )
            node = node.add_variation( board.push_san(text) )
            print( "BLACK: " + text )

        except chess.InvalidMoveError: continue
        except KeyError:
            print( "Rate limit" )
            exit()

    svg = chess.svg.board( board, size=500 )
    output = open( "img.svg", "w" )
    output.write( str(svg) )
    output.close()

    cairosvg.svg2png( url="img.svg", write_to="img.png" )

    image = pg.image.load( 'img.png' )
    SURF.blit( image, (0, 0) )

    pg.display.update()
    frameRate.tick(90)
    counter += 1
    time.sleep(5.0)

print( "***GAME OVER***" )
game.headers["Result"] = board.result()

output = open( "game.pgn", "w" )
output.write( str(game) )
output.close()
