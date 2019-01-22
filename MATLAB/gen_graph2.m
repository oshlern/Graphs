function [L,lam,V] = gen_graph2(A)
%This function generates a graph with adjacency matrix A.  Typical 
%application:
%
%B = [0 1 0 0 0;1 0 0 1 0;0 0 0 1 0;0 0 0 0 1;0 0 1 0 0];[L,lam,V] = gen_graph2(B);
%

[N,dum] = size(A);
x = exp(2*pi*i*[0:N-1]'/N);
figure(1);
clf;
plot(real(x),imag(x),'bo');
hold on;
for j = 1:N,
    for k = 1:N,
        if A(j,k)==1,
            plot(real([x(j);x(k)]),imag([x(j);x(k)]),'r-');
        else end
    end
end

hold off;
axis([-2,2,-2,2]);

d = sum(A')';
L = diag(d)-A;
[V,lam] = eig(L);
lam = diag(lam);