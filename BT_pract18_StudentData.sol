// SPDX-License-Identifier: MIT
// ^ licence line required at the top of every Solidity file

// BT Practical 18: Store student data using STRUCTURES, ARRAYS and a FALLBACK function.
// Deploy on Ethereum (test network) and observe the TRANSACTION FEE and GAS values.
//
// HOW TO RUN (Remix IDE):
//  1. Open https://remix.ethereum.org -> contracts folder -> New File "StudentData.sol" -> paste this code.
//  2. Solidity Compiler tab -> version 0.8.x -> "Compile StudentData.sol".
//  3. Deploy & Run tab -> Environment "Injected Provider - MetaMask" (Sepolia test network, needs test ETH)
//     or "Remix VM" for a quick local test -> click "Deploy".
//  4. Note the deployment transaction in the Remix console: click it and write down
//       "gas" (limit), "transaction cost" (gas used), "execution cost".  On Sepolia also open the
//       transaction on sepolia.etherscan.io to see "Gas Price" and "Transaction Fee".
//  5. Call addStudent, e.g.  1, "Yash", "Computer", 85  -> note gas used again.
//  6. Call getStudent(0), getStudentCount(), and the public "students" array with index 0 (free calls).
//  7. Test the fallback: scroll to "Low level interactions", type 0x1234 in CALLDATA, click "Transact"
//     -> fallback() runs (check the FallbackCalled event in the logs).
//     Put 1 wei in VALUE with empty CALLDATA and click "Transact" -> receive() runs.
//  8. Fill a table: Operation | Gas used | Transaction fee  (deploy, addStudent, fallback) -> include in write-up.

pragma solidity ^0.8.0;                                   // compiler version 0.8.x

contract StudentData {                                    // contract = program stored on the blockchain

    struct Student {                                      // STRUCTURE: groups related fields into one custom type
        uint256 rollNo;                                   // roll number (unsigned integer)
        string name;                                      // student name (text)
        string branch;                                    // department / branch
        uint256 marks;                                    // marks out of 100
    }

    Student[] public students;                            // ARRAY: dynamic list of Student structs (public = auto getter by index)
    address public owner;                                 // who deployed the contract

    event StudentAdded(uint256 index, uint256 rollNo, string name);   // log when a student is added
    event FallbackCalled(address sender, uint256 value, bytes data);  // log when fallback() runs
    event EtherReceived(address sender, uint256 value);               // log when receive() runs

    constructor() {                                       // runs once at deployment
        owner = msg.sender;                               // save deployer's address
    }

    modifier onlyOwner() {                                // MODIFIER: reusable check added to functions
        require(msg.sender == owner, "Only owner can add students");   // stop if caller is not the owner
        _;                                                // "_" = run the rest of the function here
    }

    // Add a new student record (writes to storage -> costs gas)
    function addStudent(uint256 _rollNo, string memory _name, string memory _branch, uint256 _marks) public onlyOwner {
        require(_marks <= 100, "Marks must be between 0 and 100");      // validate input
        students.push(Student(_rollNo, _name, _branch, _marks));        // create struct and append it to the array
        emit StudentAdded(students.length - 1, _rollNo, _name);         // log the index where it was stored
    }

    // Read one student by array index (view -> free when called from Remix)
    function getStudent(uint256 index) public view returns (uint256, string memory, string memory, uint256) {
        require(index < students.length, "Student does not exist");     // avoid reading outside the array
        Student memory s = students[index];               // copy the struct from storage into memory
        return (s.rollNo, s.name, s.branch, s.marks);     // return all four fields
    }

    // Number of students stored
    function getStudentCount() public view returns (uint256) {
        return students.length;                           // length of the dynamic array
    }

    // FALLBACK: runs when someone calls a function that does not exist (or sends data that matches nothing)
    fallback() external payable {
        emit FallbackCalled(msg.sender, msg.value, msg.data);   // record who called, Ether sent and the raw data
    }

    // RECEIVE: runs when plain Ether is sent to the contract with EMPTY data
    receive() external payable {
        emit EtherReceived(msg.sender, msg.value);        // record the Ether transfer
    }
}
