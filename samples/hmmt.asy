size(8cm,0);
import olympiad;
import geometry;

real theta = 65;
pair B = (0,0);
pair C = (4,0);
pair A = B + 2*dir(theta);
pair D = C + 3.35*dir(180-theta);
pair P = reflect((B+C)/2, extension(A,B,C,D)) * A;
pair X = circumcenter(P,A,D);
pair K = extension(X, (A+D)/2, B,C);
pair P = extension(A, A+C-B, D,C);

draw(A--B--C--D--cycle, linewidth(1.2));
draw(A--P, red);
pen thickred = red+linewidth(0.8);
draw(circumcircle(A,D,P), red);
draw(A--X, thickred, StickIntervalMarker(1,1,size=0.25cm,thickred));
draw(D--X, thickred, StickIntervalMarker(1,1,size=0.25cm,thickred));
draw(P--X, thickred, StickIntervalMarker(1,1,size=0.25cm,thickred));
draw(B--X, gray, StickIntervalMarker(1,2,size=0.4cm,gray));
draw(X--C, gray, StickIntervalMarker(1,2,size=0.4cm,gray));
dot("$A$",A,?????);
dot("$B$",B,?????);
dot("$C$",C,?????);
dot("$D$",D,?????);
dot("$X$",X,?????);
dot("$P$",P,?????);