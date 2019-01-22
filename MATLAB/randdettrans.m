function [a, at, da, dat] = randdettrans(N,p)

a = binornd(1,p,N,N)*binornd(1,p,N,N)*binornd(1,p,N,N);
% a = a*a;
at = a';
da = det(a);
dat = det(at);

% almost always 0