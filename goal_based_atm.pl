/* ================================
   GOAL-BASED ATM AGENT IN PROLOG
   ================================ */

% Facts: account(AccountNumber, Balance).
account(12345, 5000).
account(67890, 2000).

% Goal: successfully withdraw money without overdraft

% Rule: check if withdrawal is possible
can_withdraw(AccountNumber, Amount) :-
    account(AccountNumber, Balance),
    Balance >= Amount.

% Rule: perform withdrawal if goal is achievable
withdraw(AccountNumber, Amount, NewBalance) :-
    can_withdraw(AccountNumber, Amount),
    account(AccountNumber, Balance),
    NewBalance is Balance - Amount,
    write('Withdrawal successful.'), nl,
    write('New balance is: '), write(NewBalance), nl.

% Rule: failure case when goal cannot be achieved
withdraw(AccountNumber, Amount, _) :-
    account(AccountNumber, Balance),
    Balance < Amount,
    write('Withdrawal failed.'), nl,
    write('Insufficient balance.'), nl.

% Goal-based decision making
goal_based_agent(AccountNumber, Amount) :-
    write('Goal: Withdraw '), write(Amount), write(' from account '),
    write(AccountNumber), nl,
    withdraw(AccountNumber, Amount, _).
