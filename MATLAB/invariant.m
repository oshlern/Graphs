function inv_dist = invariant(B,steps,v0)
%This function simulates the powers of the adjacency matrix B.  Typical
%application:
%
%inv_dist = invariant(A,200,[1 zeros(1,49)]);
%

N = numel(v0);
v = v0;
figure(2);
clf;
bar(v/sum(v));
axis([0,N+1,0,1]);
for i = 1:steps,
    pause(0.1);
    v = v*B;
    bar(v/sum(v));
    axis([0,N+1,0,1]);
end
inv_dist = v/sum(v);

