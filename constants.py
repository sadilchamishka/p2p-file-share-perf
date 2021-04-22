HEADER_LENGTH = 4
BUFFER_SIZE = 9999

RESPONSE_CODES = {
    "REGOK": {
        "0": {"stat": True, "msg": "request is successful, no nodes in the system"},
        "1": {"stat": True, "msg": "request is successful, 1 or 2 nodes' contacts will be returned"},
        "2": {"stat": True, "msg": "request is successful, 1 or 2 nodes' contacts will be returned"},
        "9999": {"stat": False, "msg": "failed, there is some error in the command"},
        "9998": {"stat": False, "msg": "failed, already registered to you, unregister first"},
        "9997": {"stat": False, "msg": "failed, registered to another user, try a different IP and port"},
        "9996": {"stat": False, "msg": " failed, can’t register. BS full"}
    },
    "UNROK": {
        "0": {"stat": True, "msg": "successful"},
        "9999": {"stat": False, "msg": "error while unregistering. IP and port may not be in the registry or command is incorrect."}
    },
    "JOINOK": {
        "0": {"stat": True, "msg": "successful"},
        "9999": {"stat": False, "msg": "error while adding new node to routing table"}
    },
    "LEAVEOK": {
        "0": {"stat": True, "msg": "successful"},
        "9999": {"stat": False, "msg": "error while removing node from routing table"}
    },
    "SEROK": {
        "1": {"stat": True, "msg": "successful"}, # the key can be <=1 , thats why,  the key is number of files found 
        "2": {"stat": True, "msg": "successful"},
        "3": {"stat": True, "msg": "successful"},
        "4": {"stat": True, "msg": "successful"},
        "5": {"stat": True, "msg": "successful"},
        "6": {"stat": True, "msg": "successful"},
        "7": {"stat": True, "msg": "successful"},
        "0": {"stat": False, "msg": "no matching results. Searched key is not in key table"},
        "9999": {"stat": False, "msg": "failure due to node unreachable"},
        "9998": {"stat": False, "msg": "some other error."}
    },
    "ERROR": {
        "0001": {"stat": False, "msg": "Request Timeout"}
    },
}