include "globals.mzn";

    %Define variables
    int: n;
    array[1..n, 1..2] of int: circuits;
    array[1..n] of int: sorted_indexes;
    array[1..n] of int: x = [circuits[i, 1] | i in sorted_indexes];
    array[1..n] of int: y = [circuits[i, 2] | i in sorted_indexes];
    int: w;
    int: max_y = max(y);
    int: total_area = sum([y[i]*x[i] | i in 1..n]);
    int: approxmiate_max_y = ceil(total_area/w);
    int: min_height = max(max_y , approxmiate_max_y );
    int: max_height = sum([y[i] | i in 1..n]);
    var min_height..max_height: height;

    array [1..n] of var 0..w-min(x): pos_x;
    array [1..n] of var 0..max_height-min(y): pos_y;

    %Constraints
    
    %Implied Constraints

    %..........................Boundaries Constraint..................................
    constraint forall(i in 1..n)(pos_x[i] >= 0 /\ pos_x[i] <= w-min(x));
    constraint forall(i in 1..n)(pos_y[i] >= 0 /\ pos_y[i] <= height-min(y));
    
    constraint forall(i in 1..n)(pos_x[i] + x[i] <= w /\ pos_y[i] + y[i] <= height);
    
    %..........................constraint for preventing overlap.......................
    constraint diffn(pos_x, pos_y, x, y);

    %.............................cumulative constraint...............................
    constraint cumulative(pos_y, y, x, w);
    constraint cumulative(pos_x, x, y, max_height);

    %.............................Symmetry breaking constraints.......................
    %flip vertical & horizontal
    constraint pos_x[1] == 0 /\ pos_y[1] == 0;

    %.............................Same dimensions.....................................
    constraint forall(i in 1..n-1, j in 2..n where i<j) ( if (x[i]==x[j] /\ y[i]==y[j]) then lex_less([pos_x[i], pos_y[i]], [pos_x[j], pos_y[j]]) endif);

    solve :: seq_search([int_search([height], dom_w_deg, indomain_min), int_search(pos_x, dom_w_deg, indomain_min), int_search(pos_y, dom_w_deg, indomain_min)])
          %:: restart_linear(100)
    minimize height

 