/* ========================================================
   GOAL-BASED ATM FRAUD DETECTION AGENT IN PROLOG
   ========================================================
   
   PERCEPTS (Inputs from Environment):
   1. transaction_amount - The amount being withdrawn/transferred
   2. account_balance - Current account balance
   3. location - Geographic location of transaction
   4. time - Time of transaction (hour of day)
   5. transaction_count_today - Number of transactions today
   6. days_since_last_transaction - Days since last activity
   7. is_foreign_location - Whether location is unusual
   8. transaction_velocity - Multiple transactions in short time
   
   GOAL: Protect customer accounts by detecting and preventing
         fraudulent transactions while allowing legitimate ones.
   ======================================================== */

% ============ ACCOUNT DATABASE ============
% account(AccountNumber, Balance, HomeLocation, AverageWithdrawal)
account(12345, 5000, 'New York', 200).
account(67890, 2000, 'Los Angeles', 150).
account(11111, 10000, 'Chicago', 500).
account(22222, 1500, 'Miami', 100).

% ============ TRANSACTION HISTORY ============
% recent_transaction(AccountNumber, Amount, Date)
recent_transaction(12345, 150, '2026-02-17').
recent_transaction(67890, 100, '2026-02-15').

% ============ FRAUD DETECTION RULES ============

% PERCEPT ANALYSIS: Check if transaction amount is suspicious
suspicious_amount(Amount, AverageWithdrawal) :-
    Amount > AverageWithdrawal * 5,
    write('  [PERCEPT] Unusual amount detected: '), write(Amount), 
    write(' is 5x higher than average '), write(AverageWithdrawal), nl.

% PERCEPT ANALYSIS: Check if location is suspicious
suspicious_location(TransactionLocation, HomeLocation) :-
    TransactionLocation \= HomeLocation,
    write('  [PERCEPT] Foreign location detected: '), write(TransactionLocation),
    write(' (Home: '), write(HomeLocation), write(')'), nl.

% PERCEPT ANALYSIS: Check if time is unusual (late night transactions)
suspicious_time(Hour) :-
    (Hour >= 23; Hour =< 4),
    write('  [PERCEPT] Unusual time detected: '), write(Hour), write(':00 hours'), nl.

% PERCEPT ANALYSIS: Check transaction velocity
suspicious_velocity(TransactionCountToday) :-
    TransactionCountToday >= 5,
    write('  [PERCEPT] High transaction velocity: '), 
    write(TransactionCountToday), write(' transactions today'), nl.

% PERCEPT ANALYSIS: Check if account has sufficient balance
insufficient_balance(Balance, Amount) :-
    Balance < Amount,
    write('  [PERCEPT] Insufficient balance: '), write(Balance),
    write(' < '), write(Amount), nl.

% PERCEPT ANALYSIS: Check dormant account suddenly active
dormant_account_activation(DaysSinceLastTransaction) :-
    DaysSinceLastTransaction > 90,
    write('  [PERCEPT] Dormant account activation: '), 
    write(DaysSinceLastTransaction), write(' days since last transaction'), nl.

% ============ GOAL-BASED DECISION ENGINE ============

% Calculate fraud risk score based on percepts
calculate_risk_score(Amount, AverageWithdrawal, TransactionLocation, HomeLocation, 
                     Hour, TransactionCountToday, DaysSinceLastTransaction, Score) :-
    write('[ANALYZING PERCEPTS]'), nl,
    
    % Initialize score
    BaseScore = 0,
    
    % Add points for each suspicious percept
    (suspicious_amount(Amount, AverageWithdrawal) -> Score1 = 30 ; Score1 = 0),
    (suspicious_location(TransactionLocation, HomeLocation) -> Score2 = 25 ; Score2 = 0),
    (suspicious_time(Hour) -> Score3 = 15 ; Score3 = 0),
    (suspicious_velocity(TransactionCountToday) -> Score4 = 20 ; Score4 = 0),
    (dormant_account_activation(DaysSinceLastTransaction) -> Score5 = 10 ; Score5 = 0),
    
    % Calculate total risk score
    Score is BaseScore + Score1 + Score2 + Score3 + Score4 + Score5,
    write('[RISK SCORE CALCULATED: '), write(Score), write('/100]'), nl.

% ============ DECISION RULES ============

% APPROVE TRANSACTION: Low risk and sufficient balance
approve_transaction(AccountNumber, Amount, Balance, RiskScore) :-
    RiskScore < 40,
    Balance >= Amount,
    NewBalance is Balance - Amount,
    write(''), nl,
    write('>>> DECISION: TRANSACTION APPROVED <<<'), nl,
    write('Reason: Low fraud risk (Score: '), write(RiskScore), write('/100)'), nl,
    write('Amount withdrawn: $'), write(Amount), nl,
    write('New balance: $'), write(NewBalance), nl.

