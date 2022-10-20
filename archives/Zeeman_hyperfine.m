%%% AUTHOR: Huan Q. Bui %%%
%%% Colby College '21 %%%%%
%%% April 17, 2021 %%%%%%%%


% looking at 5P3/2 in K39

clear

J = 1/2;
I = 1;
L = 0; 
S = 1/2;
B = 811.138:0.001:811.140; % units is Gauss
Ahf = 152.137e6; % Ahf coef in Hz 
%Bhf = 0.870e6; % Bhf coef in Hz
Bhf=0;


% % lithium
% 
% J = 1/2;
% I = 1;
% L = 0; 
% S = 1/2;
% B = 0:1:60; % units is Gauss
% Ahf = 152.1e6; % Ahf coef in Hz 
% Bhf = 0; % Bhf coef in Hz

mJ = J:-1:-J;
mI = I:-1:-I;

size = length(mJ)*length(mI);
H = zeros(size, size);

% creat a basis for the Hamiltonian
basis = [];
for mj = mJ
    for mi = mI
        basis = [basis; [mj mi]];
   end
end

zeeman = figure(1);
for b = B % loop over field strengths
    % create the Hamiltonian, element-by-element
    % I'm not imposing the symmetric condition on H to make it easy to code
    % The formulas for the matrix elements take care of H's self-adjointness
    for r = 1:size
        mj = basis(r,1);
        mi = basis(r,2);
        for c = 1:size     
            mjj = basis(c,1);  
            mii = basis(c,2);
            
            H(r,c) = Ahf*A_hfs(J, I, mj, mi, mjj, mii) + mag(b, J, L, S, mj, mi, mjj, mii);
        end
    end
    % diagonalize and plot eigenvalues associated with field strength b
    energies = eig(H)/1e6; % fix units to MHz
    hold on 
    plot(b*ones(size), energies, 'o', 'Color', 'red', 'MarkerSize',1);
end
hold off
%dim = [0.2 0.6 0.25 0.3];
%str = {'B = 0.870 MHz, A = 1.973 MHz'};
%annotation('textbox',dim,'String',str,'FitBoxToText','on');
%title('Hyperfine Zeeman splitting for P_{3/2} of K-39 (I=3/2)')
xlabel('Magnetic Field (G)')
ylabel('Energy Shift (MHz)')



%%%%%%% FUNCTIONS %%%%%%%
% This part is self-explanatory, so I won't add further comments

function Ahfs = A_hfs(J, I, mj, mi, mjj, mii)
    Ahfs = 0;
    if mj == mjj && mi == mii
        Ahfs = mj*mi;
    elseif mj == mjj + 1 && mi == mii - 1
        Ahfs = (1/2)*sqrt((J+mj)*(J-mj+1)*(I-mi)*(I+mi+1));
    elseif mj == mjj - 1 && mi == mii + 1   
        Ahfs = (1/2)*sqrt((J-mj)*(J+mj+1)*(I+mi)*(I-mi+1));
    else
        Ahfs = 0;
    end
end


function Bhfs = B_hfs(J, I, mj, mi, mjj, mii)
    Bhfs = 0;
    if mj == mjj && mi == mii
        Bhfs = (1/2)*(3*mi^2-I*(I+1))*(3*mj^2-J*(J+1));
    elseif mj == mjj - 1 && mi == mii + 1   
        Bhfs = (3/4)*(2*mjj-1)*(2*mii+1)*sqrt((J+mjj)*(J-mjj+1)*(I-mii)*(I+mii+1));
    elseif mj == mjj + 1 && mi == mii - 1
        Bhfs = (3/4)*(2*mjj+1)*(2*mii-1)*sqrt((J-mjj)*(J+mjj+1)*(I+mii)*(I-mii+1));
    elseif mj == mjj - 2 && mi == mii + 2   
        Bhfs = (3/4)*sqrt((J+mjj)*(J+mjj-1)*(J-mjj+1)*(J-mjj+2)...
            *(I-mii)*(I-mii-1)*(I+mii+1)*(I+mii+2));
    elseif mj == mjj + 2 && mi == mii - 2
        Bhfs = (3/4)*sqrt((J-mjj)*(J-mjj-1)*(J+mjj+1)*(J+mjj+2)...
            *(I+mii)*(I+mii-1)*(I-mii+1)*(I-mii+2));
    else
        Bhfs = 0;
    end
    Bhfs = Bhfs/(2*I*(2*I-1)*J*(2*J-1));
end

function mag = mag(B, J, L, S, mj, mi, mjj, mii)
    me = 9.1093837015e-31; % electron mass
    mn = 6*1.67493e-27; % nuclear mass
    eC = 1.60218e-19; % electric charge
    hbar = 1.054571817e-34;
    muB = eC*hbar/(2*me); % Bohr magneton
    gL = 1 - me/mn; % gyro magnetic factor of the orbital
    gS = 2.0023193043622; % electron spin g-factor
    gJ = gL*(J*(J+1)-S*(S+1)+L*(L+1))/(2*J*(J+1)) + gS*(J*(J+1)+S*(S+1)-L*(L+1))/(2*J*(J+1));
    %gI = -0.00014193489; % this is an experimental value
    gI = -0.000447654; % lithium

    mag = 0;
    if mj == mjj && mi == mii
        mag = (muB/(hbar*2*pi))*(gJ*mj + gI*mi)*B*1e-4; % B is in Gauss
    else 
        mag = 0;
    end
end

