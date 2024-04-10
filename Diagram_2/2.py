import csv
import pandas as pd

def piece_name(piece):
    if piece == "P":
        return "Pawn"
    elif piece == "K":
        return "King"
    elif piece == "Q":
        return "Queen"
    elif piece == "N":
        return "Knight"
    elif piece == "R":
        return "Rook"
    elif piece == "B":
        return "Bishop"
    else:
        return piece

def parse_chess_moves(moves):
    parsed_moves = []
    move_count = 0
    for move in moves.split():
        # Remove '+' or '#' symbols if they exist
        move = move.rstrip('+#')
        move_count += 1
        player = "player1" if move_count % 2 != 0 else "player2"
        # Check for castling
        if move == "0-0" or move == "O-O":
            piece = "K"  # King
            origin = "e1" if move == "0-0" else "e8"
            destination = "g1" if move == "0-0" else "g8"
        elif move == "0-0-0" or move == "O-O-O":
            piece = "K"  # King
            origin = "e1" if move == "0-0-0" else "e8"
            destination = "c1" if move == "0-0-0" else "c8"
        else:
            piece = move[0]
            # Replace lowercase letters with 'P' (Pawn)
            if piece.islower():
                piece = "P"
            destination = move[-2:]
            if 'x' in move:
                start_idx = move.index('x') + 1
            else:
                start_idx = 1
            origin = move[start_idx:-2]
        parsed_moves.append((piece_name(piece), destination, player))
    return parsed_moves

def write_parsed_moves_to_csv(parsed_moves, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Piece', 'To', 'Player']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for move in parsed_moves:
            writer.writerow({'Piece': move[0], 'To': move[1], 'Player': move[2]})
    print(f"CSV file '{filename}' has been generated successfully.")

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('../games.csv')

# Extract the moves from the fourth row
moves_from_df = df['moves'].iloc[3]  # 3 for the third row (0-indexed)

# Parse moves from the CSV format
parsed_moves_from_csv = parse_chess_moves(moves_from_df)

# Write parsed moves from CSV to a new CSV file
write_parsed_moves_to_csv(parsed_moves_from_csv, 'parsed_moves_from_csv.csv')
