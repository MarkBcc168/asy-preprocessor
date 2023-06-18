size(11cm,0);
import olympiad;

pair A = dir(140);
pair B = dir(210);
pair C = dir(330);
pair D = dir(240);
pair E_prime = extension(B, C, A, B*C/D);
pair I = incenter(A, B, C);
pair M = dir(270);
pair I_a = 2*M-I;
pair K = extension(A, I, B, C);
pair P = extension(D, K, M, E_prime);
pair X = 2*M-E_prime;

draw(unitcircle, blue);
draw(A--B--C--cycle, blue);
draw(circumcircle(D, I, I_a), blue);
draw(A--I_a, blue);
draw(D--P--X, orange);
draw(X--I--E_prime--I_a--cycle, red);
draw(circumcircle(B, I, C), grey);
draw(D--A--E_prime, deepcyan+dashed);

dot("$A$", A, ?????);
dot("$B$", B, ?????);
dot("$C$", C, ?????);
dot("$D$", D, ?????);
dot("$E'$", E_prime, ?????);
dot("$I$", I, ?????);
dot("$M$", M, ?????);
dot("$I_a$", I_a, ?????);
dot("$K$", K, ?????);
dot("$P$", P, ?????);
dot("$X$", X, ?????);

