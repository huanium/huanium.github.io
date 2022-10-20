%Program 1: Numerical Integration and Plotting using MATLAB 
N = 1000; % No. of points.
L = pi/2; % Range of x: from -L to L.
x = linspace(-L, L, N).'; % Generate column vector with N 
 % x values ranging from -L to L.
dx = x(2) - x(1); % Coordinate step.
% Two-point finite-difference representation of Derivative.
D = (diag(ones((N-1),1),1) - diag(ones((N-1),1),-1)) / (2*dx);
% Next modify D so that it is consistent with f(0) = f(L) = 0.
D(1, 1) = 0; D( 1, 2) = 0; D(2, 1) = 0; 
D(N, N-1) = 0; D(N-1, N) = 0; D(N, N) = 0;


% %Laplacian can be obtained directly by D*D, but better recipe is to
% %consider a three-point finite-difference representation of Laplacian
% Lap = (diag(ones((N-1),1),-1) - 2*diag(ones(N,1),0) ...
%  + diag(ones((N-1),1), 1)) / (dx^2);
% % Next modify Lap so that it is consistent with f(0) = f(L) = 0.
% Lap(1, 1) = 0; Lap( 1, 2) = 0; Lap(2, 1) = 0;
% Lap(N, N-1) = 0; Lap(N-1, N) = 0; Lap(N, N) = 0; 

% Three-point finite-difference representation of Laplacian
% using sparse matrices, where you save memory by only
% storing non-zero matrix elements.
e = ones(N,1); % a column of ones
Lap = spdiags([e -2*e e],[-1 0 1],N,N) / dx^2;
% put -2e on the main diagonal and e-s on upper and lower diagonals


 

% % infinite square well
% % Total Hamiltonian where hbar=1 and m=1.
% hbar = 1; 
% m = 1; 
% H = -(1/2)*(hbar^2/m)*Lap; 
% % Solve for eigenvector matrix V and eigenvalue matrix E of H.
% [V, E] = eig(H);
% % Plot lowest 3 eigenfunctions.
% plot(x,V(:,3), x,V(:,4), x,V(:,5)); %V(:,1) and V(:,2) are boundary zero-energy
% %nonphysical states, they do not vanish at boundaries and exist due
% %to our convention for Laplacian at edges. 
% legend('\psi_{E_1}(x)','\psi_{E_2}(x)','\psi_{E_3}(x)','Location','EastOutside');
% xlabel('x (m)');
% ylabel('unnormalized wavefunction (1/m)');
% ax = gca; % Get the Current Axes object
% ax.XLim = [0 2*pi];


% quantum harmonic oscillator
U = 1/2*100*x.^(2); % quadratic harmonic oscillator potential
%k = 2*pi/1064e-9;

% Total Hamiltonian.
hbar = 1;
m = 1;
H = -1/2*(hbar^2/m)*Lap + spdiags(U,0,N,N); % 0 indicates main diagonal 
% put vector U on the main diagonal of NxN sparse matrix


% Find lowest nmodes eigenvectors and eigenvalues of sparse matrix.
nmodes = 3; 
[V,E] = eigs(H,nmodes,'smallestreal'); % find eigs.
[E,ind] = sort(diag(E)); % convert E to vector and sort low to high.
V = V(:,ind); % rearrange corresponding eigenvectors.

% Generate plot of lowest energy eigenvectors V(x) and U(x).
Usc = 10 * U * max(abs(V(:))) / max(abs(U));% rescale U for plotting.
plot(x,V, x,Usc,'--k'); % plot V(x) and rescaled U(x).
xlabel('x (m)');
ylabel('unnormalized wavefunction');

% Add legend showing Energy of plotted V(x).
legendLabels = [repmat('E = ',nmodes,1), num2str(E)];
legend(legendLabels) % place lengend string on plot.
%ax = gca;
%ax.XLim = sqrt(2)*[-1 1];



% 
% %----------------------------------------------------------------
% % Program 5: Calculate Probability Density as a function of time 
% % for a particle trapped in a double-well potential.
% %----------------------------------------------------------------
% % Potential due to two square wells of width 2w 
% % and a distance 2a apart.
% w = L/50; 
% a = 3*w; 
% U = -100*( heaviside(x+w-a) - heaviside(x-w-a) ...
%  + heaviside(x+w+a) - heaviside(x-w+a));
% 
% H = -(1/2)*Lap + spdiags(U,0,N,N);
% 
% 
% % Find and sort lowest nmodes eigenvectors and eigenvalues of H.
% nmodes = 2; 
% [V,E] = eigs(H,nmodes,'smallestreal'); 
% [E,ind] = sort(diag(E)); % Convert E to vector and sort low to high. 
% V = V(:,ind); % Rearrange coresponding eigenvectors, usually they are not normalized
% 
% % Rescale eigenvectors so that they are always 
% % positive at the center of the right well. 
% % Still they may not be normalized to unity.
% for c = 1:nmodes 
%  V(:,c) = V(:,c) / sign(V((3*N/4),c)); 
% end
% 
% 

