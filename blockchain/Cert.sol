// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Cert {
    struct Certificate {
        bytes32 hash;
        string cid;
        uint256 issuedAt;
        bool revoked;
    }

    mapping(bytes32 => Certificate) private certificates;
    address public immutable owner;
    event Issued(bytes32 indexed hash, string cid, uint256 issuedAt);
    event Revoked(bytes32 indexed hash, uint256 revokedAt);
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    constructor() {
        owner = msg.sender;
    }

    function issueCertificate(bytes32 _hash, string calldata _cid) external onlyOwner {
        require(certificates[_hash].issuedAt == 0, "Certificate already issued");

        certificates[_hash] = Certificate({
            hash: _hash,
            cid: _cid,
            issuedAt: block.timestamp,
            revoked: false
        });

        emit Issued(_hash, _cid, block.timestamp);
    }
    function revokeCertificate(bytes32 _hash) external onlyOwner {
        Certificate storage cert = certificates[_hash];
        require(cert.issuedAt != 0, "Certificate not found");
        require(!cert.revoked, "Already revoked");

        cert.revoked = true;
        emit Revoked(_hash, block.timestamp);
    }
    function getCertificate(bytes32 _hash) external view returns (string memory cid, uint256 issuedAt, bool revoked) {
        Certificate storage cert = certificates[_hash];
        require(cert.issuedAt != 0, "Certificate not found");

        return (cert.cid, cert.issuedAt, cert.revoked);
    }
}
