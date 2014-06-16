#pragma once

#undef NDEBUG

#include <assert.h>
#include <math.h>
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include <utility>

const int N = 6;

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

    static Position initial() {
        Position p;
        int base = (N / 2 - 1) * (N + 1);
        p.cells[base] = WHITE;
        p.cells[base + 1] = BLACK;
        p.cells[base + N] = BLACK;
        p.cells[base + N + 1] = WHITE;
        return p;
    }

    std::string __str__() const {
        std::ostringstream out;
        out << "Position(" << move_number;
        if (prev_skipped)
            out << ", prev skipped";
        if (move_number % 2 == 0)
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
        Cell my_color = move_number % 2 == 0 ? BLACK : WHITE;
        Cell opponent_color = move_number % 2 == 0 ? WHITE : BLACK;
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
            cells[pos] = move_number % 2 == 0 ? BLACK : WHITE;
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

    int leaf_score() const {
        int result = cnt_black_minus_cnt_white();
        if (move_number % 2)
            result = -result;
        if (result > 0)
            return result + 1000;
        if (result < 0)
            return result - 1000;
        return 0;
    }

    static int num_features() {
        return N * N;
    }

    void features_array(float *hz, int n) const {
        Cell my_color = move_number % 2 == 0 ? BLACK : WHITE;
        Cell opponent_color = move_number % 2 == 0 ? WHITE : BLACK;
        assert(n == N * N);
        int i = 0;
        for (Cell c : cells) {
            if (c == my_color)
                hz[i] = 1.0f;
            else if (c == opponent_color)
                hz[i] = -1.0f;
            else
                hz[i] = 0.0f;
            i++;
        }

    }
};
