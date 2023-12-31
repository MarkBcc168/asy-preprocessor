import geometry;
import graph;
import olympiad;
defaultpen(fontsize(10pt));
size(14cm);
pair TT,A,B,C,D,E,I,N2,N1,M,T1,T2,S,P,Q,M2,M1;

E = dir(130);
D = dir(222);
C = dir(-43);
N2 = dir(90);
M2 = -N2;
I = incenter(C,D,E);
real r = inradius(C,D,E);
TT = I + dir(140)*(r,0);
pair TTT = (I - TT) * dir(90) + TT;
A = extension(TTT,TT,E,D);
B = extension(TTT,TT,E,C);
N1 = intersectionpoints(line(E,N2),circumcircle(A,B,E))[1];
M1 = 2 * circumcenter(A,B,E) - N1;
M = intersectionpoints(circumcircle(A,B,E),unitcircle)[1];
T1 = intersectionpoints(I--N1,circumcircle(A,B,M))[0];
T2 = intersectionpoints(line(I,N2),circumcircle(N2,D,E))[2];
S = circumcenter(I,M,E);
P = 2*S - I;
Q = extension(I,M,N1,N2);

draw(A--B);

draw(incircle(C,D,E),dashed);
draw(unitcircle, blue);
draw(circumcircle(A,B,E), red);
draw(C--D--E--cycle);
draw(N2--Q, linewidth(1));
draw(P--I--Q, gray);
draw(circumcircle(M,I,T1),deepgreen+linewidth(1));
draw(circumcircle(E,M,I),black+linewidth(0.8));
draw(N2--T2, blue+linewidth(1));
draw(E--M2);
draw(T1--M1, red);
draw(T2--M2, blue);
draw(I--N1, red + linewidth(1));


dot("$E$",E,?????);
dot("$D$",D,?????);
dot("$C$",C,?????);
dot("$I$",I,?????,deepgreen);
dot("$A$",A,?????);
dot("$B$",B,?????);
dot("$N_1$",N1,?????, red);
dot("$N_2$",N2,?????, blue);
dot("$M$",M,?????,deepgreen);
dot("$T_1$",T1,?????, red);
dot("$T_2$",T2,?????, blue);
dot("$Q$",Q,?????);
dot("$P$",P,?????);
dot("$S$",S,?????);
dot("$M_2$",M2,?????, blue);
dot("$M_1$",M1,?????, red);