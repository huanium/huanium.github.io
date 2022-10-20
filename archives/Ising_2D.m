opengl software

%% Initial Configuration
n_grid = 400; % Size of grid
Ms = [];
Ts = [];
Ns = [];
Es = [];


%% Monte Carlo loop, slowly decrease in T
num_sims = 1000;
for n = 1:1:num_sims
% Perform a simulation
T = rand()*3+1e-10;
[M, N, E] = ising(n_grid, T, n);
% Record the results
Ms = [Ms M/(n_grid^2)];
Es = [Es E/(n_grid^2)];
Ns = [Ns N];
Ts = [Ts T];
end

%% Figure Generation
% Energy per site, versus temperature
figure(1)
plot(Ts, Es, 'ro');
ylabel('energy per site');
xlabel('temperature');
pbaspect([2 1 1]);
title('Energy per site, versus temperature');
% Magnetization per site, versus temperature
figure(2)
plot(Ts, Ms, 'bo');
ylabel('magnetization per site');
xlabel('temperature');
ylim([-1.1 1.1]);
pbaspect([2 1 1]);
title('Magnetization per site, versus temperature')
% Magnetization per site, versus Energy per site
figure(3)
plot(Es, Ms, 'o', 'Color', [0 0.5 0]);
xlabel('Energy per site');
ylabel('Magnetization per site');
pbaspect([2 1 1]);
title('Magnetization per site, versus Energy per site');




%% Ising funtion
function [M, num, E] = ising(N,T, num_sim)
J = 1; % Strength of interaction (Joules)
k = 1; % Joules per kelvin
Ms = [];
Es = [];
%% Generate a random initial configuration
grid = (rand(N) > 0.5)*2 - 1;
%% Evolve the system for a fixed number of steps
for i=1:1500
    % Calculate the number of neighbors of each cell
    neighbors = circshift(grid, [ 0 1]) + ...
    circshift(grid, [ 0 -1]) + ...
    circshift(grid, [ 1 0]) + ...
    circshift(grid, [-1 0]);
    % Calculate the change in energy of flipping a spin
    DeltaE = 2 * J * (grid .* neighbors);
    % Calculate the transition probabilities
    p_trans = exp(-DeltaE/(k * T));
    % Decide which transitions will occur
    transitions = (rand(N) < p_trans ).*(rand(N) < 0.1) * -2 + 1;
    % Perform the transitions
    grid = grid .* transitions;
    % Sum up our variables of interest
    M = sum(sum(grid));
    E = -sum(sum(DeltaE))/2;
    % Display the current state of the system (optional)
    image((grid+1)*128);
    xlabel(sprintf('Sim No. = %0.0f, i = %0.0f, T = %0.2f, M = %0.2f, E = %0.2f', num_sim, i, T, M/N^2, E/N^2));
    set(gca,'YTickLabel',[],'XTickLabel',[]);
    axis square; colormap bone; drawnow;
end
% Count the number of clusters of ’spin up’ states
[L, num] = bwlabel(grid == 1, 4);
end
