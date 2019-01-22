function [A,L,lam,V] = gen_graph(N,p)
%This function generates a random (E-R) graph with N vertices and 
%connection probability p.  Typical application:
%
%[A,L,lam,V] = gen_graph(15,.1);sum(abs(lam)<1e-10)
%

x = exp(2*pi*1i*[0:N-1]'/N);
Ah = binornd(1,p,N,N); %Too big but it doesn't matter
figure(1);
clf;
plot(real(x),imag(x),'bo');
hold on;
for j = 1:N-1,
    for k = j+1:N,
        if Ah(j,k)==1,
            A(j,k) = Ah(j,k);
            A(k,j) = Ah(j,k);
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