% DECLINE TRANSACTION: High risk
decline_transaction_high_risk(AccountNumber, Amount, RiskScore) :-
    RiskScore >= 40,
    write(''), nl,
    write('>>> DECISION: TRANSACTION DECLINED <<<'), nl,
    write('Reason: High fraud risk detected (Score: '), write(RiskScore), write('/100)'), nl,
    write('Recommended action: Contact customer for verification'), nl.

% DECLINE TRANSACTION: Insufficient balance
decline_transaction_insufficient_funds(AccountNumber, Amount, Balance) :-
    Balance < Amount,
    write(''), nl,
    write('>>> DECISION: TRANSACTION DECLINED <<<'), nl,
    write('Reason: Insufficient funds'), nl,
    write('Available: $'), write(Balance), write(', Requested: $'), write(Amount), nl.

% ============ MAIN AGENT LOGIC ============

% Process transaction with all percepts
process_transaction(AccountNumber, Amount, TransactionLocation, Hour, 
                    TransactionCountToday, DaysSinceLastTransaction) :-
    write(''), nl,
    write('================================================'), nl,
    write('  ATM FRAUD DETECTION AGENT - Transaction Analysis'), nl,
    write('================================================'), nl,
    write('Account: '), write(AccountNumber), nl,
    write('Amount: $'), write(Amount), nl,
    write('Location: '), write(TransactionLocation), nl,
    write('Time: '), write(Hour), write(':00'), nl,
    write('------------------------------------------------'), nl,
    
    % Retrieve account information
    account(AccountNumber, Balance, HomeLocation, AverageWithdrawal),
    
    % Calculate risk score based on percepts
    calculate_risk_score(Amount, AverageWithdrawal, TransactionLocation, 
                        HomeLocation, Hour, TransactionCountToday, 
                        DaysSinceLastTransaction, RiskScore),
    
    % Make decision based on goal (protect account while allowing legitimate transactions)
    write('------------------------------------------------'), nl,
    write('[MAKING DECISION]'), nl,
    (   
        % Check if balance is sufficient first
        Balance < Amount ->
        decline_transaction_insufficient_funds(AccountNumber, Amount, Balance)
    ;
        % Check risk score
        RiskScore >= 40 ->
        decline_transaction_high_risk(AccountNumber, Amount, RiskScore)
    ;
        % Approve if all checks pass
        approve_transaction(AccountNumber, Amount, Balance, RiskScore)
    ),
    write('================================================'), nl, nl.

% Alternative: process transaction without account check (will fail gracefully)
process_transaction(AccountNumber, _, _, _, _, _) :-
    \+ account(AccountNumber, _, _, _),
    write(''), nl,
    write('>>> DECISION: TRANSACTION DECLINED <<<'), nl,
    write('Reason: Account '), write(AccountNumber), write(' not found'), nl, nl.

% ============ TEST SCENARIOS ============

% Test Case 1: Normal transaction - should APPROVE
test_normal_transaction :-
    write('TEST 1: Normal Transaction'), nl,
    process_transaction(12345, 150, 'New York', 14, 2, 1).

% Test Case 2: Suspicious amount - should DECLINE
test_suspicious_amount :-
    write('TEST 2: Suspicious Large Amount'), nl,
    process_transaction(12345, 2000, 'New York', 14, 2, 1).

% Test Case 3: Foreign location + late night - should DECLINE
test_foreign_location :-
    write('TEST 3: Foreign Location + Late Night'), nl,
    process_transaction(67890, 500, 'Moscow', 2, 1, 5).

% Test Case 4: High velocity - should DECLINE
test_high_velocity :-
    write('TEST 4: High Transaction Velocity'), nl,
    process_transaction(11111, 400, 'Chicago', 15, 6, 2).

% Test Case 5: Dormant account - should DECLINE
test_dormant_account :-
    write('TEST 5: Dormant Account Activation'), nl,
    process_transaction(22222, 200, 'Miami', 10, 1, 120).

% Test Case 6: Insufficient balance - should DECLINE
test_insufficient_balance :-
    write('TEST 6: Insufficient Balance'), nl,
    process_transaction(67890, 5000, 'Los Angeles', 14, 2, 1).

% Run all tests
run_all_tests :-
    test_normal_transaction,
    test_suspicious_amount,
    test_foreign_location,
    test_high_velocity,
    test_dormant_account,
    test_insufficient_balance.
