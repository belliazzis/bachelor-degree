#caricamento di phi e u da variabile MATLAB salvata
phi = loadmat('sim_fin.mat')['phi'].astype('complex')
u = loadmat('sim_fin.mat')['u'].astype('complex')
phi_torch=torch.from_numpy(phi).to(device)
#inizializzazione di gamma come vettore di zeri
gamma_start_re=torch.zeros(87,1).type(torch.float32)
gamma_start_im=torch.zeros(87,1).type(torch.float32)
gamma_start=torch.complex(gamma_start_re,gamma_start_im)

#alternativamente caricaemnto di gamma da variabile MATLAB
salvata (in questo caso ricostruita con SVD)
gamma_start=loadmat('sim_fin.mat')['gamma_SVD'].astype('comp
lex')
dataset =[(gamma_start, u)] #definizione del dataset
#definizione della rete neurale
class ComplexNet(nn.Module):
 def __init__(self):
 super(ComplexNet, self).__init__()
 self.fc1 = ComplexLinear(87,200)
 self.fc2 = ComplexLinear(200, 28)
 def forward(self, x):
 x = complex_relu(self.fc1(x))
 x = self.fc2(x)
 bb=torch.reshape(x,[87,1])
 aa=phi_torch
 rl=torch.real(aa)
 rl=rl.type(torch.float32)
 im=torch.imag(aa)
 im=im.type(torch.float32)
 aa2=torch.complex(rl,im)
 rl=torch.real(bb)
 rl=rl.type(torch.float32)
 im=torch.imag(bb)
 im=im.type(torch.float32)
 bb2=torch.complex(rl,im)
 x2=torch.matmul(aa2,bb2)
 return x2,x

#definizione della funzione di perdita dell’errore quadratico
medio
class ComplexMSELoss(nn.Module):
 def __init__self(self):
 super(ComplexMSELoss,self).__initmatlab__()
 self.mse_loss= nn.MSELoss()
 def forward(self,input:torch.Tensor,
target:torch.Tensor) -> torch.Tensor:
 rl=torch.real(input)
 im=torch.imag(input)
 rl_tar=torch.real(target)
 im_tar=torch.imag(target)
 ll=nn.MSELoss()
 rl_loss=ll(rl.to(device),rl_tar.to(device))
 im_loss=ll(im.to(device),im_tar.to(device))
 return rl_loss+im_loss
epochs = 10000 #numero di epoche
l_r = 5e-3 #learning rate
loss_f = ComplexMSELoss()
loss_=nn.MSELoss()
optmz = optim.Adam(net.parameters(), lr=l_r)
lam=0.7
#ciclo di training
for i in range(epochs):
for traindata in trainset:
 matrix, targ = traindata
 net.zero_grad()
 start=datetime.now()
 matrix = torch.reshape(matrix,[1,1,87])
 rl=torch.real(matrix)
 rl=rl.type(torch.float32)
 im=torch.imag(matrix)
 im=im.type(torch.float32)
 matrix2=torch.complex(rl,im)
 net.zero_grad()
 [targ_exit, layerr] = net(matrix2.to(device))
#calcolo della Perdita in parte reale e immaginaria
loss_re=loss_(torch.real(targ_exit).to(device),torch.real(to
rch.reshape(targ,[28,1])).to(device).type(torch.float32))
loss_im=loss_(torch.imag(targ_exit).to(device),torch.imag(to
rch.reshape(targ,[28,1])).to(device).type(torch.float32))
# Funzione di costo complessiva con regolarizzazione L2
loss_train=(1-lam)*(loss_re+loss_im)+
lam*torch.norm(layerr,2)
#definizione, rappresentazione e salvataggio della variabile
contenente la ricostruzione
reconstruction = np.squeeze(layerr.cpu().detach().numpy())
plt.plot(np.abs(reconstruction)/max(np.abs(reconstruction)))
dic_reconstruction = {}
file_name_reconstruction = 'SVD5'
dic_reconstruction['reconstruction']=reconstruction
savemat(f'{file_name_reconstruction}.mat',
dic_reconstruction)
