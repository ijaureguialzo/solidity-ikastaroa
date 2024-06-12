// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract AddressStorage {
    mapping(address => uint256) saldo;

    function store(address direccion, uint256 numero) public {
        saldo[direccion] = numero;
    }

    function retrieve(address direccion) public view returns (uint256) {
        return saldo[direccion];
    }
}
