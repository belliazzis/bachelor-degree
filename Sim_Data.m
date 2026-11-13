%Parametri radar e inizializzazione
lambda=0.031066576;
f0=9.6500000e+09; %carrier frequency
cv=3e8;
f=cv/lambda;
R0=617472 ;
Bw=1.2000000e+08; %range bandwidth
dx= 4.7840000 ; %azimuth antenna dimension
teta=0.6134;
v=7071.7701; %platform velocity
prf= 3744.7563; %pulse repetition frequency
fs=1.6482918e+08; %sampling frequency (range)
delta_r=cv/2/fs;
Appendice A
46
delta_y=delta_r/sin(teta);
delta_x=v/prf;
% phi è la matrice da invertire
for m=1:p
 for k=1:n
 phi(m,k)=exp(-1i*4*pi/lambda*(1/R0*s1(m)*s(k)));
 end
end
%generazione del vettore gamma
smin=min(s);
smax=max(s);
for nt=1:Ntrain
 gamma=zeros(n,1)+1i*zeros(n,1);
 s_gamma(nt)=smin+(smax-smin)*rand();
 ks=floor((s_gamma(nt)-smin)/delta_s)+1;
 fase_gamma=rand()*2*pi-0.999*pi;
 gamma(ks)=exp(1i*fase_gamma);
 gamma(ks+5)=1*exp(1i*fase_gamma);

 % u è il vettore dei dati
 u= phi*gamma + (randn(m,1)+1i*randn(m,1))*sigman;

%algoritmo iterative per la ricostruzione di gamma tramite CS
 niter=100;
 tau=norm(phi)^2/40;
 Th=sqrt(mean(abs(u).^2))/140;
 g1k=zeros(N,1);
Appendice A
47
 for k=1:niter
 gk=g1k;
 r = u - phi*gk ;
 gk =gk+1/tau*pinv(phi,1e-1)*r;
 g1k = (abs(gk)>Th).*gk;
 err(k) = norm(r, 'fro');
 end
 gamma_CS=g1k;
%ricostruzione di gamma tramite SVD
 gamma_SVD=complex(pinv(phi,1e-1)*u);
%ricostruzione di gamma tramite BF
 gamma_BF=phi'*u;