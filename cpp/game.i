%module game

%include "typemaps.i"
%include "std_vector.i"
%include "std_string.i"
%include "std_pair.i"

%template(IntVector) std::vector<int>;

%{
#define SWIG_FILE_WITH_INIT
#include "game.h"
%}

%include "numpy.i"
%init %{
import_array();
%}

%rename(assign) Position::operator=;

%template(MovePositionVector) std::vector<std::pair<Move, Position> >;
%template(MovePositionPair) std::pair<Move, Position>;


%apply (int DIM1, float* IN_ARRAY1) {(int n, float* in_arr)};
%apply (int DIM1, float* ARGOUT_ARRAY1) {(int n, float* out_arr)};

%include "game.h"


