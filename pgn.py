import argparse
import fileinput
import os
import sys

import pyffish as sf


PGN_HEADER = """
[Event "{}"]
[Result "*"]
[Variant "{}"]
[FEN "{}"]
[SetUp "1"]
"""


def epd_to_pgn(epd_stream, pgn_stream):
    for epd in epd_stream:
        tokens = epd.strip().split(';')
        fen = tokens[0]
        annotations = dict(token.split(' ', 1) for token in tokens[1:])
        variant = annotations['variant']
        pgn_stream.write(PGN_HEADER.format(annotations.get('type'), variant.capitalize(), fen))
        moves = annotations.get('pv', '').split(',')
        san_moves = sf.get_san_moves(variant, fen, moves)
        for i, san_move in enumerate(san_moves):
            cur_fen = sf.get_fen(variant, fen, moves[:i])
            fullmove = cur_fen.split(' ')[-1]
            whiteToMove = cur_fen.split(' ')[1] == 'w'
            movenum = '{}. '.format(fullmove) if whiteToMove else '{}... '.format(fullmove) if i == 0 else ''
            pgn_stream.write('{}{} '.format(movenum, san_move))
        pgn_stream.write('*{}'.format(os.linesep))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('epd_files', nargs='*')
    args = parser.parse_args()
    with fileinput.input(args.epd_files) as instream:
        epd_to_pgn(instream, sys.stdout)