% %---------------------------------------------------------------- 
% % Compute and display normalized prob. density rho(x,t). 
% %---------------------------------------------------------------- 
% % Parameters for solving the problem in the interval 0 < t < TF. 
% TF = 4*pi*hbar/(E(2)-E(1)); % Length of time interval.
% NT = 100; % No. of time points.
% t = linspace(0,TF,NT); % Time vector.
% % Compute probability normalization constant (at T=0).
% psi_o = 0.5*V(:,1) + 0.5*V(:,2); % Wavefunction at T=0.
% sq_norm = psi_o' * psi_o * dx; % Square norm = |<ff|ff>|^2.
% Usc = 4*U*max(abs(V(:))) / max(abs(U)); % Rescale U for plotting.
% 
% 
% % Compute and display rho(x,t) for each time t.
% % Plot lowest 2 eigenfunctions.
% plot(x,V(:,1), x,V(:,2),'--g',x,U/500);
% legend('\psi_{E_0}(x)','\psi_{E_1}(x)','Double well potential (rescaled)','Location','EastOutside');
% xlabel('x (m)');
% ylabel('unnormalized wavefunction (1/m)');
% ax = gca; % Get the Current Axes object
% ax.XLim = [-1 1];
% 
% 
% vw1 = VideoWriter('C:\Users\buiqu\Documents\GitHub\huanium\archives\doubleWell.avi'); % Prepare the new file.
% % vw1.FrameRate=30 by default
% open(vw1);
% for jj = 1:NT % time index parameter for stepping through loop.
%  % Compute wavefunction psi(x,t) and rho(x,t) at t=t(jj).
%  psi = 0.5*V(:,1)*exp(-1i*E(1)*t(jj)) ...
%  + 0.5*V(:,2)*exp(-1i*E(2)*t(jj));
%  rho = conj(psi) .* psi / sq_norm; % Normalized probability density.
%  
%  % Plot rho(x,jj) and rescaled potential energy Usc.
%  plot(x,rho,'o-', x, Usc,'.-');
%  axis([-L/8 L/8 -1 6]);
%  xlabel('x (m)');
%  ylabel('probability density (1/m)');
%  title(['t = ' num2str(t(jj), '%05.2f') ' s']);
%  
%  writeVideo(vw1, getframe(gcf)); 
%  % getframe returns a movie frame, a snapshot (pixmap) of the current axes or figure.
% end
% 
% close(vw1);
% %implay('doubleWell.avi')



% %---------------------------------------------------------------- 
% % Program 6: Wavepacket propagation using exponential of H.
% %---------------------------------------------------------------- 
% % Parameters for solving the problem in the interval 0 < x < L.
% L = 100; % Interval Length.
% N = 500; % No of points.
% x = linspace(0,L,N).'; % Coordinate vector.
% dx = x(2) - x(1); % Coordinate step.
% % Parameters for making intial momentum space wavefunction phi(k).
% ko = 2; % Peak momentum.
% a = 20; % Momentum width parameter.
% dk = 2*pi/L; % Momentum step.
% km = N*dk; % Momentum limit.
% k = linspace(0,+km,N).'; % Momentum vector.
% 
% 
% % Make psi(x,0) from Gaussian kspace wavefunction phi(k) using
% % fast fourier transform.
% phi = exp(-a*(k-ko).^2).* exp(-1i*6*k.^2); % Unnormalized phi(k).
% psi = ifft(phi); % Multiplies phi by exp(ikx) and integrates vs x.
% psi = psi / sqrt(psi' * psi * dx); % Normalize psi(x,0).
% % Expectation value of energy; e.g. for the parameters
% % chosen above <E> = 2.062.
% avgE = phi' * 0.5*diag(k.^2,0) * phi * dk / (phi' * phi * dk);
% % CHOOSE POTENTIAL U(X): Either U = 0 OR
% % U = step potential of height avgE that is located at x = L/2.
% %U = 0*heaviside(x-(L/2)); % Free particle wave packet evolution.
% U = 1.1*avgE*heaviside(x-(L/2)); % Scattering off step potential.
% % Hamiltonian.
% Lap = spdiags([e -2*e e],[-1 0 1],N,N) / dx^2;
% H = -(1/2)*Lap + spdiags(U,0,N,N);
% % Parameters for computing psi(x,t) at different times 0 < t < TF.
% NT = 200; % No. of time steps.
% TF = 28;
% t = linspace(0,TF,NT); % time vector
% dt = t(2) - t(1); % time step
% hbar = 1;
% % time displacement operator.
% Evolution_Operator = expm(-1i * H * dt / hbar);
% %----------------------------------------------------------------
% % Simulate rho(x,t) and plot for each t
% %----------------------------------------------------------------
% vw2 = VideoWriter('C:\Users\buiqu\Documents\GitHub\huanium\archives\propagation.avi');
% vw2.FrameRate=35;
% open(vw2);
% for jj = 1:NT % Time index for loop.
%     % Calculate probability density rho(x,t).
%     psi = Evolution_Operator * psi; % Calculate psi(t+\Delta t) from psi(t)
%     rho = conj(psi) .* psi; % rho(x,t).
%     
%     plot(x,rho,x,U/50,'.-'); %potential is rescaled to fit nicely in the plot
%     axis([0 L 0 0.25]);
%     xlabel('x (m)');
%     ylabel('probability density (1/m)');
%     title(['t = ' num2str(t(jj), '%05.2f') ' s']);
%     
%     writeVideo(vw2, getframe(gcf));
% end
% 
% close(vw2);
% % Calculate Reflection probability
% R = 0;
% for a = 1:floor(N/2) 
%  R = R + rho(a); % density at the eft of step barrier
% end
% R = R * dx



