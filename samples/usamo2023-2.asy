size(11cm,0);
import olympiad;
defaultpen(fontsize(10pt));
pair I_A = dir(115);
pair I_B = dir(200);
pair I_C = dir(340);
pair A = foot(I_A, I_B, I_C);
pair B = foot(I_B, I_A, I_C);
pair C = foot(I_C, I_A, I_B);
pair I = orthocenter(I_A, I_B, I_C);
pair D = (I + dir(50))/2;
pair E = extension(reflect(A,I)*D, A, B, C);
pair E1 = reflect(A,I)*E;
pair E2 = reflect(I_B,I_C)*E;
pair O1 = circumcenter(I_A,I,D);
pair O2 = circumcenter(I_B,I_C,D);
pair K1 = 2*foot(O1,E,E1) - E1;
pair K2 = 2*foot(O2,E,E2) - E2;
pair S = extension(O1, (E1+K1)/2, O2, (E2+K2)/2);
pair T = 2*circumcenter(A,B,C) - A;
pair N = (I+I_A)/2;
pair M = (I_B+I_C)/2;

draw(E1--E--E2, linewidth(1));
draw(E2--D);
draw(O1--T--O2--S--cycle, deepgreen+linewidth(1.2));
draw(S--(E2+K2)/2, deepgreen);
draw(O1--(I+I_A)/2, deepgreen);
draw(E--C,blue+linewidth(0.4));
draw(A--I_A,blue+linewidth(0.4));

draw(circumcircle(I_A,I,D), red+linewidth(1));
draw(circumcircle(A,B,C),blue+linewidth(0.4));
draw(arc(circumcenter(I_B,I_C,D), circumradius(I_B,I_C,D),
    degrees(E2-O2)+10, 540-degrees(E2-O2)-10, CW),red+linewidth(1));


draw(I_A--I_B--I_C--cycle, gray);
draw(A--B--C--cycle, blue+linewidth(0.4));


dot("$A$",A,?????,blue);
dot("$B$",B,?????,blue);
dot("$C$",C,?????,blue);
dot("$I$",I,?????,blue);
dot("$I_A$",I_A,?????);
dot("$I_B$",I_B,?????);
dot("$I_C$",I_C,?????);
dot("$D$",D,?????,red);
dot("$E$",E,?????);
dot("$E_1$",E1,?????);
dot("$E_2$",E2,?????);
dot("$K_1$",K1,?????,gray);
dot("$K_2$",K2,?????,gray);
dot("$O_1$",O1,?????,deepgreen);
dot("$O_2$",O2,?????,deepgreen);
dot("$T$",T,?????,deepgreen);
dot("$S$",S,?????,deepgreen);
dot("$M$",M,?????,blue);
dot("$N$",N,?????,blue);