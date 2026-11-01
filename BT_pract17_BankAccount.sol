// SPDX-License-Identifier: MIT
// ^ licence line: every Solidity file should start with one, otherwise the compiler shows a warning

// BT Practical 17: Smart contract for a customer's bank account
// Operations: 1) Deposit money  2) Withdraw money  3) Show balance
//
// HOW TO RUN (Remix IDE):
//  1. Open https://remix.ethereum.org in Chrome.
//  2. File Explorer (left) -> "contracts" folder -> New File -> name it BankAccount.sol -> paste this code.
//  3. Solidity Compiler tab (2nd icon) -> choose version 0.8.x -> click "Compile BankAccount.sol" (green tick = OK).
//  4. Deploy & Run tab (3rd icon) -> Environment:
//       "Remix VM (Cancun)"            -> free fake accounts with 100 ETH each (easiest), OR
//       "Injected Provider - MetaMask" -> real test network (Sepolia) using your MetaMask wallet.
//  5. Click "Deploy" (confirm in MetaMask if using a test network).
//  6. Under "Deployed Contracts" expand BankAccount and test:
//       Deposit : type 1 in the VALUE box, choose "ether", click the red "deposit" button.
//       Balance : click blue "getBalance" -> shows 1000000000000000000 (1 ETH in Wei).
//       Withdraw: type 500000000000000000 (0.5 ETH in Wei) next to "withdraw", click it.
//       Error   : try to withdraw more than your balance -> transaction reverts with "Insufficient balance".
//  7. Take screenshots of each step and of the transaction details (gas used, fee) in the Remix console.

pragma solidity ^0.8.0;                                   // compile with any 0.8.x compiler (0.8 has built-in overflow checks)

contract BankAccount {                                    // a contract is like a class that lives on the blockchain

    mapping(address => uint256) private balances;         // mapping = dictionary: wallet address -> balance in Wei
    address public owner;                                 // address that deployed the contract (public = auto getter)

    event Deposited(address indexed customer, uint256 amount);   // event = log entry saved in the transaction
    event Withdrawn(address indexed customer, uint256 amount);   // "indexed" lets apps search logs by customer

    constructor() {                                       // runs ONLY once, when the contract is deployed
        owner = msg.sender;                               // msg.sender = the address that sent this transaction
    }

    // 1) DEPOSIT: "payable" means this function can receive Ether along with the call
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");   // msg.value = Ether sent (in Wei); stop if 0
        balances[msg.sender] += msg.value;                // add the sent Ether to the caller's balance
        emit Deposited(msg.sender, msg.value);            // write a log entry for this deposit
    }

    // 2) WITHDRAW: send Ether from the contract back to the caller
    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be greater than 0");               // check: valid amount
        require(balances[msg.sender] >= amount, "Insufficient balance");    // check: enough money (else revert)
        balances[msg.sender] -= amount;                   // effect: reduce balance FIRST (prevents re-entrancy attack)
        payable(msg.sender).transfer(amount);             // interaction: send the Ether to the caller's wallet
        emit Withdrawn(msg.sender, amount);               // write a log entry for this withdrawal
    }

    // 3) SHOW BALANCE: "view" = only reads data, so calling it is free (no gas, no transaction)
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];                      // balance of whoever is calling, in Wei
    }

    // Extra: total Ether held by the contract (sum of all customers' deposits)
    function getBankBalance() public view returns (uint256) {
        return address(this).balance;                     // address(this) = this contract's own address
    }
}
