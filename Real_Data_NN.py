# caricamento dati dal file MATLAB
data = loadmat('ricostruzionedatoreale.mat')
immagini = data['immagini'].astype(np.complex64)
phi = data['phi'].astype(np.complex64)
s = data['s'].squeeze()
teta = float(data['teta'].squeeze())
z0 = float(data['z0'].squeeze())
#utilizzato per inizializzare gamma alla ricostruzione
ottenuta dal CS
gamma_all = data['gamma_all_CS'].astype(np.complex64)
H, W, M = immagini.shape
_, N = phi.shape
# nei parametri di training le epoche sono state ridotte
epochs = 300
lr = 5e-3
lam = 0.7
loss_fn = nn.MSELoss()
# inizializzazione volume gamma
reconstruction_map = np.zeros((H, W, N),
dtype=np.complex64)
# loop su tutti i pixel
for i in range(H):
 for j in range(W):
 u = immagini[i, j, :]
 # controllo se il pixel è valido
 if np.all(np.abs(u) < 1e-10) or
np.any(np.isnan(u)):
 continue
 u_tensor = torch.from_numpy(u).reshape(M,
1).to(device)

 #inizializza gamma a gamma_all_CS
 gamma = gamma_all[i, j, :]
 gamma_tensor = torch.from_numpy(gamma).reshape(1,
1, N).to(device)
 # oppure inizializza gamma = 0
 # gamma_tensor = torch.zeros(1, 1, N,
dtype=torch.cfloat).to(device)
 # inizializza rete
 net = ComplexNet(input_size=N).to(device)
 optimizer = optim.Adam(net.parameters(), lr=lr)
 # training
 for epoch in range(epochs):
 net.zero_grad()
 output, latent = net(gamma_tensor)
 loss_re = loss_fn(torch.real(output),
torch.real(u_tensor).float())
 loss_im = loss_fn(torch.imag(output),
torch.imag(u_tensor).float())
 loss = (1 - lam) * (loss_re + loss_im) + lam *
torch.norm(latent, 2)
 loss.backward()
 optimizer.step()
# ricostruzione mappa altezza e mappa altezza filtrata
indice_massimo = np.argmax(np.abs(reconstruction_map),
axis=2)
altezza_mappa = s[indice_massimo] * np.sin(teta) + z0
altezza_filtrata = medfilt2d(altezza_mappa, kernel_size=3)
# visualizzazione
plt.figure()
plt.imshow(altezza_mappa, cmap='jet')
plt.colorbar(label='Altezza [m]')
plt.title('Mappa delle Altezze stimata ')
plt.show()
