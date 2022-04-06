#!/bin/bash
# DoB26Fj4x9LboAFWJra17O
curl -s -X POST "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0AMDEyMzQ1Njc4OWxtbm9wcQ\"}" | jq
curl -s -X POST "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"holder\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0AMDEyMzQ1Njc4OWxtbm9abc\"}" | jq
sleep 3

curl -s -X PUT "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
curl -s -X PUT "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"holder\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/ids/issuer" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[\"BGKVzj4ve0VSd8z_AmvhLg4lqcC_9WYX90k03q-R_Ydo\", \"BuyRFMideczFZoapylLIyCjSdhtqVb31wZkRKvPfNqkw\",\"Bgoq68HCmYNUDgOz4Skvlu306o_NY-NrYuKAVhk3Zh9c\"],\"toad\":3, \"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
curl -s -X POST "http://localhost:5723/ids/holder" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[\"BGKVzj4ve0VSd8z_AmvhLg4lqcC_9WYX90k03q-R_Ydo\", \"BuyRFMideczFZoapylLIyCjSdhtqVb31wZkRKvPfNqkw\",\"Bgoq68HCmYNUDgOz4Skvlu306o_NY-NrYuKAVhk3Zh9c\"],\"toad\":3, \"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/registries" -H "accept: */*" -H "Content-Type: application/json" -d "{\"alias\":\"issuer\",\"baks\":[],\"estOnly\":false,\"name\":\"vLEI\",\"noBackers\":true,\"toad\":0}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/oobi/holder" -H "accept: */*" -H "Content-Type: application/json" -d "{\"url\":\"http://127.0.0.1:5643/oobi/Ew9ae1KDP6apL8N7WeyaUBCXOEbEmCcO6uzgCo3WU72A/witness/BuyRFMideczFZoapylLIyCjSdhtqVb31wZkRKvPfNqkw\"}" | jq
curl -s -X POST "http://localhost:5723/oobi/issuer" -H "accept: */*" -H "Content-Type: application/json" -d "{\"url\":\"http://127.0.0.1:5644/oobi/Ew-o5dU5WjDrxDBK4b4HrF82_rYb6MX6xsegjq4n0Y7M/witness/Bgoq68HCmYNUDgOz4Skvlu306o_NY-NrYuKAVhk3Zh9c\"}" | jq