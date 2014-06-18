#pragma once

#undef NDEBUG

#include <assert.h>
#include <math.h>
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <utility>

const int N = 8;

enum Cell {
    EMPTY = 0,
    BLACK = 1,
    WHITE = 2
};


typedef int Move;


class Position {
private:
    std::vector<Cell> cells;
    bool prev_skipped;

public:
    int move_number;

    Position() : cells(N * N), prev_skipped(false), move_number(0) {
        //std::cerr << "Position default constructor" << std::endl;
    }
    Position(const Position &other)
        : cells(other.cells),
          prev_skipped(false),
          move_number(other.move_number) {
        //std::cerr << "Position copy constructor" << std::endl;
    }
    void operator=(const Position &other) {
        //std::cerr << "Position assignment operator" << std::endl;
        cells = other.cells;
        prev_skipped = other.prev_skipped;
        move_number = other.move_number;
    }
    ~Position() {
        //std::cerr << "Position destructor" << std::endl;
    }

    Cell at(int i, int j) const {
        assert(0 <= i && i < N);
        assert(0 <= j && j < N);
        return cells[i * N + j];
    }

    static Position initial() {
        Position p;
        int base = (N / 2 - 1) * (N + 1);
        p.cells[base] = WHITE;
        p.cells[base + 1] = BLACK;
        p.cells[base + N] = BLACK;
        p.cells[base + N + 1] = WHITE;
        return p;
    }

    bool black_to_move() const {
        return move_number % 2 == 0;
    }

    std::string __str__() const {
        std::ostringstream out;
        out << "Position(" << move_number;
        if (prev_skipped)
            out << ", prev skipped";
        if (black_to_move())
            out << ", black to move" << std::endl;
        else
            out << ", white to move" << std::endl;
        for (int i = 0; i < N; i++) {
            out << "    ";
            for (int j = 0; j < N; j++)
                out << ".BW"[cells[i * N + j]] << " ";
            out << std::endl;
        }
        out << ")";
        return out.str();
    }

    bool try_flip_line(int pos, int dir) {
        Cell my_color = black_to_move() ? BLACK : WHITE;
        Cell opponent_color = black_to_move() ? WHITE : BLACK;
        int p = pos + dir;
        int i = 0;
        while (p >= 0 && p < N * N && abs(p % N - (p - dir) % N) <= 1) {
            if (cells[p] == EMPTY) break;
            if (cells[p] == my_color) {
                if (i > 0) {
                    while (i > 0) {
                        p -= dir;
                        assert(cells[p] == opponent_color);
                        cells[p] = my_color;
                        i--;
                    }
                    return true;
                } else
                    return false;
            }
            i++;
            p += dir;
        }
        return false;
    }

    bool try_move_inplace(int pos) {
        if (pos == -1) {
            assert(!prev_skipped);
            prev_skipped = true;
            move_number++;
            return true;
        }

        if (cells[pos] != EMPTY)
            return false;

        static const int dirs[] = {
            1, -1, N, -N, N + 1, N - 1, - N - 1, - N + 1};
        bool flipped = false;
        for (int dir : dirs) {
            if (try_flip_line(pos, dir))
                flipped = true;
        }
        if (flipped) {
            cells[pos] = black_to_move() ? BLACK : WHITE;
            move_number++;
            prev_skipped = false;
        }
        return flipped;
    }

    std::vector<std::pair<Move, Position> > generate_successors() const {
        std::vector<std::pair<Move, Position> > result;
        Position p = *this;
        for (int i = 0; i < N * N; i++) {
            if (p.try_move_inplace(i)) {
                result.push_back(std::make_pair(i, p));
                p = *this;
            }
        }
        if (result.empty() && !prev_skipped) {
            result.push_back(std::make_pair(-1, *this));
            result.back().second.try_move_inplace(-1);
        }
        return result;
    }

    int num_moves() const {
        // Intended for mobility calculations, does not include skip move.
        int result = 0;
        Position p = *this;
        for (int i = 0; i < N * N; i++)
            if (p.try_move_inplace(i)) {
                p = *this;
                result++;
            }
        return result;
    }

    // Difference between the number of moves by the current player and
    // the number of moves by the opponent (assuming it was her turn).
    // Skip moves are not taken into consideration because they indeed don't
    // contribute to mobility.
    int mobility() const {
        Position flipped = *this;
        flipped.move_number++;
        assert(black_to_move() != flipped.black_to_move());
        return num_moves() - flipped.num_moves();
    }

    int cnt_black_minus_cnt_white() const {
        int result = 0;
        for (Cell c : cells) {
            if (c == BLACK)
                result++;
            else if (c == WHITE)
                result--;
        }
        return result;
    }

    int final_score() const {
        int num_black = 0;
        int num_white = 0;
        for (Cell c : cells) {
            if (c == BLACK)
                num_black++;
            else if (c == WHITE)
                num_white++;
        }

        int score;
        if (num_black > num_white)
            score = N * N - 2 * num_white;  // empty cells count toward black
        else
            score = 2 * num_black - N * N;  // empty cells count toward white

        return black_to_move() ? score : -score;
    }

    template<typename EmitFn>
    void emit_features(EmitFn emit) const {
        Cell my_color = move_number % 2 == 0 ? BLACK : WHITE;
        Cell opponent_color = move_number % 2 == 0 ? WHITE : BLACK;
        assert(N % 2 == 0);
        for (int i = 0; i < N/2; i++)
            for (int j = 0; j <= i; j++) {
                int mirrored[] = {
                    i * N + j,
                    (N - 1 - i) * N + j,
                    i * N + (N - 1 - j),
                    (N - 1 - i) * N + (N - 1 - j),
                    j * N + i,
                    (N - 1 - j) * N + i,
                    j * N + (N - 1 - i),
                    (N - 1 - j) * N + (N - 1 - i),
                };
                // We count cells on diagonals twice, but that can be
                // addressed by assigning them half the weight.
                int d = 0;
                for (int idx : mirrored) {
                    if (cells[idx] == my_color)
                        d++;
                    else if (cells[idx] == opponent_color)
                        d--;
                }
                emit(d);
            }
        emit(mobility());
    }

    static int num_features() {
        int cnt = 0;
        initial().emit_features([&cnt](float f){ cnt ++; });
        return cnt;
    }

    void features_array(int n, float *out_arr) const {
        int cnt = 0;
        emit_features([&cnt, &out_arr](float f){ *out_arr++ = f; cnt ++; });
        assert(cnt == n);
    }

    float weight_features(int n, float *in_arr /* weights */) const {
        float result = 0.0f;
        int cnt = 0;
        emit_features([&](float f){
            result += *in_arr++ * f;
            cnt++;
        });
        assert(cnt == n);
        return result;
    }
};
