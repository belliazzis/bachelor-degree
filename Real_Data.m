% parametri SAR
lambda = 0.031066576;
cv = 3e8;
R0 = 617472;
oversamp_factor = 1; % valore aggiornato
Sground = 130; % valore aggiornato
z0=23; % costante da sommare all'altezza per trovarsi con i
valori LiDAR
s = [0:(n-1)] * delta_s - 60; % valore aggiornato
phi = zeros(Nbase, N);
for m = 1:Nbase
 for k = 1:N
Appendice B
52
 phi(m,k) = exp(1i * 4 * pi / lambda * (1 / R0 * s1(m)
* s(k))); %esponenziale positivo per evitare l’inversione
del DEM
 end
end
pinv_phi = pinv(phi, 0,01); % valore aggiornato della
regolarizzazione della pseudo-inversa
[nrow, ncol, ~] = size(immagini);
% preallocazione dei volumi gamma e delle mappe d’altezza
gamma_all_SVD = zeros(nrow, ncol, N);
gamma_all_BF = zeros(nrow, ncol, N);
gamma_all_CS = zeros(nrow, ncol, N);
height_map_SVD = zeros(nrow, ncol);
height_map_BF = zeros(nrow, ncol);
height_map_CS = zeros(nrow, ncol);
% loop principale su tutti i pixel
for i = 1:nrow
 for j = 1:ncol
 u = squeeze(immagini(i,j,:));
 % verifica dati validi
 if all(abs(u) < 1e-10) || any(isnan(u))
 continue
 end
 % ricostruzione SVD
 gamma_SVD = pinv_phi * u;
 gamma_all_SVD(i,j,:) = gamma_SVD;
 % ricostruzione Beamforming
 gamma_BF = phi' * u;
 gamma_all_BF(i,j,:) = gamma_BF;
 % ricostruzione Compressive Sensing
 niter = 100;
 %valori aggiornati di tau e della soglia, rendendo la
soglia adattiva
 tau = norm(u)/norm(pinv_phi*u);
 Th=norm(pinv_phi*u)/sqrt(length(u))/sqrt(length(s));
 g1k = zeros(N,1);
 for k = 1:niter
 gk = g1k;
 r = u - phi * gk;
 gk = gk + 1 / tau * pinv_phi * r;
 g1k = (abs(gk) > Th) .* gk;
 end
 gamma_all_CS(i,j,:) = g1k;
 % estrazione quota dominante
 [~, idx_max_SVD] = max(abs(gamma_SVD));
 [~, idx_max_BF] = max(abs(gamma_BF));
 [~, idx_max_CS] = max(abs(g1k));
 % trasformazione necessaria per passare da s a z
height_map_SVD(i,j) = s(idx_max_SVD)*sin(teta)+z0;
 height_map_BF(i,j) = s(idx_max_BF)*sin(teta)+z0;
 height_map_CS(i,j) = s(idx_max_CS)*sin(teta)+z0;
 end
end
% visualizzazione delle mappe di altezza
figure, imagesc(height_map_SVD); colorbar; title('Mappa
Altezza - SVD');colormap('jet');
figure, imagesc(height_map_BF); colorbar; title('Mappa
Altezza - BF');colormap('jet');
figure, imagesc(height_map_CS); colorbar; title('Mappa
Altezza - CS');colormap('jet');
%applicazione filtro mediano (3x3)
height_map_SVD_filt=medfilt2(height_map_SVD,[3,3]);
height_map_BF_filt=medfilt2(height_map_BF,[3,3]);
height_map_CS_filt=medfilt2(height_map_CS,[3,3]);
%visualizzazione delle mappe di altezza filtrate
figure, imagesc(height_map_SVD_filt); colorbar; title('Mappa
Altezza filtrata - SVD');colormap('jet');
figure, imagesc(height_map_BF_filt); colorbar; title('Mappa
Altezza filtrata - BF');colormap('jet');
figure, imagesc(height_map_CS_filt); colorbar; title('Mappa
Altezza filtrata - CS');colormap('jet'); 
